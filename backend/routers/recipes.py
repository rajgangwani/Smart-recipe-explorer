from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import SessionLocal
from .. import models, schemas


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


# ==============================
# Database Dependency
# ==============================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================
# Create Recipe
# ==============================

@router.post(
    "/",
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


# ==============================
# Get Recipes (With Filtering + Pagination)
# ==============================

@router.get(
    "/",
    response_model=List[schemas.RecipeResponse]
)
def get_recipes(
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    ingredient: Optional[str] = None,
    category: Optional[str] = None,
    max_time: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Recipe)

    if name:
        query = query.filter(models.Recipe.name.ilike(f"%{name}%"))

    if ingredient:
        query = query.filter(models.Recipe.ingredients.ilike(f"%{ingredient}%"))

    if category:
        query = query.filter(models.Recipe.category.ilike(f"%{category}%"))

    if max_time:
        query = query.filter(models.Recipe.cooking_time <= max_time)

    return query.offset(skip).limit(limit).all()


# ==============================
# Get Single Recipe
# ==============================

@router.get(
    "/{recipe_id}",
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


# ==============================
# Update Recipe
# ==============================

@router.put(
    "/{recipe_id}",
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


# ==============================
# Delete Recipe
# ==============================

@router.delete(
    "/{recipe_id}",
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