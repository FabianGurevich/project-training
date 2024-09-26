from uuid import UUID
from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends

from src.api.v1.core.dependencies import get_session, get_user
from src.api.v1.schemas.team import AddRemovePlayer, TeamCreate, TeamInfo
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


@router.post("/add_player", status_code=200)
def add_player_to_team(
    add_player_data: AddRemovePlayer,
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


@router.post("/remove_player", status_code=200)
def remove_player_from_team(
    add_player_data: AddRemovePlayer,
    session: Session = Depends(get_session),
    request: Request = None,
) -> None:
    logged_user = get_user(request=request, session=session)
    if not logged_user:
        HTTPException(status_code=401, detail="Unauthorized")
    TeamController.remove_player_from_team(
        team_id=add_player_data.team_id,
        player_id=add_player_data.player_id,
        session=session,
        owner_id=logged_user.id,
    )
    return {"message": "Player removed from team successfully."}


@router.get("/list_teams_user", status_code=200, response_model=list[TeamInfo])
def get_teams_from_user(
    session: Session = Depends(get_session), request: Request = None
):
    logged_user = get_user(request=request, session=session)
    if not logged_user:
        HTTPException(status_code=401, detail="Unauthorized")
    teams = TeamController.get_teams(user_id=logged_user.id, session=session)
    return teams


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


@router.delete("/{team_id}", status_code=200)
def delete_team(
    team_id: UUID, session: Session = Depends(get_session), request: Request = None
) -> None:
    logged_user = get_user(request=request, session=session)
    if not logged_user:
        HTTPException(status_code=401, detail="Unauthorized")

    TeamController.delete_team(
        team_id=team_id, owner_id=logged_user.id, session=session
    )
    return {"message": "Team deleted successfully."}
