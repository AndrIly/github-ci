from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from database import engine, async_session, Base
import models
import schema
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@app.get("/recipes", response_model = List[schema.RecipeListOut],
         summary="Список рецептов")
async def get_recipes(session: AsyncSession = Depends(get_session)) -> List[dict[str, str | int]]:
    res = await session.execute(select(models.Recipes.id,
                                       models.Recipes.title,
                                       models.Recipes.time_cooking,
                                       models.Recipes.ingredient,
                                       models.Recipes.description,
                                       models.Recipes.count_watch,
                                       )
                                .order_by(
                            models.Recipes.count_watch.desc(),
                    models.Recipes.time_cooking.asc(),))
    result = res.all()

    return [
        {"id": r.id,
         "title": r.title,
         "time_cooking": r.time_cooking,
         "count_watch": r.count_watch,
         }
        for r in result
    ]


@app.post("/recipes", response_model=schema.RecipeOut,
          summary="Создать новый рецепт")
async def create_recipe(recipe: schema.RecipeIn, session: AsyncSession = Depends(get_session)) -> models.Recipes:
    new_recipe = models.Recipes(
        title=recipe.title,
        count_watch=0,
        description=recipe.description,
        time_cooking=recipe.time_cooking,
        ingredient=recipe.ingredient,
    )
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)
    return new_recipe


@app.get("/recipes/{id}", response_model=schema.RecipeDetailOut,
         summary="Детальная информация про рецепт")
async def get_recipe(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, str | int]:
    result = await session.execute(
        select(models.Recipes).where(models.Recipes.id == id)
    )
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe.count_watch += 1
    await session.commit()
    await session.refresh(recipe)

    return {
        "id": recipe.id,
        "title": recipe.title,
        "time_cooking": recipe.time_cooking,
        "ingredient": recipe.ingredient,
        "description": recipe.description,
    }
