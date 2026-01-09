from http import HTTPStatus


class CreateUserError(Exception):
    def __init__(self, message: str = "CPF or e-mail already exists", status_code: int = HTTPStatus.CONFLICT) -> None:
        self.message = message
        self.status_code = status_code


class AccountNotFoundError(Exception):
    def __init__(self, message: str = "Account not found", status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY) -> None:
        self.message = message
        self.status_code = status_code


class BusinessError(Exception):
    def __init__(self, message: str = "Action not allowed", status_code: int = HTTPStatus.BAD_REQUEST) -> None:
        self.message = message
        self.status_code = status_code


class InternalServerError(Exception):
    def __init__(
        self, message: str = "Internal server error", status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    ) -> None:
        self.message = message
        self.status_code = status_code
