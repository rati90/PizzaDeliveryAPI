from fastapi import status
from fastapi.exceptions import HTTPException


async def authorization_token(Authorize, message):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=message
                            )



