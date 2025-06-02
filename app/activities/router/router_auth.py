from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.models .user import *
from . import router
from app.auth.models.user import JWTData
from ..service import Service, get_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login/", auto_error=True)

@router.post(
    "/users/register", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse
)
def register_user(
    input: RegisterUserRequest,
    svc: Service = Depends(get_service),
) -> dict[str, str]:



    svc.create_user(input)

    return RegisterUserResponse(email=input.email)


@router.get(
     "/users", status_code=status.HTTP_200_OK, 
     response_model=GetAllUsersResponse
)
def fetch_users(
    token: Annotated[str, Depends(oauth2_scheme)],
    svc: Service = Depends(get_service),
):

    users = GetAllUsersResponse(
        users=svc.get_all_users()
    )
    

    return users


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
    token: Annotated[str, Depends(oauth2_scheme)],
    svc: Service = Depends(get_service),
) -> dict[str, str]:

    user = await svc.get_current_user(token)

    return user

@router.post("/accounts/login/", response_model=AuthorizeUserResponse)
def authorize_user(
    input: OAuth2PasswordRequestForm = Depends(),
    svc: Service = Depends(get_service),
) -> AuthorizeUserResponse:
    return AuthorizeUserResponse(
        access_token=svc.login(input),
    )
