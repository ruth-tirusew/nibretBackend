from fastapi import Depends, HTTPException, status, Body
from typing import Optional, List

from app.auctions.service import Service, get_service
from app.auctions.models.auction import *
from . import router


@router.post("",status_code=status.HTTP_201_CREATED, response_model=Optional[Auction])
def register_auction(
    input: Auction,
    svc: Service = Depends(get_service),
) -> Auction:
    auction_response = svc.repository.register_auction(input)

    return auction_response

@router.put("/{id}",status_code=status.HTTP_200_OK, response_model=Optional[Auction])
def update_auction(
    id: str,
    input: Auction,
    svc: Service = Depends(get_service),
) -> Auction:
    auction_response = svc.repository.update_auction(id, input)

    return auction_response

@router.delete("/{id}",status_code=status.HTTP_200_OK, response_model=bool)
def delete_auction(
    id: str,
    svc: Service = Depends(get_service),
) -> bool:
    if not svc.repository.get_auction_by_id(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auction not found",
        )

    auction_response = svc.repository.delete_auction(id)

    return auction_response

@router.get("",status_code=status.HTTP_200_OK, response_model=Optional[List[AuctionResponse]])
def fetch_auctions(
    svc: Service = Depends(get_service),
) -> List[AuctionResponse]:
    auction_response = svc.repository.get_auctions().to_list()

    print(auction_response)
    return auction_response


@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=Optional[Auction])
def fetch_auction(
    id: str,
    svc: Service = Depends(get_service),
) -> Auction:
    auction_response = svc.repository.get_auction_by_id(id)
    if not auction_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auction not found",
        )

    return auction_response

@router.post("/location",status_code=status.HTTP_200_OK, response_model=Optional[List[AuctionResponse]])
def fetch_auctions(
    coordinates: List[float] = Body(),
    svc: Service = Depends(get_service),
) -> List[AuctionResponse]:
    auction_response = svc.repository.get_auctions_by_location(coordiantes=coordinates)
    return auction_response



