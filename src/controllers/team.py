from sqlalchemy import UUID
from src.api.v1.core.database import Session
from src.models.team import Team
from src.api.v1.schemas import TeamCreate


class TeamController:
    def create_team(info: TeamCreate, session: Session, owner_id: UUID) -> TeamCreate:
        team_info = info.model_dump()
        team_info["owner_id"] = owner_id
        team = Team.objects(session).create(team_info)
        return team
