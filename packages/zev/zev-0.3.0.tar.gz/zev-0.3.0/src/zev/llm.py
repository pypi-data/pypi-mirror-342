import openai
import os
from pydantic import BaseModel
from typing import Optional

from zev.constants import DEFAULT_MODEL

class Command(BaseModel):
    command: str
    short_explanation: str


class OptionsResponse(BaseModel):
    commands: list[Command]
    is_valid: bool
    explanation_if_not_valid: Optional[str] = None


PROMPT = """
You are a helpful assistant that helps users remember commands for the terminal. You 
will return a JSON object with a list of at most three options.

The options should be related to the prompt that the user provides (the prompt might
either be desciptive or in the form of a question).

The options should be in the form of a command that can be run in a bash terminal.

If the user prompt is not clear, return an empty list and set is_valid to false, and
provide an explanation of why it is not clear in the explanation_if_not_valid field.

Otherwise, set is_valid to true, leave explanation_if_not_valid empty, and provide the 
commands in the commands field (remember, up to 3 options, and they all must be commands
that can be run in a bash terminal without changing anything). Each command should have
a short explanation of what it does.

Here is some context about the user's environment:

============== 

{context}

============== 

Here is the users prompt:

============== 

{prompt}
"""


def get_client():
    base_url = os.getenv("OPENAI_BASE_URL", default="").strip()
    api_key = os.getenv("OPENAI_API_KEY", default="").strip()
    if not base_url or not api_key:
        raise ValueError("OPENAI_BASE_URL and OPENAI_API_KEY must be set. Try running `zev --setup`.")
    return openai.OpenAI(base_url=base_url, api_key=api_key)


def get_options(prompt: str, context: str) -> OptionsResponse | None:
    client = get_client()
    model = os.getenv("OPENAI_MODEL", default=DEFAULT_MODEL)
    if not model:
        raise ValueError("OPENAI_MODEL must be set. Try running `zev --setup`.")
    try:
        assembled_prompt = PROMPT.format(prompt=prompt, context=context)
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[{"role": "user", "content": assembled_prompt}],
            response_format=OptionsResponse,
        )
        return response.choices[0].message.parsed
    except openai.AuthenticationError as e:
        print("Error: There was an error with your OpenAI API key. You can change it by running `zev --setup`.")
        return
