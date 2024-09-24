from fastapi import APIRouter

from src.api.v1.routers import user, team, player, club

v1_router = APIRouter()
v1_router.include_router(user.router, prefix="/users", tags=["Users"])
v1_router.include_router(team.router, prefix="/teams", tags=["Teams"])
v1_router.include_router(player.router, prefix="/players", tags=["Players"])
v1_router.include_router(club.router, prefix="/clubs", tags=["Clubs"])
