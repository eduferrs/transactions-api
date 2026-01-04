from http import HTTPStatus


class CreateUserError(Exception):
    def __init__(self, message: str = "CPF ou E-mail já cadastrado", status_code: int = HTTPStatus.CONFLICT) -> None:
        self.message = message
        self.status_code = status_code


class InternalServerError(Exception):
    def __init__(
        self, message: str = "Internal server error", status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    ) -> None:
        self.message = message
        self.status_code = status_code
