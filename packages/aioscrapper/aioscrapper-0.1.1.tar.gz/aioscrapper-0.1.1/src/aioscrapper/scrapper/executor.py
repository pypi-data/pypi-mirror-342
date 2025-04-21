import asyncio
import time
from logging import Logger, getLogger
from types import TracebackType
from typing import Type, Any

from aiojobs import Scheduler

from .request_manager import RequestManager
from ..config import Config
from ..helpers import get_func_kwargs
from ..pipeline import PipelineDispatcher, BasePipeline
from ..scrapper import BaseScrapper
from ..session.aiohttp import AiohttpSession
from ..types import RequestMiddleware, ResponseMiddleware


class AIOScrapper:
    def __init__(
        self,
        scrappers: list[BaseScrapper],
        config: Config | None = None,
        logger: Logger | None = None,
    ) -> None:
        self._start_time = time.time()
        self._config = config or Config()
        self._logger = logger or getLogger("aioscrapper")

        self._scrappers = scrappers
        self._request_outer_middlewares = []
        self._request_inner_middlewares = []
        self._response_middlewares = []

        self._pipelines: dict[str, list[BasePipeline]] = {}
        self._pipeline_dispatcher = PipelineDispatcher(
            logger=self._logger.getChild("pipeline"), pipelines=self._pipelines
        )

        def _exception_handler(_, context: dict[str, Any]):
            if "job" in context:
                self._logger.error(f'{context["message"]}: {context["exception"]}', extra={"context": context})
            else:
                self._logger.error("Unhandled error", extra={"context": context})

        self._scheduler = Scheduler(
            limit=self._config.scheduler.concurrent_requests,
            pending_limit=self._config.scheduler.pending_requests,
            close_timeout=self._config.scheduler.close_timeout,
            exception_handler=_exception_handler,
        )

        self._request_queue = asyncio.PriorityQueue()
        self._request_manager = RequestManager(
            logger=self._logger.getChild("request_worker"),
            session=AiohttpSession(
                timeout=self._config.session.request.timeout,
                ssl=self._config.session.request.ssl,
            ),
            schedule_request=self._scheduler.spawn,
            queue=self._request_queue,
            delay=self._config.session.request.delay,
            shutdown_timeout=self._config.execution.shutdown_timeout,
            srv_kwargs={"pipeline": self._pipeline_dispatcher},
            request_outer_middlewares=self._request_outer_middlewares,
            request_inner_middlewares=self._request_inner_middlewares,
            response_middlewares=self._response_middlewares,
        )

    def add_pipeline(self, name: str, pipeline: BasePipeline) -> None:
        if name not in self._pipelines:
            self._pipelines[name] = [pipeline]
        else:
            self._pipelines[name].append(pipeline)

    def add_outer_request_middlewares(self, *middlewares: RequestMiddleware) -> None:
        self._request_outer_middlewares.extend(middlewares)

    def add_inner_request_middlewares(self, *middlewares: RequestMiddleware) -> None:
        self._request_inner_middlewares.extend(middlewares)

    def add_response_middlewares(self, *middlewares: ResponseMiddleware) -> None:
        self._response_middlewares.extend(middlewares)

    async def __aenter__(self) -> "AIOScrapper":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def start(self) -> None:
        await self._pipeline_dispatcher.initialize()
        self._request_manager.listen_queue()

        scrapper_kwargs = {"request_sender": self._request_manager.sender, "pipeline": self._pipeline_dispatcher}
        for scrapper in self._scrappers:
            await scrapper.initialize(**get_func_kwargs(scrapper.initialize, scrapper_kwargs))

        await asyncio.gather(
            *[scrapper.start(**get_func_kwargs(scrapper.start, scrapper_kwargs)) for scrapper in self._scrappers]
        )

    async def _shutdown(self) -> bool:
        status = False
        execution_timeout = (
            max(self._config.execution.timeout - (time.time() - self._start_time), 0.1)
            if self._config.execution.timeout
            else None
        )
        while True:
            if execution_timeout is not None and time.time() - self._start_time > execution_timeout:
                self._logger.log(
                    level=self._config.execution.log_level,
                    msg=f"execution timeout: {self._config.execution.timeout}",
                )
                status = True
                break
            if len(self._scheduler) == 0 and self._request_queue.qsize() == 0:
                break

            await asyncio.sleep(self._config.execution.shutdown_check_interval)

        return status

    async def shutdown(self) -> None:
        force = await self._shutdown()
        await self._request_manager.shutdown(force)

    async def close(self, shutdown: bool = True) -> None:
        if shutdown:
            await self.shutdown()

        scrapper_kwargs = {"pipeline": self._pipeline_dispatcher}
        try:
            for scrapper in self._scrappers:
                await scrapper.close(**get_func_kwargs(scrapper.close, scrapper_kwargs))
        finally:
            await self._scheduler.close()
            await self._request_manager.close()
            await self._pipeline_dispatcher.close()
