from pydantic import BaseModel, Field


class ChatbotOutput(BaseModel):
    """Structured response returned by the Qdrant chatbot."""

    answer: str = Field(description="A clear answer grounded in the prospectus.")
    sources: list[str] = Field(
        default_factory=list,
        description="PDF filename and page citations used in the answer.",
    )
    information_available: bool = Field(
        description="Whether the prospectus contained enough information."
    )
