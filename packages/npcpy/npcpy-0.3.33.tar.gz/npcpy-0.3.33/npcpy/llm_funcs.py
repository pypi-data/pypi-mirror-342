import subprocess
import requests
import os
import json
import PIL

import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional, Union, Generator


from jinja2 import Environment, FileSystemLoader, Template, Undefined

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from npcpy.npc_sysenv import (
    get_system_message,
    get_available_models,
    get_model_and_provider,
    lookup_provider,
    NPCSH_CHAT_PROVIDER,
    NPCSH_CHAT_MODEL,
    NPCSH_API_URL,
    EMBEDDINGS_DB_PATH,
    NPCSH_EMBEDDING_MODEL,
    NPCSH_EMBEDDING_PROVIDER,
    NPCSH_DEFAULT_MODE,
    NPCSH_REASONING_MODEL,
    NPCSH_REASONING_PROVIDER,
    NPCSH_IMAGE_GEN_MODEL,
    NPCSH_IMAGE_GEN_PROVIDER,
    NPCSH_VIDEO_GEN_MODEL,
    NPCSH_VIDEO_GEN_PROVIDER,
    NPCSH_VISION_MODEL,
    NPCSH_VISION_PROVIDER,
    available_reasoning_models,
    available_chat_models,
)

from npcpy.stream import get_litellm_stream
from npcpy.conversation import (
    get_litellm_conversation,
)
from npcpy.response import (
    get_litellm_response,
)
from npcpy.image_gen import (
    generate_image_litellm,
)
from npcpy.video_gen import (
    generate_video_diffusers,
)

from npcpy.embeddings import (
    get_ollama_embeddings,
    get_openai_embeddings,
    get_anthropic_embeddings,
    store_embeddings_for_model,
)

import asyncio
import sys
from queue import Queue
from threading import Thread
import select


