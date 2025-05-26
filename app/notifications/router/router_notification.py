from fastapi import Depends, HTTPException, status, Body
from typing import Optional, List

from app.notifications.service import Service, get_service
from app.notifications.models.notifications import *
from . import router


@router.post("/client",status_code=status.HTTP_201_CREATED, response_model=Optional[NotificationClient])
def register_notification_client(
    input: NotificationClient,
    svc: Service = Depends(get_service),
) -> NotificationClient:
    notification_client_response = svc.repository.register_notification_client(input)

    return notification_client_response

@router.put("/client/{id}",status_code=status.HTTP_200_OK, response_model=Optional[NotificationClient])
def update_notification_client(
    id: str,
    input: NotificationClient,
    svc: Service = Depends(get_service),
) -> NotificationClient:
    notification_client_response = svc.repository.update_notification_client(id, input)

    return notification_client_response

@router.delete("/{id}",status_code=status.HTTP_200_OK, response_model=bool)
def delete_notification_client(
    id: str,
    svc: Service = Depends(get_service),
) -> bool:
    if not svc.repository.get_notification_client_by_id(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification client not found",
        )

    notification_client_response = svc.repository.delete_notification_client(id)

    return notification_client_response

@router.get("/client",status_code=status.HTTP_200_OK, response_model=Optional[List[NotificationClientResponse]])
def fetch_properties(
    svc: Service = Depends(get_service),
) -> List[NotificationClientResponse]:
    notification_client_response = svc.repository.get_properties().to_list()

    print(notification_client_response)
    return notification_client_response


@router.get("/client/{id}",status_code=status.HTTP_200_OK, response_model=Optional[NotificationClient])
def fetch_notification_client(
    id: str,
    svc: Service = Depends(get_service),
) -> NotificationClient:
    notification_client_response = svc.repository.get_notification_client_by_id(id)
    if not notification_client_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NotificationClient not found",
        )

    return notification_client_response