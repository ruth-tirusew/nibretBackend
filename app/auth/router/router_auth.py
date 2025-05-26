from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.models.user import *
from app.auth.router import router
from app.auth.service import Service, get_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login/", auto_error=True)

@router.post(
    "/registration", status_code=status.HTTP_201_CREATED, response_model=AuthorizeUserResponse
)
def register_user(
    input: RegisterUserRequest,
    svc: Service = Depends(get_service),
) -> dict[str, str]:    
    return AuthorizeUserResponse(
        access_token=svc.create_user(input))


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


@router.get("/user/", response_model=UserResponse)
async def get_my_account(
    token: Annotated[str, Depends(oauth2_scheme)],
    svc: Service = Depends(get_service),
) -> dict[str, str]:

    user = await svc.get_current_user(token)

    return user

@router.post("/login/", response_model=AuthorizeUserResponse)
def authorize_user(
    input: OAuth2PasswordRequestForm = Depends(),
    svc: Service = Depends(get_service),
) -> AuthorizeUserResponse:
    return AuthorizeUserResponse(
        access_token=svc.login(input),
    )

@router.put("/user/", status_code=status.HTTP_200_OK, response_model=RegisterUserResponse)
def update_profile(
    input: UpdateUserRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    svc: Service = Depends(get_service),
) -> dict[str, str]:

    user = svc.update_profile(token, input)

    return RegisterUserResponse(email=input.email)

@router.put("/user/{id}", status_code=status.HTTP_200_OK, response_model=RegisterUserResponse)
def update_user(
    id:str,
    input: UpdateUserRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    svc: Service = Depends(get_service),
) -> dict[str, str]:

    user = svc.update_user(id, input)
    return RegisterUserResponse(email=input.email)


@router.patch("/user/{id}",status_code=status.HTTP_200_OK)
def update_user_status(
    id:str,
    status: bool, token: Annotated[str, Depends(oauth2_scheme)],
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user = svc.update_user_status(id, status)
    return {
        "detail":"Status updated successully"
    }
