from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"User with ID {user_id} not found"
        super().__init__(self.message)


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )
