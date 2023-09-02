""" errors module """


from typing import Any, Optional, Dict

from fastapi import HTTPException
from starlette import status


class NotFoundException(HTTPException):
    """ not found exception class """

    def __init__(
            self,
            detail: Any = "Not found",
            headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        self.headers = headers
