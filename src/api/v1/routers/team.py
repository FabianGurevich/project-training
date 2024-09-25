from uuid import UUID
from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends

from src.api.v1.core.dependencies import get_session, get_user
from src.api.v1.schemas.team import AddPlayer, TeamCreate, TeamInfo
from src.api.v1.core.database import Session
from src.controllers.team import TeamController


router = APIRouter()


@router.post("/create", status_code=201)
def create_team(
    team_data: TeamCreate,
    session: Session = Depends(get_session),
    request: Request = None,
) -> TeamCreate:
    logged_user = get_user(request=request, session=session)
    info_with_owner = TeamCreate(owner_id=logged_user.id, **team_data.model_dump())
    team = TeamController.create_team(
        info=info_with_owner, session=session, owner_id=logged_user.id
    )
    return team


@router.post("/add_player", status_code=201)
def add_player_to_team(
    add_player_data: AddPlayer,
    session: Session = Depends(get_session),
    request: Request = None,
) -> None:
    logged_user = get_user(request=request, session=session)
    if not logged_user:
        HTTPException(status_code=401, detail="Unauthorized")
    TeamController.add_player_to_team(
        team_id=add_player_data.team_id,
        player_id=add_player_data.player_id,
        session=session,
        owner_id=logged_user.id,
    )
    return {"message": "Player added to team successfully."}


@router.get("/{team_id}", response_model=TeamInfo)
def get_team(team_id: UUID, session: Session = Depends(get_session)) -> TeamInfo:
    team = TeamController.get_team(team_id=team_id, session=session)
    players = [player.name for player in team.players]
    team_info = TeamInfo(
        name=team.name,
        description=team.description,
        formation=team.formation,
        score=team.score,
        id=team.id,
        players=players,
    )
    return team_info
