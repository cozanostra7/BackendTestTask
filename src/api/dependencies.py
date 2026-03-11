from fastapi import Request, Depends, HTTPException
from src.services.auth import AuthService



# def get_token(request: Request) -> str:
#     token = request.cookies.get("access_token")
#     if not token:
#         raise HTTPException(status_code=401, detail="You are not authorized")
#     return token
#
# def get_current_user(token: str = Depends(get_token)):
#     auth_service = AuthService()
#     payload = auth_service.decode_token(token)
#     return {"username": payload["sub"], "role": payload["role"]}



def getCurrentUser():

    return {"username": "admin", "role": "admin"}


