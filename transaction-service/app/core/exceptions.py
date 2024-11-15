from typing import Any

from fastapi import HTTPException, status


class AuthError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)


class NotFoundError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)


class EntityError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, headers)


class AlreadyExistsError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)
