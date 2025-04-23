########
########
########
########
######## STREAM
########
########

from typing import Any, Dict, Generator, List, Literal
import os
import base64
import json
import requests
from PIL import Image
from typing import Any, Dict, Generator, List, Union

from pydantic import BaseModel
from npcpy.npc_sysenv import (
    get_system_message,
    compress_image,
    available_chat_models,
    available_reasoning_models,
)

from litellm import completion

try:
    import ollama
except:
    pass
# import litellm
# litellm._turn_on_debug()


def get_ollama_hf_stream(
    messages: List[Dict[str, str]],
    model: str,
    npc: Any = None,
    tools: list = None,
    images: List[Dict[str, str]] = None,
    api_key: str = None,
    api_url: str = None,
    tool_choice: Dict = None,
    **kwargs,
) -> Generator:
    """Streams responses from ollama in HF cases that arent covered yet by litellm"""

    system_message = get_system_message(npc) if npc else "You are a helpful assistant."

    if not messages:
        messages = [{"role": "system", "content": system_message}]

    # Add images if provided
    if images:
        messages[-1]["images"] = [image["file_path"] for image in images]

    # Prepare API call parameters
    api_params = {
        "messages": messages,
        "stream": True,
        "model": model,
    }
    # Add tools if provided
    if tools:
        api_params["tools"] = tools
    # Add tool choice if specified
    if tool_choice:
        api_params["tool_choice"] = tool_choice

    # Add any additional parameters
    for key, value in kwargs.items():
        if key in [
            "stream",
            "stop",
            "temperature",
            "top_p",
            "max_tokens",
            "max_completion_tokens",
            "tools",
            "tool_choice",
            "extra_headers",
            "parallel_tool_calls",
            "response_format",
            "user",
        ]:
            api_params[key] = value
    res = ollama.chat(**api_params)
    for chunk in res:
        yield chunk


def get_litellm_stream(
    messages: List[Dict[str, str]],
    model: str,
    provider: str = None,
    npc: Any = None,
    tools: list = None,
    images: List[Dict[str, str]] = None,
    api_key: str = None,
    api_url: str = None,
    tool_choice: Dict = None,
    **kwargs,
) -> Generator:
    """Streams responses from OpenAI, supporting images, tools and yielding raw text chunks."""
    #print("model", "provider")
    #print(model, provider)
    if "hf.co" in model:
        resp = get_ollama_hf_stream(
            messages,
            model,
            npc=npc,
            tools=tools,
            images=images,
            api_key=api_key,
            api_url=api_url,
            tool_choice=tool_choice,
            **kwargs,
        )
        for chunk in resp:
            yield chunk
    else:
        system_message = (
            get_system_message(npc) if npc else "You are a helpful assistant."
        )

        if not messages:
            messages = [{"role": "system", "content": system_message}]

        # Add images if provided
        if images:
            last_user_message = (
                messages[-1]
                if messages and messages[-1]["role"] == "user"
                else {"role": "user", "content": []}
            )

            if isinstance(last_user_message["content"], str):
                last_user_message["content"] = [
                    {"type": "text", "text": last_user_message["content"]}
                ]

            for image in images:
                with open(image["file_path"], "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("utf-8")
                    last_user_message["content"].append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        }
                    )

            if last_user_message not in messages:
                messages.append(last_user_message)

        api_params = {
            "messages": messages,
            "stream": True,
        }

        if api_key is not None and provider == "openai-like":
            api_params["api_key"] = api_key

        if api_url is not None and provider == "openai-like":
            api_params["api_base"] = api_url
            provider = "openai"

        if provider is not None:
            model_str = f"{provider}/{model}"
        else:
            model_str = model
        api_params["model"] = model_str
        if tools:
            api_params["tools"] = tools

        if tool_choice:
            api_params["tool_choice"] = tool_choice
        if kwargs:
            for key, value in kwargs.items():
                if key in [
                    "stream",
                    "stop",
                    "temperature",
                    "top_p",
                    "max_tokens",
                    "max_completion_tokens",
                    "tools",
                    "tool_choice",
                    "extra_headers",
                    "parallel_tool_calls",
                    "response_format",
                    "user",
                ]:
                    api_params[key] = value
        stream = completion(**api_params)

        for chunk in stream:
            yield chunk


"""
from ollama import chat

stream = chat(
    model='hf.co/caug37/TinyTim:latest',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
"""


def process_litellm_tool_stream(stream, tool_map: Dict[str, callable]) -> List[Dict]:
    """
    Process the litellm tool use stream
    """
    final_tool_calls = {}
    tool_results = []

    for chunk in stream:
        delta = chunk.choices[0].delta

        # Process tool calls if present
        if delta.tool_calls:
            for tool_call in delta.tool_calls:
                index = tool_call.index

                # Initialize tool call if new
                if index not in final_tool_calls:
                    final_tool_calls[index] = {
                        "id": tool_call.id,
                        "name": tool_call.function.name if tool_call.function else None,
                        "arguments": (
                            tool_call.function.arguments if tool_call.function else ""
                        ),
                    }
                # Append arguments if continuing
                elif tool_call.function and tool_call.function.arguments:
                    final_tool_calls[index]["arguments"] += tool_call.function.arguments

    # Process all complete tool calls
    for tool_call in final_tool_calls.values():
        try:
            # Parse the arguments
            tool_input = (
                json.loads(tool_call["arguments"])
                if tool_call["arguments"].strip()
                else {}
            )

            # Execute the tool
            tool_func = tool_map.get(tool_call["name"])
            if tool_func:
                result = tool_func(tool_input)
                tool_results.append(
                    {
                        "tool_name": tool_call["name"],
                        "tool_input": tool_input,
                        "tool_result": result,
                    }
                )
            else:
                tool_results.append(
                    {
                        "tool_name": tool_call["name"],
                        "tool_input": tool_input,
                        "error": f"Tool {tool_call['name']} not found",
                    }
                )

        except Exception as e:
            tool_results.append(
                {
                    "tool_name": tool_call["name"],
                    "tool_input": tool_call["arguments"],
                    "error": str(e),
                }
            )

    return tool_results


def generate_tool_schema(
    name: str,
    description: str,
    parameters: Dict[str, Any],
    required: List[str] = None,
) -> Dict[str, Any]:
    """
    Generate provider-specific function/tool schema from common parameters

    Args:
        name: Name of the function
        description: Description of what the function does
        parameters: Dict of parameter names and their properties
        provider: Which provider to generate schema for
        required: List of required parameter names
    """
    if required is None:
        required = []

    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
                "additionalProperties": False,
            },
            "strict": True,
        },
    }


"""

from npcpy.stream import get_litellm_stream
model = 'hf.co/caug37/TinyTim:latest'
messages = [{'role': 'user', 'content': 'Why is the sky blue?'}]
stream = get_litellm_stream(
    messages=messages,
    model=model,
    provider='hf.co',
    stream=True,
)
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)


"""
