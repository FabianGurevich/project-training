from fastapi import APIRouter, Depends

from src.api.v1.core.dependencies import get_session
from src.api.v1.schemas.player import PlayerCreate
from src.controllers.player import PlayerController
from src.api.v1.core.database import Session
from src.models.club import Club


router = APIRouter()


@router.post("/create", status_code=201)
def create_player(
    info_to_create: PlayerCreate,
    session: Session = Depends(get_session),
) -> PlayerCreate:
    print(info_to_create.club_name)
    print(info_to_create)
    club = Club.objects(session).get(Club.name == info_to_create.club_name)
    player = PlayerController.create_player(
        info=info_to_create, club_id=club.id, session=session
    )
    return player
