from fastapi import APIRouter

router = APIRouter()

@router.get("/profiles")
def get_profiles():
    return []
