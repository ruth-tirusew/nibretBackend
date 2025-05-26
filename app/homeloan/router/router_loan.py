from fastapi import Depends, HTTPException, status, Body
from typing import Optional, List

from app.homeloan.service import Service, get_service
from app.homeloan.models.loan import *
from . import router


@router.post("",status_code=status.HTTP_201_CREATED, response_model=Optional[Homeloan])
def register_loan(
    input: Homeloan,
    svc: Service = Depends(get_service),
) -> Homeloan:
    loan_response = svc.repository.register_loan(input)

    return loan_response

@router.put("/{id}",status_code=status.HTTP_200_OK, response_model=Optional[Homeloan])
def update_loan(
    id: str,
    input: Homeloan,
    svc: Service = Depends(get_service),
) -> Homeloan:
    loan_response = svc.repository.update_loan(id, input)

    return loan_response

@router.delete("/{id}",status_code=status.HTTP_200_OK, response_model=bool)
def delete_loan(
    id: str,
    svc: Service = Depends(get_service),
) -> bool:
    if not svc.repository.get_loan_by_id(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Homeloan not found",
        )

    loan_response = svc.repository.delete_loan(id)

    return loan_response

@router.get("",status_code=status.HTTP_200_OK, response_model=Optional[List[HomeloanResponse]])
def fetch_loans(
    svc: Service = Depends(get_service),
) -> List[HomeloanResponse]:
    loan_response = svc.repository.get_loans().to_list()

    print(loan_response)
    return loan_response


@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=Optional[Homeloan])
def fetch_loan(
    id: str,
    svc: Service = Depends(get_service),
) -> Homeloan:
    loan_response = svc.repository.get_loan_by_id(id)
    if not loan_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Homeloan not found",
        )

    return loan_response




