"""Pydantic schemas for user and onboarding endpoints."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    """Request body for creating a new user."""
    user_id: str = Field(..., description="Client-generated UUID for the user")


class UserResponse(BaseModel):
    """Response body for user information."""
    id: str
    created_at: datetime
    updated_at: datetime
    onboarding_completed: bool

    class Config:
        from_attributes = True


class OnboardingRequest(BaseModel):
    """Request body for onboarding submission."""
    user_id: str = Field(..., description="User ID")
    education_level: str = Field(
        ...,
        description="Education level",
        pattern="^(high_school|undergraduate|graduate|professional)$"
    )
    programming_experience: str = Field(
        ...,
        description="Programming experience level",
        pattern="^(none|beginner|intermediate|advanced)$"
    )
    robotics_background: bool = Field(..., description="Has robotics experience")
    ai_ml_experience: str = Field(
        ...,
        description="AI/ML experience level",
        pattern="^(none|basic|intermediate|advanced)$"
    )
    learning_goals: list[str] = Field(
        ...,
        description="Learning goals (multi-select)",
        min_length=1
    )
    preferred_language: str = Field(
        default="en",
        description="Preferred language",
        pattern="^(en|ur)$"
    )


class UserPreferencesResponse(BaseModel):
    """Response body for user preferences."""
    id: str
    user_id: str
    education_level: str
    programming_experience: str
    robotics_background: bool
    ai_ml_experience: str
    learning_goals: list[str]
    preferred_language: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UpdatePreferencesRequest(BaseModel):
    """Request body for updating preferences."""
    education_level: Optional[str] = Field(
        default=None,
        pattern="^(high_school|undergraduate|graduate|professional)$"
    )
    programming_experience: Optional[str] = Field(
        default=None,
        pattern="^(none|beginner|intermediate|advanced)$"
    )
    robotics_background: Optional[bool] = None
    ai_ml_experience: Optional[str] = Field(
        default=None,
        pattern="^(none|basic|intermediate|advanced)$"
    )
    learning_goals: Optional[list[str]] = None
    preferred_language: Optional[str] = Field(
        default=None,
        pattern="^(en|ur)$"
    )


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    message: str
    detail: Optional[dict] = None
