from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.models.user import *
from app.lead.models.lead_management import *
from . import router
from ..service import Service, get_service
from app.auth.service import Service as AuthService
from app.auth.service import get_service as get_auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login/", auto_error=True)


# @router.post(
#     "/register", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse
# )
# def register_lead(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     input: RegisterUserRequest,
#     svc: Service = Depends(get_service),
# ) -> dict[str, str]:



#     svc.create_user(input)

#     return RegisterUserResponse(email=input.email)


@router.post(
    "/register/alert", status_code=status.HTTP_201_CREATED, response_model=LeadActivityResponse
)
async def register_activity(
    token: Annotated[str, Depends(oauth2_scheme)],
    input: LeadActivity,
    svc: Service = Depends(get_service),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    print(token)
    user = await auth_service.get_current_user(token)
    input.agent_id = str(user['_id'])
    result = svc.add_activity(input)
    return result


@router.post(
    "/register/alert/email", status_code=status.HTTP_201_CREATED, response_model=LeadActivityResponse
)
async def register_activity(
    token: Annotated[str, Depends(oauth2_scheme)],
    input: LeadActivity,
    svc: Service = Depends(get_service),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    print(token)
    user = await auth_service.get_current_user(token)
    input.agent_id = str(user['_id'])
    result = svc.add_activity(input)
    return result


@router.get(
    "/alert", status_code=status.HTTP_200_OK, response_model=Optional[List[LeadActivityResponse]]
)
async def fetch_activities(
    token: Annotated[str, Depends(oauth2_scheme)],
    svc: Service = Depends(get_service)
):

    return svc.get_all_activities()



@router.get(
    "/alert/{agentId}", status_code=status.HTTP_200_OK, response_model=Optional[List[LeadActivityResponse]]
)
async def fetch_agent_activity(
    token: Annotated[str, Depends(oauth2_scheme)],
    agentId: str,
    svc: Service = Depends(get_service)
):

    return svc.get_all_activities()


@router.get(
    "/alert/detail/{activityId}", status_code=status.HTTP_200_OK, response_model=Optional[List[LeadActivityResponse]]
)
async def fetch_activity_detail(
    token: Annotated[str, Depends(oauth2_scheme)],
    activityId: str,
    svc: Service = Depends(get_service)
):

    return svc.get_all_activities()





