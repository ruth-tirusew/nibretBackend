from fastapi import Depends, HTTPException, status, Body
from typing import Optional, List

from app.auctions.service import AuctionService, get_service
from app.auctions.models.auction import *
from . import router


@router.post("",status_code=status.HTTP_201_CREATED, response_model=Optional[Auction])
def register_auction(
    input: Auction,
    svc: AuctionService = Depends(get_service),
) -> Auction:
    auction_response = svc.create_auction(input)

    return auction_response

@router.put("/{id}",status_code=status.HTTP_200_OK, response_model=Optional[Auction])
def update_auction(
    id: str,
    input: Auction,
    svc: AuctionService = Depends(get_service),
) -> Auction:
    auction_response = svc.up(id, input)

    return auction_response

@router.delete("/{id}",status_code=status.HTTP_200_OK, response_model=bool)
def delete_auction(
    id: str,
    svc: AuctionService = Depends(get_service),
) -> bool:
    if not svc.repository.get_auction_by_id(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auction not found",
        )

    auction_response = svc.repository.delete_auction(id)

    return auction_response

@router.get("",status_code=status.HTTP_200_OK)
def fetch_auctions(
    svc: AuctionService = Depends(get_service),
):
    auction_response = svc.repository.get_auctions().to_dict()
    print(auction_response)
    return auction_response


@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=Optional[Auction])
def fetch_auction(
    id: str,
    svc: AuctionService = Depends(get_service),
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
    svc: AuctionService = Depends(get_service),
) -> List[AuctionResponse]:
    auction_response = svc.repository.get_auctions_by_location(coordiantes=coordinates)
    return auction_response



