"""
Pydantic schemas for FitBuddy.
These validate the shape of data coming in from the HTML forms
before it's passed to the Gemini generator functions / the DB layer.
"""

from pydantic import BaseModel, Field


class UserInput(BaseModel):
    """Data captured from index.html when a user requests a plan."""
    username: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    age: int = Field(..., gt=0, lt=120)
    weight: float = Field(..., gt=0)
    goal: str  # e.g. "weight loss", "muscle gain", "general wellness"
    intensity: str  # "low", "medium", "high"


class FeedbackRequest(BaseModel):
    """Data captured from the feedback form on result.html."""
    user_id: str = Field(..., min_length=1)
    feedback: str = Field(..., min_length=1)
