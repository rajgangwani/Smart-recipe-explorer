from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

import models, schemas
from database import engine, SessionLocal
from services.ai_service import generate_recipe_suggestion


# =========================
# ENVIRONMENT CONFIG
# =========================

ENV = os.getenv("ENV", "development")

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5500"  # fallback for local development
)


# =========================
# INITIALIZATION
# =========================

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Recipe Explorer",
    version="1.0.0",
    docs_url=None if ENV == "production" else "/docs",
    redoc_url=None if ENV == "production" else "/redoc"
)


# =========================
# CORS CONFIGURATION (Production Safe)
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE RECIPE
# =========================

@app.post(
    "/api/v1/recipes",
    response_model=schemas.RecipeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db)
):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


# =========================
# GET RECIPES (Smart Search + Filter + Sort + Pagination)
# =========================

@app.get(
    "/api/v1/recipes",
    response_model=List[schemas.RecipeResponse]
)
def get_recipes(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    category: Optional[str] = None,
    max_time: Optional[int] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Recipe)

    if search:
        query = query.filter(
            (models.Recipe.name.ilike(f"%{search}%")) |
            (models.Recipe.ingredients.ilike(f"%{search}%"))
        )

    if category:
        query = query.filter(
            models.Recipe.category.ilike(f"%{category}%")
        )

    if max_time:
        query = query.filter(
            models.Recipe.cooking_time <= max_time
        )

    if sort_by == "name":
        query = query.order_by(models.Recipe.name.asc())
    elif sort_by == "time":
        query = query.order_by(models.Recipe.cooking_time.asc())

    return query.offset(skip).limit(limit).all()


# =========================
# GET SINGLE RECIPE
# =========================

@app.get(
    "/api/v1/recipes/{recipe_id}",
    response_model=schemas.RecipeResponse
)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    return recipe


# =========================
# UPDATE RECIPE
# =========================

@app.put(
    "/api/v1/recipes/{recipe_id}",
    response_model=schemas.RecipeResponse
)
def update_recipe(
    recipe_id: int,
    updated_recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    for key, value in updated_recipe.dict().items():
        setattr(recipe, key, value)

    db.commit()
    db.refresh(recipe)

    return recipe


# =========================
# DELETE RECIPE
# =========================

@app.delete(
    "/api/v1/recipes/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    db.delete(recipe)
    db.commit()

    return


# =========================
# AI ENDPOINT
# =========================

@app.post(
    "/api/v1/ai/suggest",
    response_model=schemas.AISuggestionResponse
)
def ai_suggest(
    request: schemas.AISuggestionRequest
):
    result = generate_recipe_suggestion(request.ingredients)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service unavailable"
        )

    return {"suggestion": result}


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {"status": "healthy"}
