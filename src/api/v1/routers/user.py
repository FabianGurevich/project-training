
from fastapi import APIRouter

router = APIRouter()


@router.post("", status_code=201)
def signup() -> dict:
    return {"message": "User signed up successfully"}
