"""Initialize our GPT object to make API calls."""

import os
import json
from typing import AsyncGenerator
import tiktoken
import aiohttp
from openai import OpenAI


class OpenAIo4Service:
    """Defines the OpenAI 4o object."""

    def __init__(self):
        self.default_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "o4-mini-2025-04-16"
        self.encoding = tiktoken.get_encoding("o200k_base")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.reasoning_effort = "low"

    def call_o4_api(
        self,
        system_prompt: str,
        data: str,
    ) -> str:
        """
        Makes an API call to OpenAI o4-mini and returns the response.

        Args:
            system_prompt (str): The instruction/system prompt
            data (str): Input string from client

        Returns:
            str: o4-mini's response text
        """

        client = self.default_client

        try:
            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": data},
                ],
                max_completion_tokens=12000,
                reasoning_effort=self.reasoning_effort,
            )

            if completion.choices[0].message.content is None:
                raise ValueError("No content returned from OpenAI o4-mini")

            return completion.choices[0].message.content

        except Exception as e:
            print(f"Error in o4-mini API call {str(e)}")
            raise

    async def call_o4_api_stream(
        self,
        system_prompt: str,
        data: str,
    ) -> AsyncGenerator[str, None]:
        """
        Asynchronously streams a response from the OpenAI o4-mini model using SSE.

        This function sends a system prompt and a user-formatted message to the OpenAI
        Chat Completions API with streaming enabled. It yields incremental chunks of
        the model's response as they arrive.

        Args:
            system_prompt (str): The system-level instructions for the model.
            data (str): Input string from client

        Yields:
            str: Chunks of the model's response text as they are received.

        Raises:
            ValueError: If the API returns a non-200 response or the stream is malformed.
            aiohttp.ClientError: If there's a connection issue with the API.
            Exception: For any unexpected errors during the streaming process.

        Example Usage:
            async for chunk in o4_service.call_o4_api_stream(
                    system_prompt=system_prompt,
                    data=str
                ):
                yield f"data: {json.dumps({'status': 'explanation_chunk', 'chunk': chunk})}"
        """

        api_key = self.api_key

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data},
            ],
            "max_completion_tokens": 12000,
            "stream": True,
            "reasoning_effort": self.reasoning_effort,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url, headers=headers, json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"Error response: {error_text}")
                        raise ValueError(
                            f"OpenAI API returned status code {response.status}: {error_text}"
                        )

                    line_count = 0
                    async for line in response.content:
                        line = line.decode("utf-8").strip()
                        if not line:
                            continue

                        line_count += 1

                        if line.startswith("data: "):
                            if line == "data: [DONE]":
                                break
                            try:
                                data = json.loads(line[6:])
                                content = (
                                    data.get("choices", [{}])[0]
                                    .get("delta", {})
                                    .get("content")
                                )
                                if content:
                                    yield content
                            except json.JSONDecodeError as e:
                                print(f"JSON decode error: {e} for line: {line}")
                                continue

                    if line_count == 0:
                        print("Warning: No lines received in stream response")

        except aiohttp.ClientError as e:
            print(f"Connection error: {str(e)}")
            raise ValueError(f"Failed to connect to OpenAI API: {str(e)}") from e
        except Exception as e:
            print(f"Unexpected error in streaming API call: {str(e)}")
            raise

    def count_tokens(self, prompt: str) -> int:
        """
        Counts the number of tokens in a prompt.

        Args:
            prompt (str): The prompt to count tokens for

        Returns:
            int: Estimated number of input tokens
        """
        num_tokens = len(self.encoding.encode(prompt))
        return num_tokens
