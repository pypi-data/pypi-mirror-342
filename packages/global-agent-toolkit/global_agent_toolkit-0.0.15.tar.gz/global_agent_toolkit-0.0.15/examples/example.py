from gat.generations.models.assistant_message import TextPart
from gat.generations.providers.google.google_generation_provider import (
    GenerationConfig,
    GoogleGenerationProvider,
    UserMessage,
)
from dotenv import load_dotenv
import pprint

from pydantic import BaseModel

load_dotenv()


class DangerousDogsResponse(BaseModel):
    dangerous_dogs: list[str]


provider = GoogleGenerationProvider(
    use_vertex_ai=False,
)

generation = provider.create_generation(
    model="gemini-1.5-flash",
    messages=[
        UserMessage(
            parts=[
                TextPart(text="Hello, how are you?"),
                TextPart(text="What are the most dangerous dogs in the world?"),
            ]
        )
    ],
    response_schema=DangerousDogsResponse,
    generation_config=GenerationConfig(timeout=10),
)

pprint.pprint(generation)
