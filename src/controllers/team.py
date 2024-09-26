from typing import List
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

    def update_team_score(team_id: UUID, session: Session) -> None:
        team = Team.objects(session).get(Team.id == team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        if team.players is not None:
            team.score = sum([player.score for player in team.players])
            session.commit()
        return None

    def add_player_to_team(
        team_id: UUID, player_id: UUID, owner_id: UUID, session: Session
    ):
        team = TeamController.get_team(team_id, session)
        if team.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="Not owner of team")
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
        TeamController.update_team_score(team_id, session)
        session.commit()
        return team

    def remove_player_from_team(
        team_id: UUID, player_id: UUID, owner_id: UUID, session: Session
    ):
        team = TeamController.get_team(team_id, session)
        if team.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="Not owner of team")
        player_to_remove = PlayerController.get_player(player_id, session)
        if player_to_remove not in team.players:
            raise HTTPException(status_code=400, detail="Player not in team")
        team.players.remove(player_to_remove)
        TeamController.update_team_score(team_id, session)
        session.commit()
        return team

    def get_teams(user_id: UUID, session: Session) -> List[TeamInfo]:
        teams = Team.objects(session).get_all(user_id == Team.owner_id)
        team_to_return = []
        for team in teams:
            players = [player.name for player in team.players]
            team_info = TeamInfo(
                name=team.name,
                description=team.description,
                formation=team.formation,
                score=team.score,
                id=team.id,
                players=players,
            )
            team_to_return.append(team_info)
        return team_to_return

    def delete_team(team_id: UUID, owner_id: UUID, session: Session) -> None:
        team = Team.objects(session).get(Team.id == team_id)
        if team.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="Not owner of team")
        session.delete(team)
        session.commit()
        return None

    def update_team(team_id: UUID, owner_id: UUID, info: TeamCreate, session: Session) -> None:
        team = Team.objects(session).get(Team.id == team_id)
        if team.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="Not owner of team")
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        if info.name:
            team.name = info.name
        if info.description:
            team.description = info.description
        if info.formation:
            team.formation = info.formation
        session.commit()
        return None
