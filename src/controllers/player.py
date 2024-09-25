from fastapi import HTTPException
from src.api.v1.schemas.player import PlayerCreate, Player as PlayerSchema
from src.models.player import Player


class PlayerController:

    def create_player(info: PlayerCreate, club_id, session) -> PlayerCreate:
        player_info = PlayerSchema(
            name=info.name, score=info.score, position=info.position, club_id=club_id
        )
        model = player_info.model_dump()
        Player.objects(session).create(model)
        return info

    def get_player(player_id, session) -> Player:
        player = Player.objects(session).get(Player.id == player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
