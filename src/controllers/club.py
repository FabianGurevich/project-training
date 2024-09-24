from src.api.v1.schemas.club import CreateClub
from src.models.club import Club


class ClubController:
    def create_club(club_info: CreateClub, session) -> CreateClub:
        club = Club.objects(session).create(club_info.model_dump())
        return club
