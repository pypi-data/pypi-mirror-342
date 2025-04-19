from httpx import Response


class ClientError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response: Response | None = None,
    ):
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class AuthError(ClientError):
    pass


class NotFoundError(ClientError):
    pass


class RateLimitError(ClientError):
    pass


class RequestError(ClientError):
    pass


class ResponseError(ClientError):
    pass
