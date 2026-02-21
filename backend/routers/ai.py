from fastapi import APIRouter, HTTPException, status
from ..schemas import AISuggestionRequest, AISuggestionResponse
from ..services.ai_service import generate_recipe_suggestion

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post(
    "/suggest",
    response_model=AISuggestionResponse,
    status_code=status.HTTP_200_OK
)
def ai_suggest(request: AISuggestionRequest):
    result = generate_recipe_suggestion(request.ingredients)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service unavailable"
        )

    return {"suggestion": result}