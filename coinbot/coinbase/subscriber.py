from requests import Response

from coinbot.coinbase.client import Client


class Subscriber:
    def __init__(self, client: Client = None):
        self.__client = client if client else Client()

    @property
    def client(self) -> Client:
        return self.__client

    # NOTE: error is left here as a convenience method for plugs
    def error(self, response: Response) -> bool:
        return 200 != response.status_code
