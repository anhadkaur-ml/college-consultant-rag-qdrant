"""Gemini models used for embeddings and agent responses."""

from langchain_google_genai import ChatGoogleGenerativeAI

from config import Settings, settings


def create_chat_model(
    config: Settings = settings,
) -> ChatGoogleGenerativeAI:
    config.validate(require_google=True)
    return ChatGoogleGenerativeAI(
        model=config.chat_model,
        google_api_key=config.google_api_key,
    )
