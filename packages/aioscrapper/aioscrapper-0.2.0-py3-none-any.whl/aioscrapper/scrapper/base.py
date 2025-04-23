import abc


class BaseScrapper(abc.ABC):
    @abc.abstractmethod
    async def start(self, *args, **kwargs) -> None:
        """
        Starts the scrapper.

        This method is called to start the scraper by sending the initial requests required for its operation.
        """
        ...

    async def initialize(self, *args, **kwargs) -> None:
        """
        Initializes the scrapper.

        This method is called before starting the scrapper. It should be used to initialize any
        necessary state or resources required by the scrapper.
        """
        ...

    async def close(self, *args, **kwargs) -> None:
        """
        Closes the scrapper.

        This method is called to clean up any resources created by the scrapper after it has finished
        running.
        """
        ...
