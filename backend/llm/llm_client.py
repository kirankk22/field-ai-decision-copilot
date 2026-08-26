import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class LLMClient:

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:

        self.api_key = os.getenv(
            "GROQ_API_KEY"
        )

        self.model_name = (
            model_name
            or os.getenv("GROQ_MODEL")
            or "openai/gpt-oss-120b"
        )

        if not self.api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=self.api_key
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        try:

            response = (
                self.client
                .chat
                .completions
                .create(
                    model=self.model_name,

                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],

                    temperature=0.1,
                )
            )

        except Exception as exc:

            raise RuntimeError(
                f"Groq LLM request failed: {exc}"
            ) from exc

        if not response.choices:
            raise RuntimeError(
                "Groq returned no choices."
            )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        if not answer:
            raise RuntimeError(
                "Groq returned an empty response."
            )

        return answer.strip()