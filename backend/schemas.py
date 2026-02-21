from pydantic import BaseModel


# =========================
# RECIPE SCHEMAS
# =========================

class RecipeBase(BaseModel):
    name: str
    ingredients: str
    instructions: str
    category: str
    cooking_time: int


class RecipeCreate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    id: int

    class Config:
        from_attributes = True  # ✅ Pydantic v2 fix


# =========================
# AI SCHEMAS
# =========================

class AISuggestionRequest(BaseModel):
    ingredients: str


class AISuggestionResponse(BaseModel):
    suggestion: str