def generate_image(
    prompt: str,
    model: str = NPCSH_IMAGE_GEN_MODEL,
    provider: str = NPCSH_IMAGE_GEN_PROVIDER,
    filename: str = None,
    npc: Any = None,
    height: int = 256,
    width: int = 256,
):
    """This function generates an image using the specified provider and model.
    Args:
        prompt (str): The prompt for generating the image.
    Keyword Args:
        model (str): The model to use for generating the image.
        provider (str): The provider to use for generating the image.
        filename (str): The filename to save the image to.
        npc (Any): The NPC object.
    Returns:
        str: The filename of the saved image.
    """
    if model is not None and provider is not None:
        pass
    elif model is not None and provider is None:
        provider = lookup_provider(model)
    elif npc is not None:
        if npc.provider is not None:
            provider = npc.provider
        if npc.model is not None:
            model = npc.model
        if npc.api_url is not None:
            api_url = npc.api_url
    if filename is None:
        # Generate a filename based on the prompt and the date time
        os.makedirs(os.path.expanduser("~/.npcsh/images/"), exist_ok=True)
        filename = (
            os.path.expanduser("~/.npcsh/images/")
            + f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
    image = generate_image_litellm(
        prompt=prompt,
        model=model,
        provider=provider,
        height=height,
        width=width,
    )
    # save image
    # check if image is a PIL image
    if isinstance(image, PIL.Image.Image):
        image.save(filename)
        return filename

    else:
        try:
            # image is at a private url
            response = requests.get(image.data[0].url)
            with open(filename, "wb") as file:
                file.write(response.content)
            from PIL import Image

            img = Image.open(filename)
            img.show()
            # console = Console()
            # console.print(Image.from_path(filename))
            return filename

        except AttributeError as e:
            print(f"Error saving image: {e}")


def get_embeddings(
    texts: List[str],
    model: str = NPCSH_EMBEDDING_MODEL,
    provider: str = NPCSH_EMBEDDING_PROVIDER,
) -> List[List[float]]:
    """Generate embeddings using the specified provider and store them in Chroma."""
    if provider == "ollama":
        embeddings = get_ollama_embeddings(texts, model)
    elif provider == "openai":
        embeddings = get_openai_embeddings(texts, model)
    elif provider == "anthropic":
        embeddings = get_anthropic_embeddings(texts, model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    # Store the embeddings in the relevant Chroma collection
    # store_embeddings_for_model(texts, embeddings, model, provider)
    return embeddings


def get_llm_response(
    prompt: str,
    provider: str = NPCSH_CHAT_PROVIDER,
    model: str = NPCSH_CHAT_MODEL,
    images: List[Dict[str, str]] = None,
    npc: Any = None,
    team: Any = None,
    messages: List[Dict[str, str]] = None,
    api_url: str = NPCSH_API_URL,
    api_key: str = None,
    context=None,
    **kwargs,
):
    """This function generates a response using the specified provider and model.
    Args:
        prompt (str): The prompt for generating the response.
    Keyword Args:
        provider (str): The provider to use for generating the response.
        model (str): The model to use for generating the response.
        images (List[Dict[str, str]]): The list of images.
        npc (Any): The NPC object.
        messages (List[Dict[str, str]]): The list of messages.
        api_url (str): The URL of the API endpoint.
    Returns:
        Any: The response generated by the specified provider and model.
    """

    # print(provider, model)
    # print(provider, model)

    response = get_litellm_response(
        prompt,
        model=model,
        provider=provider,
        npc=npc,
        team=team,
        api_url=api_url,
        api_key=api_key,
        images=images,        
        context=context,
        **kwargs,
    )
    return response


def get_stream(
    messages: List[Dict[str, str]],
    provider: str = NPCSH_CHAT_PROVIDER,
    model: str = NPCSH_CHAT_MODEL,
    npc: Any = None,
    team: Any = None,
    images: List[Dict[str, str]] = None,
    api_url: str = NPCSH_API_URL,
    api_key: str = None,
    context=None,
    **kwargs,
) -> List[Dict[str, str]]:
    """This function generates a streaming response using the specified provider and model
    Args:
        messages (List[Dict[str, str]]): The list of messages in the conversation.
    Keyword Args:
        provider (str): The provider to use for the conversation.
        model (str): The model to use for the conversation.
        npc (Any): The NPC object.
        api_url (str): The URL of the API endpoint.
        api_key (str): The API key for accessing the API.
    Returns:
        List[Dict[str, str]]: The list of messages in the conversation.
    """
    if model is not None and provider is not None:
        pass
    elif model is not None and provider is None:
        provider = lookup_provider(model)
    elif npc is not None:
        if npc.provider is not None:
            provider = npc.provider
        if npc.model is not None:
            model = npc.model
        if npc.api_url is not None:
            api_url = npc.api_url
    else:
        provider = "ollama"
        model = "llama3.2"

    return get_litellm_stream(
        messages,
        model=model,
        provider=provider,
        npc=npc,
        team=team,
        api_url=api_url,
        api_key=api_key,
        images=images,
        context=context,
        **kwargs,
    )


def generate_video(
    prompt,
    model: str = NPCSH_VIDEO_GEN_MODEL,
    provider: str = NPCSH_VIDEO_GEN_PROVIDER,
    npc: Any = None,
    device: str = "cpu",
    output_path="",
    num_inference_steps=10,
    num_frames=10,
    height=256,
    width=256,
    messages: list = None,
):
    """
    Function Description:
        This function generates a video using the Stable Diffusion API.
    Args:
        prompt (str): The prompt for generating the video.
        model_id (str): The Hugging Face model ID to use for Stable Diffusion.
        device (str): The device to run the model on ('cpu' or 'cuda').
    Returns:
        PIL.Image: The generated image.
    """
    output_path = generate_video_diffusers(
        prompt,
        model,
        npc=npc,
        device=device,
        output_path=output_path,
        num_inference_steps=num_inference_steps,
        num_frames=num_frames,
        height=height,
        width=width,
    )
    if provider == "diffusers":
        return {"output": "output path at " + output_path, "messages": messages}


def get_conversation(
    messages: List[Dict[str, str]],
    provider: str = NPCSH_CHAT_PROVIDER,
    model: str = NPCSH_CHAT_MODEL,
    images: List[Dict[str, str]] = None,
    npc: Any = None,
    api_url: str = NPCSH_API_URL,
    context=None,
    **kwargs,
) -> List[Dict[str, str]]:
    """This function generates a conversation using the specified provider and model.
    Args:
        messages (List[Dict[str, str]]): The list of messages in the conversation.
    Keyword Args:
        provider (str): The provider to use for the conversation.
        model (str): The model to use for the conversation.
        npc (Any): The NPC object.
    Returns:
        List[Dict[str, str]]: The list of messages in the conversation.
    """
    if model is not None and provider is not None:
        pass  # Use explicitly provided model and provider
    elif model is not None and provider is None:
        provider = lookup_provider(model)
    elif npc is not None and (npc.provider is not None or npc.model is not None):
        provider = npc.provider if npc.provider else provider
        model = npc.model if npc.model else model
        api_url = npc.api_url if npc.api_url else api_url
    else:
        provider = "ollama"
        model = "llava:7b" if images is not None else "llama3.2"

    return get_litellm_conversation(
        messages,
        model=model,
        provider=provider,
        npc=npc,
        api_url=api_url,
        images=images,
        context=context,
        **kwargs,
    )

def execute_llm_question(
    command: str,
    model: str = NPCSH_CHAT_MODEL,
    provider: str = NPCSH_CHAT_PROVIDER,
    api_url: str = NPCSH_API_URL,
    api_key: str = None,
    npc: Any = None,
    messages: List[Dict[str, str]] = None,
    stream: bool = False,
    images: List[Dict[str, str]] = None,
    context=None,
):
    if messages is None or len(messages) == 0:
        messages = []
        messages.append({"role": "user", "content": command})

    if stream:
        # print("beginning stream")
        response = get_stream(
            messages,
            model=model,
            provider=provider,
            npc=npc,
            images=images,
            api_url=api_url,
            api_key=api_key,
            context=context,
        )
        return {'messages': messages, 'output':response}
    else:
        response = get_conversation(
            messages,
            model=model,
            provider=provider,
            npc=npc,
            images=images,
            api_url=api_url,
            api_key=api_key,
        )
    if isinstance(response, str) and "Error" in response:
        output = response
    elif isinstance(response, list) and len(response) > 0:
        messages = response  
        output = response[-1]["content"]
    else:
        output = "Error: Invalid response from conversation function"
    return {"messages": messages, "output": output}


def execute_llm_command(
    command: str,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    api_url: str = NPCSH_API_URL,
    api_key: str = None,
    npc: Optional[Any] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    stream=False,
    context=None,
) -> str:
    """This function executes an LLM command.
    Args:
        command (str): The command to execute.

    Keyword Args:
        model (Optional[str]): The model to use for executing the command.
        provider (Optional[str]): The provider to use for executing the command.
        npc (Optional[Any]): The NPC object.
        messages (Optional[List[Dict[str, str]]): The list of messages.
    Returns:
        str: The result of the LLM command.
    """

    max_attempts = 5
    attempt = 0
    subcommands = []
    npc_name = npc.name if npc else "sibiji"
    location = os.getcwd()
    print(f"{npc_name} generating command")
    # Create context from retrieved documents
    context = ""
    while attempt < max_attempts:
        prompt = f"""
        A user submitted this query: {command}.
        You need to generate a bash command that will accomplish the user's intent.
        Respond ONLY with the command that should be executed.
        in the json key "bash_command".
        You must reply with valid json and nothing else. Do not include markdown formatting
        """
        if len(context) > 0:
            prompt += f"""
            What follows is the context of the text files in the user's directory that are potentially relevant to their request
            Use these to help inform your decision.
            {context}
            """
        if len(messages) > 0:
            prompt += f"""
            The following messages have been exchanged between the user and the assistant:
            {messages}
            """

        response = get_llm_response(
            prompt,
            model=model,
            provider=provider,
            api_url=api_url,
            api_key=api_key,
            messages=[],
            npc=npc,
            format="json",
            context=context,
        )

        llm_response = response.get("response", {})
        # messages.append({"role": "assistant", "content": llm_response})
        # print(f"LLM response type: {type(llm_response)}")
        # print(f"LLM response: {llm_response}")

        try:
            if isinstance(llm_response, str):
                llm_response = json.loads(llm_response)

            if isinstance(llm_response, dict) and "bash_command" in llm_response:
                bash_command = llm_response["bash_command"]
            else:
                raise ValueError("Invalid response format from LLM")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing LLM response: {e}")
            attempt += 1
            continue

        print(f"LLM suggests the following bash command: {bash_command}")
        subcommands.append(bash_command)

        try:
            print(f"Running command: {bash_command}")
            result = subprocess.run(
                bash_command, shell=True, text=True, capture_output=True, check=True
            )
            print(f"Command executed with output: {result.stdout}")

            prompt = f"""
                Here was the output of the result for the {command} inquiry
                which ran this bash command {bash_command}:

                {result.stdout}

                Provide a simple response to the user that explains to them
                what you did and how it accomplishes what they asked for.
                """
            if len(context) > 0:
                prompt += f"""
                What follows is the context of the text files in the user's directory that are potentially relevant to their request
                Use these to help inform how you respond.
                You must read the context and use it to provide the user with a more helpful answer related to their specific text data.

                CONTEXT:

                {context}
                """
            messages.append({"role": "user", "content": prompt})
            # print(messages, stream)
            if stream:
                response = get_stream(
                    messages,
                    model=model,
                    provider=provider,
                    api_url=api_url,
                    api_key=api_key,
                    npc=npc,
                )
                return response

            else:
                response = get_llm_response(
                    prompt,
                    model=model,
                    provider=provider,
                    api_url=api_url,
                    api_key=api_key,
                    npc=npc,
                    messages=messages,
                    context=context,
                )
            output = response.get("response", "")

            # render_markdown(output)

            return {"messages": messages, "output": output}
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error:")
            print(e.stderr)

            error_prompt = f"""
            The command '{bash_command}' failed with the following error:
            {e.stderr}
            Please suggest a fix or an alternative command.
            Respond with a JSON object containing the key "bash_command" with the suggested command.
            Do not include any additional markdown formatting.

            """

            if len(context) > 0:
                error_prompt += f"""
                    What follows is the context of the text files in the user's directory that are potentially relevant to their request
                    Use these to help inform your decision.
                    {context}
                    """

            fix_suggestion = get_llm_response(
                error_prompt,
                model=model,
                provider=provider,
                npc=npc,
                api_url=api_url,
                api_key=api_key,
                format="json",
                messages=messages,
                context=context,
            )

            fix_suggestion_response = fix_suggestion.get("response", {})

            try:
                if isinstance(fix_suggestion_response, str):
                    fix_suggestion_response = json.loads(fix_suggestion_response)

                if (
                    isinstance(fix_suggestion_response, dict)
                    and "bash_command" in fix_suggestion_response
                ):
                    print(
                        f"LLM suggests fix: {fix_suggestion_response['bash_command']}"
                    )
                    command = fix_suggestion_response["bash_command"]
                else:
                    raise ValueError(
                        "Invalid response format from LLM for fix suggestion"
                    )
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing LLM fix suggestion: {e}")

        attempt += 1

    return {
        "messages": messages,
        "output": "Max attempts reached. Unable to execute the command successfully.",
    }


def decide_plan(
    command: str,
    possible_actions: Dict[str, str],
    responder = None,
    messages: Optional[List[Dict[str, str]]] = None, 
    model: Optional[str] = None,
    provider: Optional[str] = None,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Gets a plan by asking LLM to choose from possible_actions.
    Prompt includes only command, actions, and potential delegation targets (if responder is Team).
    Relies on get_llm_response to handle all other context via the passed npc object.

    Args:
        command: User input.
        possible_actions: Dictionary of valid action names and descriptions.
        responder: The NPC or Team object, or None.
        messages: Conversation history (passed to get_llm_response).
        model, provider, api_url, api_key: LLM configuration overrides.

    Returns:
        Plan dictionary: {"chosen_action":..., "parameters":..., "explanation":..., "error":...}.
    """
    if not possible_actions:
        return {"error": "No possible actions provided."}


    prompt = f"User Request: \"{command}\"\n\n"
    prompt += "## Possible Actions:\nChoose ONE action:\n"
    for name, desc in possible_actions.items():
        prompt += f"- {name}: {desc}\n"

    # Add delegation targets ONLY if responder is a Team    
    if hasattr(responder, 'npcs'):
        foreman = decision_npc_obj # Already fetched
        entities = []
        for name, npc_obj in responder.npcs.items():
             if npc_obj != foreman: # Don't list the foreman itself
                 entities.append(f"- {name} (NPC)")
        for name, team_obj in responder.sub_teams.items():
             entities.append(f"- {name} (Team)")
        if entities:
            prompt += "\n### Potential Delegation Targets:\n" + "\n".join(entities) + "\n"

    # Instructions for LLM
    prompt += """
# Instructions:
1. Select the single most appropriate action from 'Possible Actions'.
2. Determine parameters identifying the action's target (e.g., 'tool_name', 'target_entity'). DO NOT determine tool arguments.
3. Explain reasoning.

# Required Output Format (JSON Only, NO MARKDOWN):
{
  "chosen_action": "action_name",
  "parameters": { /* "tool_name": "...", "target_entity": "..." */ },
  "explanation": "Your reasoning."
}
"""

    # --- 3. Call LLM ---
    # Pass decision_npc_obj - get_llm_response handles its context (directive etc.)
    llm_response = get_llm_response(
        prompt=prompt,
        model=effective_model,
        provider=effective_provider,
        api_url=effective_api_url,
        api_key=effective_api_key,
        npc=decision_npc_obj, # Pass the relevant NPC/Foreman object or None
        format="json",
        messages=messages # Pass history if get_llm_response uses it
    )

    # --- 4. Parse and Validate ---
    plan = {"error": None}
    if "error" in llm_response or "Error" in llm_response:
        plan["error"] = f"LLM Error: {llm_response.get('error', llm_response.get('Error'))}"
        print(plan["error"])
        return plan

    response_content = llm_response.get("response", {})
    parsed_json = None
    try:
        if isinstance(response_content, str): parsed_json = json.loads(response_content.strip())
        elif isinstance(response_content, dict): parsed_json = response_content
        else: raise TypeError("Response is not str or dict")

        if not all(k in parsed_json for k in ["chosen_action", "parameters", "explanation"]) or \
           not isinstance(parsed_json.get("parameters"), dict) or \
           not isinstance(parsed_json.get("chosen_action"), str) or \
           not parsed_json.get("chosen_action"):
            raise ValueError("LLM plan has invalid structure or missing keys.")

        chosen_action = parsed_json["chosen_action"]
        if chosen_action not in possible_actions:
            raise ValueError(f"LLM chose an invalid action '{chosen_action}'. Valid: {list(possible_actions.keys())}")

        plan["chosen_action"] = chosen_action
        plan["parameters"] = parsed_json.get("parameters", {})
        plan["explanation"] = parsed_json.get("explanation", "")

    except (json.JSONDecodeError, TypeError, ValueError) as e:
        plan["error"] = f"LLM plan processing error: {e}. Response: {str(response_content)[:200]}..."
        print(plan["error"])
        return plan


    print(f"Plan Determined: Action='{plan['chosen_action']}', Params='{plan['parameters']}'")
    return plan
def check_llm_command(
    command: str,
    model: str = NPCSH_CHAT_MODEL,
    provider: str = NPCSH_CHAT_PROVIDER,
    reasoning_model: str = NPCSH_REASONING_MODEL,
    reasoning_provider: str = NPCSH_REASONING_PROVIDER,
    api_url: str = NPCSH_API_URL,
    api_key: str = None,
    npc: Any = None,
    team: Any = None,
    messages: List[Dict[str, str]] = None,
    images: list = None,
    stream=False,
    context=None,
    synthesize=False,
    human_in_the_loop=False,
):
    """This function checks an LLM command.
    Args:
        command (str): The command to check.
    Keyword Args:
        model (str): The model to use for checking the command.
        provider (str): The provider to use for checking the command.
        npc (Any): The NPC object.
        n_docs (int): The number of documents.
    Returns:
        Any: The result of checking the LLM command.
    """

    ENTER_REASONING_FLOW = False
    if NPCSH_DEFAULT_MODE == "reasoning":
        ENTER_REASONING_FLOW = True
    if model in available_reasoning_models:
        print(
            """
Model provided is a reasoning model, defaulting to non reasoning model for
ReAct choices then will enter reasoning flow
            """
        )
        reasoning_model = model
        reasoning_provider = provider

        model = NPCSH_CHAT_MODEL
        provider = NPCSH_CHAT_PROVIDER
    if messages is None:
        messages = []

    prompt = f"""
    A user submitted this query: {command}

    Determine the nature of the user's request:

    1. Should a tool be invoked to fulfill the request?

    2. Is it a general question that requires an informative answer or a highly specific question that
        requires inforrmation on the web?

    3. Would this question be best answered by an alternative NPC?

    4. Is it a complex request that actually requires more than one
        tool to be called, perhaps in a sequence?
        Sequences should only be used for more than one consecutive tool call. Do not invoke sequences for single tool calls.


    """
    if human_in_the_loop:

        prompt+= f"""
            5. is there a high amount of ambiguity in the user's request?  If so, ask the user for more information.
            
            in your response, consider as well the following guidelines for whether to request input:
            
                Here are some examples of ambiguous and non-ambiguous requests:

                For exmaple,
                    "tell me a joke about my favorite city" is ambiguous because the user
                    did not specify the city. In this case, ask the user for more information.

                    "tell me a joke about the weather" is not ambiguous because the user
                    specified the topic of the joke. In this case, you can answer the question
                    without asking for more information.

                    "take a screenshot of my screen" is not ambiguous because the user
                    specified the action they want to take. In this case, you can carry out the action without asking for more information.

                    ambiguous: "whats happening tonight in my city" is ambiguous because the user 
                    did not specify the city. In this case, ask the user for more information.
                    not ambiguous: "whats happening tonight in new york" is not ambiguous because the user
                    specified the city. In this case, you can answer the question without asking for more information.
                        
                Please limit requests for input to only the most ambiguous requests to ensure the optimal user experience.
            
            """
        

    if npc is not None:
        if npc.shared_context:
            prompt += f"""
            Relevant shared context for the npc:
            {npc.shared_context}
            """

        if npc.tools_dict is None :
            prompt += "No tools available. Do not invoke tools."
        else:
            prompt += "Available tools: \n"
            tools_set = {}
            if npc.tools_dict is not None:
                for tool_name, tool in npc.tools_dict.items():
                    if tool_name not in tools_set:
                        tools_set[tool_name] = tool.description
            for tool_name, tool_description in tools_set.items():
                prompt += f"""
                            {tool_name} : {tool_description} \n

                            """
    if team is None:
        prompt += "No NPCs available for alternative answers."
    else:
        prompt += f"""
        Available NPCs for alternative answers:

            {team.npcs}
        """
        if team.context:
            prompt += f"""
            Relevant shared context for the team:
            {team.context}
            """


    action_space = ["invoke_tool", "answer_question", "pass_to_npc", "execute_sequence", ]
    if human_in_the_loop:
        action_space.append("request_input")
    prompt += f"""
    In considering how to answer this, consider:

    - Whether a tool should be used.


    Excluding time-sensitive phenomena or ones that require external data inputs /information,
    most general questions can be answered without any extra tools or agent passes.


    Only use tools or pass to other NPCs when it is obvious that the answer needs to be as up-to-date as possible. For example,
        a question about where mount everest is does not necessarily need to be answered by a tool call or an agent pass.
    Similarly, if a user asks to explain the plot of the aeneid, this can be answered without a tool call or agent pass.

    If a user were to ask for the current weather in tokyo or the current price of bitcoin or who the mayor of a city is,
        then a tool call or agent pass may be appropriate.

    Tools are valuable but their use should be limited and purposeful to
        ensure the best user experience.
        If a user asks you to search or to take a screenshot or to open a program or to write a program most likely it is
        appropriate to use a tool.
    Respond with a JSON object containing:
    - "action": one of {action_space}
    - "tool_name": : if action is "invoke_tool": the name of the tool to use.
                     else if action is "execute_sequence", a list of tool names to use.
    - "explanation": a brief explanation of why you chose this action.
    - "npc_name": (if action is "pass_to_npc") the name of the NPC to pass the question , else if action is "execute_sequence", a list of
                    npcs to pass the question to in order.



    Return only the JSON object. Do not include any additional text.

    The format of the JSON object is:
    {{
        "action": "invoke_tool" | "answer_question" | "pass_to_npc" | "execute_sequence" | "request_input",
        "tool_name": "<tool_name(s)_if_applicable>",
        "explanation": "<your_explanation>",
        "npc_name": "<npc_name(s)_if_applicable>"
    }}

    If you execute a sequence, ensure that you have a specified NPC for each tool use.
        question answering is not a tool use.
        "invoke_tool" should never be used in the list of tools when executing a sequence.
    Remember, do not include ANY ADDITIONAL MARKDOWN FORMATTING.
    There should be no leading ```json.
    
        """
    if context:
        prompt += f"""
        Additional relevant context from user:

        {context}

        """


    action_response = get_llm_response(
        prompt,
        model=model,
        provider=provider,
        api_url=api_url,
        api_key=api_key,
        npc=npc,
        format="json",
        messages=[],
        context=None,
    )
    if "Error" in action_response:
        print(f"LLM Error: {action_response['error']}")
        return action_response["error"]

    response_content = action_response.get("response", {})

    if isinstance(response_content, str):
        try:
            response_content_parsed = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(
                f"Invalid JSON received from LLM: {e}. Response was: {response_content}"
            )
            return f"Error: Invalid JSON from LLM: {response_content}"
    else:
        response_content_parsed = response_content

    action = response_content_parsed.get("action")
    explanation = response_content_parsed.get("explanation")

    print(f"action chosen: {action}")
    print(f"explanation given: {explanation}")

    # print(response_content)
    if response_content_parsed.get("tool_name"):
        print(f"tool name: {response_content_parsed.get('tool_name')}")

    if action == "execute_command":

        result = execute_llm_command(
            command,
            model=model,
            provider=provider,
            api_url=api_url,
            api_key=api_key,
            messages=[],
            npc=npc,
            stream=stream,
        )
        if stream:
            return result

        output = result.get("output", "")
        messages = result.get("messages", messages)
        return {"messages": messages, "output": output}

    elif action == "invoke_tool":
        tool_name = response_content_parsed.get("tool_name")
        # print(npc)
        print(f"tool name: {tool_name}")
        result = handle_tool_call(
            command,
            tool_name,
            model=model,
            provider=provider,
            api_url=api_url,
            api_key=api_key,
            messages=messages,
            npc=npc,
            stream=stream,
        )
        if stream:
            return result
        messages = result.get("messages", messages)
        output = result.get("output", "")
        return {"messages": messages, "output": output}

    elif action == "answer_question":
        if ENTER_REASONING_FLOW:
            print("entering reasoning flow")
            result = enter_reasoning_human_in_the_loop(
                messages, reasoning_model, reasoning_provider
            )
        else:
            result = execute_llm_question(
                command,
                model=model,
                provider=provider,
                api_url=api_url,
                api_key=api_key,
                messages=messages,
                npc=npc,
                stream=stream,
                images=images,
            )

        if stream:
            return result
        messages = result.get("messages", messages)
        output = result.get("output", "")
        return {"messages": messages, "output": output}
    elif action == "pass_to_npc":
        npc_to_pass = response_content_parsed.get("npc_name")
        npc_to_pass_obj = None
        print(npc_to_pass)
        agent_passes = []
        if team is not None:
            print(f"team npcs: {team.npcs}")
            match = team.npcs.get(npc_to_pass)
            if match is not None:
                npc_to_pass_obj = match
                print(type(npc_to_pass_obj))
                agent_passes.append(
                    npc.handle_agent_pass(
                        npc_to_pass_obj,
                        command,
                        messages=messages,
                    )
                )
        output = ""
        print(agent_passes)
        for agent_pass in agent_passes:
            output += str(agent_pass.get("response"))
        return {"messages": messages, "output": output}
    elif action == "request_input":
        explanation = response_content_parsed.get("explanation")

        request_input = handle_request_input(
            f"Explanation from check_llm_command:  {explanation} \n for the user input command: {command}",
            model=model,
            provider=provider,
        )
        # pass it back through with the request input added to the end of the messages
        # so that we can re-pass the result through the check_llm_command.

        messages.append(
            {
                "role": "assistant",
                "content": f"""its clear that extra input is required.
                                could you please provide it? Here is the reason:

                                {explanation},

                                and the prompt: {command}""",
            }
        )
        messages.append(
            {
                "role": "user",
                "content": command + " \n \n \n extra context: " + request_input,
            }
        )

        return check_llm_command(
            command + " \n \n \n extra context: " + request_input,
            model=model,
            provider=provider,
            api_url=api_url,
            api_key=api_key,
            npc=npc,
            messages=messages,
            stream=stream,
        )

    elif action == "execute_sequence":
        tool_names = response_content_parsed.get("tool_name")
        npc_names = response_content_parsed.get("npc_name")

        # print(npc_names)
        npcs = []
        # print(tool_names, npc_names)
        if isinstance(npc_names, list):
            if len(npc_names) == 0:
                # if no npcs are specified, just have the npc take care of it itself instead of trying to force it to generate npc names for sequences all the time

                npcs = [npc] * len(tool_names)
            if team is None:
                # try again and append that there are no agents to pass to
                print('')
            for npc_name in npc_names:
                for npc_obj in team.npcs:
                    if npc_name in npc_obj:
                        npcs.append(npc_obj[npc_name])
                        break
                if len(npcs) < len(tool_names):
                    npcs.append(npc)

        output = ""
        results_tool_calls = []
        if synthesize:
            # carry out fact extraction
            print("synthesize not yet implemented")

        if len(tool_names) > 0:
            for npc_obj, tool_name in zip(npcs, tool_names):
                result = handle_tool_call(
                    command,
                    tool_name,
                    model=model,
                    provider=provider,
                    api_url=api_url,
                    api_key=api_key,
                    messages=messages,
                    npc=npc_obj,
                    stream=stream,
                )
                # print(result)
                results_tool_calls.append(result)
                messages = result.get("messages", messages)
                output += result.get("output", "")
                # print(results_tool_calls)
        else:
            print('agent pass')
            for npc_obj in npcs:
                result = npc.handle_agent_pass(
                    npc_obj,
                    command,
                    messages=messages,
                    shared_context=npc.shared_context,
                )

                messages = result.get("messages", messages)
                results_tool_calls.append(result.get("response"))
                # print(messages[-1])
        # import pdb

        # pdb.set_trace()

        return {"messages": messages, "output": output}
    else:
        print("Error: Invalid action in LLM response")
        return "Error: Invalid action in LLM response"


def handle_tool_call(
    command: str,
    tool_name: str,
    model: str = NPCSH_CHAT_MODEL,
    provider: str = NPCSH_CHAT_PROVIDER,
    api_url: str = NPCSH_API_URL,
    api_key: str = None,
    messages: List[Dict[str, str]] = None,
    npc: Any = None,
    stream=False,
    n_attempts=3,
    attempt=0,
    context=None,
) -> Union[str, Dict[str, Any]]:
    """This function handles a tool call.
    Args:
        command (str): The command.
        tool_name (str): The tool name.
    Keyword Args:
        model (str): The model to use for handling the tool call.
        provider (str): The provider to use for handling the tool call.
        messages (List[Dict[str, str]]): The list of messages.
        npc (Any): The NPC object.
    Returns:
        Union[str, Dict[str, Any]]: The result of handling
        the tool call.

    """
    print(npc)
    print("handling tool call")
    print(command)
    if npc is None:
        return f"No tools are available. "
    else:
        if tool_name not in npc.tools_dict:
            print("not available")
            print(f"Tool '{tool_name}' not found in NPC's tools_dict.")
            return f"Tool '{tool_name}' not found."
        elif tool_name in npc.tools_dict:
            tool = npc.tools_dict[tool_name]
        print(f"Tool found: {tool.tool_name}")
        jinja_env = Environment(loader=FileSystemLoader("."), undefined=Undefined)

        prompt = f"""
        The user wants to use the tool '{tool_name}' with the following request:
        '{command}'
        Here is the tool file:
        ```
        {tool.to_dict()}
        ```

        Please determine the required inputs for the tool as a JSON object.
        
        
        They must be exactly as they are named in the tool.
        For example, if the tool has three inputs, you should respond with a list of three values that will pass for those args.
        
        Return only the JSON object without any markdown formatting.

        """

        if npc and hasattr(npc, "shared_context"):
            if npc.shared_context.get("dataframes"):
                context_info = "\nAvailable dataframes:\n"
                for df_name in npc.shared_context["dataframes"].keys():
                    context_info += f"- {df_name}\n"
                prompt += f"""Here is contextual info that may affect your choice: {context_info}
                """
        if context is not None:
            prompt += f"Here is some additional context: {context}"

        # print(prompt)

        # print(
        # print(prompt)
        response = get_llm_response(
            prompt,
            format="json",
            model=model,
            provider=provider,
            api_url=api_url,
            api_key=api_key,
            npc=npc,
        )
        try:
            # Clean the response of markdown formatting
            response_text = response.get("response", "{}")
            if isinstance(response_text, str):
                response_text = (
                    response_text.replace("```json", "").replace("```", "").strip()
                )

            # Parse the cleaned response
            if isinstance(response_text, dict):
                input_values = response_text
            else:
                input_values = json.loads(response_text)
            # print(f"Extracted inputs: {input_values}")
        except json.JSONDecodeError as e:
            print(f"Error decoding input values: {e}. Raw response: {response}")
            return f"Error extracting inputs for tool '{tool_name}'"
        # Input validation (example):
        required_inputs = tool.inputs
        missing_inputs = []
        for inp in required_inputs:
            if not isinstance(inp, dict):
                # dicts contain the keywords so its fine if theyre missing from the inputs.
                if inp not in input_values or input_values[inp] == "":
                    missing_inputs.append(inp)
        if len(missing_inputs) > 0:
            # print(f"Missing required inputs for tool '{tool_name}': {missing_inputs}")
            if attempt < n_attempts:
                print(f"attempt {attempt+1} to generate inputs failed, trying again")
                print("missing inputs", missing_inputs)
                print("llm response", response)
                print("input values", input_values)
                return handle_tool_call(
                    command,
                    tool_name,
                    model=model,
                    provider=provider,
                    messages=messages,
                    npc=npc,
                    api_url=api_url,
                    api_key=api_key,
                    stream=stream,
                    attempt=attempt + 1,
                    n_attempts=n_attempts,
                )
            return {
                "output": f"Missing inputs for tool '{tool_name}': {missing_inputs}",
                "messages": messages,
            }

        # try:
        print("Executing tool with input values:", input_values)

        # try:
        tool_output = tool.execute(
            input_values,
            npc.tools_dict,
            jinja_env,
            command,
            model=model,
            provider=provider,
            npc=npc,
            stream=stream,
            messages=messages,
        )
        if not stream:
            if "Error" in tool_output:
                raise Exception(tool_output)
            # except Exception as e:
            # diagnose_problem = get_llm_response(
            ##    f"""a problem has occurred.
            #                                    Please provide a diagnosis of the problem and a suggested #fix.

            #                                    The tool call failed with this error:
            #                                    {e}
            #                                    Please return a json object containing two fields
            ##                                    -problem
            #                                    -suggested solution.
            #                                    do not include any additional markdown formatting or #leading json tags

            #                                    """,
            #    model=model,
            #    provider=provider,
            #    npc=npc,
            ##    api_url=api_url,
            #    api_ley=api_key,
            #    format="json",
            # )
            # print(e)
            # problem = diagnose_problem.get("response", {}).get("problem")
            # suggested_solution = diagnose_problem.get("response", {}).get(
            #    "suggested_solution"
            # )
            '''
            print(f"An error occurred while executing the tool: {e}")
            print(f"trying again, attempt {attempt+1}")
            if attempt < n_attempts:
                tool_output = handle_tool_call(
                    command,
                    tool_name,
                    model=model,
                    provider=provider,
                    messages=messages,
                    npc=npc,
                    api_url=api_url,
                    api_key=api_key,
                    stream=stream,
                    attempt=attempt + 1,
                    n_attempts=n_attempts,
                    context=f""" \n \n \n "tool failed: {e}  \n \n \n here was the previous attempt: {input_values}""",
                )
            else:
                user_input = input(
                    "the tool execution has failed after three tries, can you add more context to help or would you like to run again?"
                )
                return
            '''
        if stream:
            return tool_output
        # print(f"Tool output: {tool_output}")
        # render_markdown(str(tool_output))
        if messages is not None:  # Check if messages is not None
            messages.append({"role": "assistant", "content": tool_output})
        return {"messages": messages, "output": tool_output}
        # except Exception as e:
        #    print(f"Error executing tool {tool_name}: {e}")
        #    return f"Error executing tool {tool_name}: {e}"


def execute_data_operations(
    query: str,
    dataframes: Dict[str, pd.DataFrame],
    npc: Any = None,
    db_path: str = "~/npcsh_history.db",
):
    """This function executes data operations.
    Args:
        query (str): The query to execute.

        dataframes (Dict[str, pd.DataFrame]): The dictionary of dataframes.
    Keyword Args:
        npc (Any): The NPC object.
        db_path (str): The database path.
    Returns:
        Any: The result of the data operations.
    """

    location = os.getcwd()
    db_path = os.path.expanduser(db_path)

    try:
        try:
            # Create a safe namespace for pandas execution
            namespace = {
                "pd": pd,
                "np": np,
                "plt": plt,
                **dataframes,  # This includes all our loaded dataframes
            }
            # Execute the query
            result = eval(query, namespace)

            # Handle the result
            if isinstance(result, (pd.DataFrame, pd.Series)):
                # render_markdown(result)
                return result, "pd"
            elif isinstance(result, plt.Figure):
                plt.show()
                return result, "pd"
            elif result is not None:
                # render_markdown(result)

                return result, "pd"

        except Exception as exec_error:
            print(f"Pandas Error: {exec_error}")

        # 2. Try SQL
        # print(db_path)
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                print(query)
                print(get_available_tables(db_path))

                cursor.execute(query)
                # get available tables

                result = cursor.fetchall()
                if result:
                    for row in result:
                        print(row)
                    return result, "sql"
        except Exception as e:
            print(f"SQL Error: {e}")

        # 3. Try R
        try:
            result = subprocess.run(
                ["Rscript", "-e", query], capture_output=True, text=True
            )
            if result.returncode == 0:
                print(result.stdout)
                return result.stdout, "r"
            else:
                print(f"R Error: {result.stderr}")
        except Exception as e:
            pass

        # If all engines fail, ask the LLM
        print("Direct execution failed. Asking LLM for SQL query...")
        llm_prompt = f"""
        The user entered the following query which could not be executed directly using pandas, SQL, R, Scala, or PySpark:
        ```
        {query}
        ```

        The available tables in the SQLite database at {db_path} are:
        ```sql
        {get_available_tables(db_path)}
        ```

        Please provide a valid SQL query that accomplishes the user's intent.  If the query requires data from a file, provide instructions on how to load the data into a table first.
        Return only the SQL query, or instructions for loading data followed by the SQL query.
        """

        llm_response = get_llm_response(llm_prompt, npc=npc)

        print(f"LLM suggested SQL: {llm_response}")
        command = llm_response.get("response", "")
        if command == "":
            return "LLM did not provide a valid SQL query.", None
        # Execute the LLM-generated SQL
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(command)
                result = cursor.fetchall()
                if result:
                    for row in result:
                        print(row)
                    return result, "llm"
        except Exception as e:
            print(f"Error executing LLM-generated SQL: {e}")
            return f"Error executing LLM-generated SQL: {e}", None

    except Exception as e:
        print(f"Error executing query: {e}")
        return f"Error executing query: {e}", None


def check_output_sufficient(
    request: str,
    data: pd.DataFrame,
    query: str,
    model: str = None,
    provider: str = None,
    npc: Any = None,
) -> Dict[str, Any]:
    """
    Check if the query results are sufficient to answer the user's request.
    """
    prompt = f"""
    Given:
    - User request: {request}
    - Query executed: {query}
    - Results:
      Summary: {data.describe()}
      data schema: {data.dtypes}
      Sample: {data.head()}

    Is this result sufficient to answer the user's request?
    Return JSON with:
    {{
        "IS_SUFFICIENT": <boolean>,
        "EXPLANATION": <string : If the answer is not sufficient specify what else is necessary.
                                IFF the answer is sufficient, provide a response that can be returned to the user as an explanation that answers their question.
                                The explanation should use the results to answer their question as long as they wouold be useful to the user.
                                    For example, it is not useful to report on the "average/min/max/std ID" or the "min/max/std/average of a string column".

                                Be smart about what you report.
                                It should not be a conceptual or abstract summary of the data.
                                It should not unnecessarily bring up a need for more data.
                                You should write it in a tone that answers the user request. Do not spout unnecessary self-referential fluff like "This information gives a clear overview of the x landscape".
                                >
    }}
    DO NOT include markdown formatting or ```json tags.

    """

    response = get_llm_response(
        prompt, format="json", model=model, provider=provider, npc=npc
    )

    # Clean response if it's a string
    result = response.get("response", {})
    if isinstance(result, str):
        result = result.replace("```json", "").replace("```", "").strip()
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            return {"IS_SUFFICIENT": False, "EXPLANATION": "Failed to parse response"}

    return result


def process_data_output(
    llm_response: Dict[str, Any],
    db_conn,
    request: str,
    tables: str = None,
    history: str = None,
    npc: Any = None,
    model: str = None,
    provider: str = None,
) -> Dict[str, Any]:
    """
    Process the LLM's response to a data request and execute the appropriate query.
    """
    try:
        choice = llm_response.get("choice")
        query = llm_response.get("query")

        if not query:
            return {"response": "No query provided", "code": 400}

        # Create SQLAlchemy engine based on connection type
        if "psycopg2" in db_conn.__class__.__module__:
            engine = create_engine("postgresql://caug:gobears@localhost/npc_test")
        else:
            engine = create_engine("sqlite:///test_sqlite.db")

        if choice == 1:  # Direct answer query
            try:
                df = pd.read_sql_query(query, engine)
                result = check_output_sufficient(
                    request, df, query, model=model, provider=provider, npc=npc
                )

                if result.get("IS_SUFFICIENT"):
                    return {"response": result["EXPLANATION"], "data": df, "code": 200}
                return {
                    "response": f"Results insufficient: {result.get('EXPLANATION')}",
                    "code": 400,
                }

            except Exception as e:
                return {"response": f"Query execution failed: {str(e)}", "code": 400}

        elif choice == 2:  # Exploratory query
            try:
                df = pd.read_sql_query(query, engine)
                extra_context = f"""
                Exploratory query results:
                Query: {query}
                Results summary: {df.describe()}
                Sample data: {df.head()}
                """

                return get_data_response(
                    request,
                    db_conn,
                    tables=tables,
                    extra_context=extra_context,
                    history=history,
                    model=model,
                    provider=provider,
                    npc=npc,
                )

            except Exception as e:
                return {"response": f"Exploratory query failed: {str(e)}", "code": 400}

        return {"response": "Invalid choice specified", "code": 400}

    except Exception as e:
        return {"response": f"Processing error: {str(e)}", "code": 400}


def get_data_response(
    request: str,
    db_conn,
    tables: str = None,
    n_try_freq: int = 5,
    extra_context: str = None,
    history: str = None,
    model: str = None,
    provider: str = None,
    npc: Any = None,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """
    Generate a response to a data request, with retries for failed attempts.
    """

    # Extract schema information based on connection type
    schema_info = ""
    if "psycopg2" in db_conn.__class__.__module__:
        cursor = db_conn.cursor()
        # Get all tables and their columns
        cursor.execute(
            """
            SELECT
                t.table_name,
                array_agg(c.column_name || ' ' || c.data_type) as columns,
                array_agg(
                    CASE
                        WHEN tc.constraint_type = 'FOREIGN KEY'
                        THEN kcu.column_name || ' REFERENCES ' || ccu.table_name || '.' || ccu.column_name
                        ELSE NULL
                    END
                ) as foreign_keys
            FROM information_schema.tables t
            JOIN information_schema.columns c ON t.table_name = c.table_name
            LEFT JOIN information_schema.table_constraints tc
                ON t.table_name = tc.table_name
                AND tc.constraint_type = 'FOREIGN KEY'
            LEFT JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            LEFT JOIN information_schema.constraint_column_usage ccu
                ON tc.constraint_name = ccu.constraint_name
            WHERE t.table_schema = 'public'
            GROUP BY t.table_name;
        """
        )
        for table, columns, fks in cursor.fetchall():
            schema_info += f"\nTable {table}:\n"
            schema_info += "Columns:\n"
            for col in columns:
                schema_info += f"  - {col}\n"
            if any(fk for fk in fks if fk is not None):
                schema_info += "Foreign Keys:\n"
                for fk in fks:
                    if fk:
                        schema_info += f"  - {fk}\n"

    elif "sqlite3" in db_conn.__class__.__module__:
        cursor = db_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for (table_name,) in tables:
            schema_info += f"\nTable {table_name}:\n"
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema_info += "Columns:\n"
            for col in columns:
                schema_info += f"  - {col[1]} {col[2]}\n"

            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            foreign_keys = cursor.fetchall()
            if foreign_keys:
                schema_info += "Foreign Keys:\n"
                for fk in foreign_keys:
                    schema_info += f"  - {fk[3]} REFERENCES {fk[2]}({fk[4]})\n"

    prompt = f"""
    User request: {request}

    Database Schema:
    {schema_info}

    {extra_context or ''}
    {f'Query history: {history}' if history else ''}

    Provide either:
    1) An SQL query to directly answer the request
    2) An exploratory query to gather more information

    Return JSON with:
    {{
        "query": <sql query string>,
        "choice": <1 or 2>,
        "explanation": <reason for choice>
    }}
    DO NOT include markdown formatting or ```json tags.
    """

    failures = []
    for attempt in range(max_retries):
        # try:
        llm_response = get_llm_response(
            prompt, npc=npc, format="json", model=model, provider=provider
        )

        # Clean response if it's a string
        response_data = llm_response.get("response", {})
        if isinstance(response_data, str):
            response_data = (
                response_data.replace("```json", "").replace("```", "").strip()
            )
            try:
                response_data = json.loads(response_data)
            except json.JSONDecodeError:
                failures.append("Invalid JSON response")
                continue

        result = process_data_output(
            response_data,
            db_conn,
            request,
            tables=tables,
            history=failures,
            npc=npc,
            model=model,
            provider=provider,
        )

        if result["code"] == 200:
            return result

        failures.append(result["response"])

        if attempt == max_retries - 1:
            return {
                "response": f"Failed after {max_retries} attempts. Errors: {'; '.join(failures)}",
                "code": 400,
            }

    # except Exception as e:
    #    failures.append(str(e))


def enter_reasoning_human_in_the_loop(
    messages: List[Dict[str, str]],
    reasoning_model: str = NPCSH_REASONING_MODEL,
    reasoning_provider: str = NPCSH_REASONING_PROVIDER,
    chat_model: str = NPCSH_CHAT_MODEL,
    chat_provider: str = NPCSH_CHAT_PROVIDER,
    npc: Any = None,
    answer_only: bool = False,
    context=None,
) -> Generator[str, None, None]:
    """
    Stream responses while checking for think tokens and handling human input when needed.

    Args:
        messages: List of conversation messages
        model: LLM model to use
        provider: Model provider
        npc: NPC instance if applicable

    Yields:
        Streamed response chunks
    """
    # Get the initial stream
    if answer_only:
        messages[-1]["content"] = (
            messages[-1]["content"].replace(
                "Think first though and use <think> tags", ""
            )
            + " Do not think just answer. "
        )
    else:
        messages[-1]["content"] = (
            messages[-1]["content"]
            + "         Think first though and use <think> tags.  "
        )

    response_stream = get_stream(
        messages,
        model=reasoning_model,
        provider=reasoning_provider,
        npc=npc,
        context=context,
    )

    thoughts = []
    response_chunks = []
    in_think_block = False
    for chunk in response_stream:
        # Check for user interrupt
        
        try:
            # Extract content based on provider
            if reasoning_provider == "ollama":
                chunk_content = chunk.get("message", {}).get("content", "")
            elif reasoning_provider == "openai" or reasoning_provider == "deepseek":
                chunk_content = "".join(
                    choice.delta.content
                    for choice in chunk.choices
                    if choice.delta.content is not None
                )
            elif reasoning_provider == "anthropic":
                if chunk.type == "content_block_delta":
                    chunk_content = chunk.delta.text
                else:
                    chunk_content = ""
            else:
                chunk_content = str(chunk)

            response_chunks.append(chunk_content)
            combined_text = "".join(response_chunks)

            # Check for LLM request block
            if (
                "<request_for_input>" in combined_text
                and "</request_for_input>" not in combined_text
            ):
                in_think_block = True

            if in_think_block:
                thoughts.append(chunk_content)
                yield chunk

            if "</request_for_input>" in combined_text:
                # Process the LLM's input request
                request_text = "".join(thoughts)
                yield "\nPlease provide the requested information: "

                # Wait for user input (blocking here is OK since we explicitly asked)
                user_input = input()

                # Add the interaction to messages and restart stream
                messages.append({"role": "assistant", "content": request_text})
                messages.append({"role": "user", "content": user_input})

                yield "\n[Continuing with provided information...]\n"
                yield from enter_reasoning_human_in_the_loop(
                    messages,
                    reasoning_model=reasoning_model,
                    reasoning_provider=reasoning_provider,
                    chat_model=chat_model,
                    chat_provider=chat_provider,
                    npc=npc,
                    answer_only=True,
                )
                return

            if not in_think_block:
                yield chunk

            
        except KeyboardInterrupt:        
            user_interrupt = input("\n[Stream interrupted by user]\n Enter your additional input: ")
            

            # Add the interruption to messages and restart stream
            messages.append(
                {"role": "user", "content": f"[INTERRUPT] {user_interrupt}"}
            )

            print(f"\n[Continuing with added context...]\n")
            yield from enter_reasoning_human_in_the_loop(
                messages,
                reasoning_model=reasoning_model,
                reasoning_provider=reasoning_provider,
                chat_model=chat_model,
                chat_provider=chat_provider,
                npc=npc,
                answer_only=True,
            )
            return


def handle_request_input(
    context: str,
    model: str = NPCSH_CHAT_MODEL,
    provider: str = NPCSH_CHAT_PROVIDER,
    whisper: bool = False,
):
    """
    Analyze text and decide what to request from the user
    """
    prompt = f"""
    Analyze the text:
    {context}
    and determine what additional input is needed.
    Return a JSON object with:
    {{
        "input_needed": boolean,
        "request_reason": string explaining why input is needed,
        "request_prompt": string to show user if input needed
    }}

    Do not include any additional markdown formatting or leading ```json tags. Your response
    must be a valid JSON object.
    """

    response = get_llm_response(
        prompt,
        model=model,
        provider=provider,
        messages=[],
        format="json",
    )

    result = response.get("response", {})
    if isinstance(result, str):
        result = json.loads(result)

    user_input = request_user_input(
        {"reason": result["request_reason"], "prompt": result["request_prompt"]},
    )
    return user_input


def analyze_thoughts_for_input(
    thought_text: str,
    model: str = NPCSH_CHAT_MODEL,
    provider: str = NPCSH_CHAT_PROVIDER,
    api_url: str = NPCSH_API_URL,
    api_key: str = None,
) -> Optional[Dict[str, str]]:
    """
    Analyze accumulated thoughts to determine if user input is needed.

    Args:
        thought_text: Accumulated text from think block
        messages: Conversation history

    Returns:
        Dict with input request details if needed, None otherwise
    """

    prompt = (
        f"""
         Analyze these thoughts:
         {thought_text}
         and determine if additional user input would be helpful.
        Return a JSON object with:"""
        + """
        {
            "input_needed": boolean,
            "request_reason": string explaining why input is needed,
            "request_prompt": string to show user if input needed
        }
        Consider things like:
        - Ambiguity in the user's request
        - Missing context that would help provide a better response
        - Clarification needed about user preferences/requirements
        Only request input if it would meaningfully improve the response.
        Do not include any additional markdown formatting or leading ```json tags. Your response
        must be a valid JSON object.
        """
    )

    response = get_llm_response(
        prompt,
        model=model,
        provider=provider,
        api_url=api_url,
        api_key=api_key,
        messages=[],
        format="json",
    )

    result = response.get("response", {})
    if isinstance(result, str):
        result = json.loads(result)

    if result.get("input_needed"):
        return {
            "reason": result["request_reason"],
            "prompt": result["request_prompt"],
        }


def request_user_input(input_request: Dict[str, str]) -> str:
    """
    Request and get input from user.

    Args:
        input_request: Dict with reason and prompt for input

    Returns:
        User's input text
    """
    print(f"\nAdditional input needed: {input_request['reason']}")
    return input(f"{input_request['prompt']}: ")


def check_user_input() -> Optional[str]:
    """
    Non-blocking check for user input.
    Returns None if no input is available, otherwise returns the input string.
    """
    if select.select([sys.stdin], [], [], 0.0)[0]:
        return input()
    return None


def input_listener(input_queue: Queue):
    """
    Continuously listen for user input in a separate thread.
    """
    while True:
        try:
            user_input = input()
            input_queue.put(user_input)
        except EOFError:
            break


def stream_with_interrupts(
    messages: List[Dict[str, str]],
    model: str,
    provider: str,
    npc: Any = None,
    context=None,
) -> Generator[str, None, None]:
    """Stream responses with basic Ctrl+C handling and recursive conversation loop."""
    response_stream = get_stream(
        messages, model=model, provider=provider, npc=npc, context=context
    )

    try:
        # Flag to track if streaming is complete
        streaming_complete = False

        for chunk in response_stream:
            if provider == "ollama" and 'hf.co' in model:
                chunk_content = chunk.get("message", {}).get("content", "")
            else:
                chunk_content = "".join(
                    choice.delta.content
                    for choice in chunk.choices
                    if choice.delta.content is not None
                )
            yield chunk_content

            # Optional: Mark streaming as complete when no more chunks
            if not chunk_content:
                streaming_complete = True

    except KeyboardInterrupt:
        # Handle keyboard interrupt by getting user input
        user_input = input("\n> ")
        messages.append({"role": "user", "content": user_input})
        yield from stream_with_interrupts(
            messages, model=model, provider=provider, npc=npc, context=context
        )

    finally:
        # Prompt for next input and continue conversation
        while True:
            user_input = input("\n> ")

            # Option to exit the loop
            if user_input.lower() in ["exit", "quit", "q"]:
                break

            # Add user input to messages
            messages.append({"role": "user", "content": user_input})

            # Recursively continue the conversation
            yield from stream_with_interrupts(
                messages, model=model, provider=provider, npc=npc, context=context
            )
