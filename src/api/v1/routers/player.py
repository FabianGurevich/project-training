from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.core.dependencies import get_session
from src.api.v1.schemas.player import PlayerCreate, PlayerUpdate
from src.controllers.player import PlayerController
from src.api.v1.core.database import Session
from src.controllers.team import TeamController
from src.models.club import Club
from src.models.player import Positions


router = APIRouter()


@router.post("/create", status_code=201)
def create_player(
    info_to_create: PlayerCreate,
    session: Session = Depends(get_session),
) -> PlayerCreate:
    club = Club.objects(session).get(Club.name == info_to_create.club_name)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    if info_to_create.position not in Positions.__members__:
        raise HTTPException(
            status_code=400,
            detail="Invalid position, must be one of: "
            + ", ".join(Positions.__members__),
        )
    player = PlayerController.create_player(
        info=info_to_create, club_id=club.id, session=session
    )
    return player


@router.get("/ranked_team/{player_id}", status_code=200)
def get_ranked_teams(player_id: UUID, session: Session = Depends(get_session)):
    player = PlayerController.get_player(player_id, session)
    ranked_teams = sorted(player.teams, key=lambda x: x.score, reverse=True)
    return ranked_teams


@router.put("/update/{player_id}", status_code=200)
def update_player_info(
    player_id: UUID,
    info_to_update: PlayerUpdate,
    session: Session = Depends(get_session),
) -> None:
    player = PlayerController.get_player(player_id, session)
    new_club_id = None
    if info_to_update.club_name:
        club = Club.objects(session).get(Club.name == info_to_update.club_name)
        if club:
            new_club_id = club.id
    player_updated = PlayerController.update_player(
        info=info_to_update, player=player, club_id=new_club_id, session=session
    )
    if info_to_update.score and player.teams is not None:
        for team in player.teams:
            TeamController.update_team_score(team.id, session)
    return player_updated


@router.delete("/{player_id}", status_code=200)
def delete_player(player_id: UUID, session: Session = Depends(get_session)) -> None:
    player = PlayerController.get_player(player_id, session)
    for team in player.teams:
        team.players.remove(player)
        TeamController.update_team_score(team.id, session)
    session.delete(player)
    session.commit()
    return None
