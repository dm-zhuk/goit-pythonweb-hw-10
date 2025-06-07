from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema for all schemas in the project."""

    __abstract__ = True

    model_config = ConfigDict(extra="forbid")  # 'allow', 'ignore', 'forbid'
