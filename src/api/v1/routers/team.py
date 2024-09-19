from fastapi import APIRouter, Request
from fastapi import Depends

from src.api.v1.core.dependencies import get_session, get_user
from src.api.v1.schemas.team import TeamCreate
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
    print(logged_user.id)
    print(team_data.model_dump())
    info_with_owner = TeamCreate(owner_id=logged_user.id, **team_data.model_dump())
    print(info_with_owner)
    team = TeamController.create_team(info=info_with_owner, session=session, owner_id=logged_user.id)
    return team
