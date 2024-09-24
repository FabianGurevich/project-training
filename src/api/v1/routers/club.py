from fastapi import APIRouter, Depends

from src.api.v1.core.dependencies import get_session
from src.api.v1.schemas.club import CreateClub
from src.controllers.club import ClubController
from src.api.v1.core.database import Session


router = APIRouter()


@router.post("/create", status_code=201)
def create_club(
    club_info: CreateClub, session: Session = Depends(get_session)
) -> CreateClub:
    club = ClubController.create_club(club_info, session)
    return club
