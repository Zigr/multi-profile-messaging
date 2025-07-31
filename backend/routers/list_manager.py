from fastapi import APIRouter

router = APIRouter()

@router.get("/lists")
def get_lists():
    return []
