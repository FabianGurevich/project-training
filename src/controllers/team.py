from fastapi import HTTPException
from sqlalchemy import UUID
from src.api.v1.core.database import Session
from src.api.v1.schemas.team import TeamInfo
from src.controllers.player import PlayerController
from src.api.v1.schemas import TeamCreate
from src.models.team import Team


class TeamController:
    def create_team(info: TeamCreate, session: Session, owner_id: UUID) -> TeamCreate:
        team_info = info.model_dump()
        team_info["owner_id"] = owner_id
        team = Team.objects(session).create(team_info)
        return team

    def get_team(team_id: UUID, session: Session) -> TeamInfo:
        team = Team.objects(session).get(Team.id == team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team

    def add_player_to_team(team_id: UUID, player_id: UUID, session: Session):
        team = TeamController.get_team(team_id, session)
        player_to_add = PlayerController.get_player(player_id, session)
        count = 0
        for player in team.players:
            if player_to_add.club_id == player.club_id:
                count += 1
                if count >= 3:
                    raise HTTPException(
                        status_code=400, detail="Max players from same club"
                    )
                    break
        if player_to_add in team.players:
            raise HTTPException(status_code=400, detail="Player already in team")
        team.players.append(player_to_add)
        team.score += player_to_add.score
        session.commit()
        return team
