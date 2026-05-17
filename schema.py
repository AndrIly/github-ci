from pydantic import BaseModel, Field, ConfigDict


class RecipeIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Название блюда")
    description: str = Field(..., min_length=1, description="Описание рецепта")
    time_cooking: int = Field(..., ge=1, description='Время приготовления')
    ingredient: str = Field(..., min_length=1, description="Список ингредиентов")


class RecipeOut(RecipeIn):
    id: int = Field(..., description="ID - рецепта")
    count_watch: int = Field(..., ge= 0,description="Количество просмотров")

    model_config = ConfigDict(from_attributes=True)

class RecipeListOut(BaseModel):
    id: int = Field(..., description="ID - рецепта")
    title: str = Field(..., description="Название блюда")
    count_watch: int = Field(..., ge=0, description="Количество просмотров")
    time_cooking: int = Field(..., ge=1, description='Время приготовления')


class RecipeDetailOut(BaseModel):
    id: int = Field(..., description="ID - рецепта")
    title: str = Field(..., description="Название блюда")
    time_cooking: int = Field(..., ge=1, description='Время приготовления')
    ingredient: str = Field(..., min_length=1, description="Список ингредиентов")
    description: str = Field(..., min_length=1, description="Описание рецепта")