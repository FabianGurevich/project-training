from sqlalchemy import Column, ForeignKey, Table

from src.api.v1.core.database import SQLBase


team_player_table = Table(
    "team_player_table",
    SQLBase.metadata,
    Column("team_id", ForeignKey("team.id"), primary_key=True),
    Column("player_id", ForeignKey("player.id"), primary_key=True),
)
