import os
import sys
import readline
import atexit
from inspect import isgenerator
from termcolor import colored
from sqlalchemy import create_engine
from npcpy.npc_sysenv import (
    print_and_process_stream_with_markdown,
    NPCSH_STREAM_OUTPUT,
    NPCSH_CHAT_MODEL,
    NPCSH_CHAT_PROVIDER,
    NPCSH_API_URL,
)

from npcpy.command_history import (
    CommandHistory,
    start_new_conversation,
    save_conversation_message,
)
from npcpy.helpers import (
    setup_npcsh_config,
    is_npcsh_initialized,
    initialize_base_npcs_if_needed,
)
from npcpy.shell_helpers import (
    complete,  # For command completion
    readline_safe_prompt,
    get_multiline_input,
    setup_readline,
    execute_command,

    orange,  # For colored prompt
)
from npcpy.npc_compiler import (
    NPC, Team
)

import argparse
import importlib.metadata  
try:
    VERSION = importlib.metadata.version(
        "npcpy"
    )  
except importlib.metadata.PackageNotFoundError:
    VERSION = "unknown"  


def main() -> None:
    """
    Main function for the npcsh shell and server.
    Starts either the Flask server or the interactive shell based on the argument provided.
    """
    # Set up argument parsing to handle 'serve' and regular commands

    check_old_par_name = os.environ.get("NPCSH_MODEL", None)
    if check_old_par_name is not None:
        # raise a deprecation warning
        print(
            """Deprecation Warning: NPCSH_MODEL and NPCSH_PROVIDER were deprecated in v0.3.5 in favor of NPCSH_CHAT_MODEL and NPCSH_CHAT_PROVIDER instead.\
                Please update your environment variables to use the new names.
                """
        )

    parser = argparse.ArgumentParser(description="npcsh CLI")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"npcsh version {VERSION}",  # Use the dynamically fetched version
    )
    args = parser.parse_args()

    setup_npcsh_config()
    if "NPCSH_DB_PATH" in os.environ:
        db_path = os.path.expanduser(os.environ["NPCSH_DB_PATH"])
    else:
        db_path = os.path.expanduser("~/npcsh_history.db")

    command_history = CommandHistory(db_path)

    readline.set_completer_delims(" \t\n")
    readline.set_completer(complete)
    if sys.platform == "darwin":
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    # check if ./npc_team exists
    if os.path.exists("./npc_team"):

        npc_directory = os.path.abspath("./npc_team/")
    else:
        npc_directory = os.path.expanduser("~/.npcsh/npc_team/")


    os.makedirs(npc_directory, exist_ok=True)
    """ 
    # Compile all NPCs in the user's npc_team directory
    for filename in os.listdir(npc_directory):
        if filename.endswith(".npc"):
            npc_file_path = os.path.join(npc_directory, filename)
            npc_compiler.compile(npc_file_path)

    # Compile NPCs from project-specific npc_team directory
    if os.path.exists(npc_directory):
        for filename in os.listdir(npc_directory):
            if filename.endswith(".npc"):
                npc_file_path = os.path.join(npc_directory, filename)
                npc_compiler.compile(npc_file_path) """

    if not is_npcsh_initialized():
        print("Initializing NPCSH...")
        initialize_base_npcs_if_needed(db_path)
        print(
            "NPCSH initialization complete. Please restart your terminal or run 'source ~/.npcshrc' for the changes to take effect."
        )

    history_file = setup_readline()
    atexit.register(readline.write_history_file, history_file)
    atexit.register(command_history.close)
    # make npcsh into ascii art
    from colorama import init

    init()  # Initialize colorama for ANSI code support
    if sys.stdin.isatty():

        print(
            """
    Welcome to \033[1;94mnpc\033[0m\033[1;38;5;202msh\033[0m!
    \033[1;94m                    \033[0m\033[1;38;5;202m               \\\\
    \033[1;94m _ __   _ __    ___ \033[0m\033[1;38;5;202m ___  | |___    \\\\
    \033[1;94m| '_ \ | '_ \  / __|\033[0m\033[1;38;5;202m/ __/ | |_ _|    \\\\
    \033[1;94m| | | || |_) |( |__ \033[0m\033[1;38;5;202m\_  \ | | | |    //
    \033[1;94m|_| |_|| .__/  \___|\033[0m\033[1;38;5;202m|___/ |_| |_|   //
            \033[1;94m| |          \033[0m\033[1;38;5;202m              //
            \033[1;94m| |
            \033[1;94m|_|

    Begin by asking a question, issuing a bash command, or typing '/help' for more information.
            """
        )

    current_npc = None
    messages = None
    current_conversation_id = start_new_conversation()
    team = Team(team_path=npc_directory)
    sibiji = NPC(file=os.path.expanduser("~/.npcsh/npc_team/sibiji.npc")    )
    npc = sibiji
    if not sys.stdin.isatty():
        for line in sys.stdin:
            user_input = line.strip()
            if not user_input:
                continue  # Skip empty lines
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                sys.exit(0)
            result = execute_command(
                user_input,
                db_path,
                npc = npc,
                team=team,
                model=NPCSH_CHAT_MODEL,
                provider=NPCSH_CHAT_PROVIDER,
                messages=messages,
                conversation_id=current_conversation_id,
                stream=NPCSH_STREAM_OUTPUT,
                api_url=NPCSH_API_URL,
            )
            messages = result.get("messages", messages)
            if "current_npc" in result:
                current_npc = result["current_npc"]
            output = result.get("output")
            conversation_id = result.get("conversation_id")
            model = result.get("model")
            provider = result.get("provider")
            npc = result.get("npc")
            team = result.get("team")
            messages = result.get("messages")
            current_path = result.get("current_path")
            attachments = result.get("attachments")
            npc_name = (
                npc.name
                if isinstance(npc, NPC)
                else npc if isinstance(npc, str) else None
            )
            
            save_conversation_message(
                command_history,
                conversation_id,
                "user",
                user_input,
                wd=current_path,
                model=model,
                provider=provider,
                npc=npc_name,
                attachments=attachments,
            )
            if NPCSH_STREAM_OUTPUT and (
                isgenerator(output)
                or (hasattr(output, "__iter__") and hasattr(output, "__next__"))
            ):
                output = print_and_process_stream_with_markdown(    
                                                                output, model, provider)

                    
        save_conversation_message(
            command_history,
            conversation_id,
            "assistant",
            output,
            wd=current_path,
            model=model,
            provider=provider,
            npc=npc_name,
        )
        sys.exit(0)

    while True:
        try:
            if current_npc:
                prompt = f"{colored(os.getcwd(), 'blue')}:{orange(current_npc.name)}> "
            else:
                prompt = f"{colored(os.getcwd(), 'blue')}:\033[1;94mnpc\033[0m\033[1;38;5;202msh\033[0m!> "

            prompt = readline_safe_prompt(prompt)
            user_input = get_multiline_input(prompt).strip()
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                if current_npc:
                    print(f"Exiting {current_npc.name} mode.")
                    current_npc = None
                    continue
                else:
                    print("Goodbye!")
                    break
            if npc is not None:
                print(f"{npc.name}>", end="")

            result = execute_command(
                user_input,
                npc= npc,
                team=team,
                model=NPCSH_CHAT_MODEL,
                provider=NPCSH_CHAT_PROVIDER,
                messages=messages,
                conversation_id=current_conversation_id,
                stream=NPCSH_STREAM_OUTPUT,
                api_url=NPCSH_API_URL,
            )

            messages = result.get("messages", messages)

            # need to adjust the output for the messages to all have
            # model, provider, npc, timestamp, role, content
            # also messages

            if "npc" in result:

                npc = result["npc"]
            output = result.get("output")

            conversation_id = result.get("conversation_id")
            model = result.get("model")
            provider = result.get("provider")

            messages = result.get("messages")
            current_path = result.get("current_path")
            attachments = result.get("attachments")

            if current_npc is not None:
                if isinstance(current_npc, NPC):
                    npc_name = current_npc.name
                elif isinstance(current_npc, str):
                    npc_name = current_npc
            else:
                npc_name = None
            message_id = save_conversation_message(
                command_history,
                conversation_id,
                "user",
                user_input,
                wd=current_path,
                model=model,
                provider=provider,
                npc=npc_name,
                attachments=attachments,
            )


            #import pdb 
            #pdb.set_trace()
            str_output = ""
            try:
                if NPCSH_STREAM_OUTPUT and hasattr(output, "__iter__"):

                    buffer = ""
                    in_code = False
                    code_buffer = ""

                    for chunk in output:

                        chunk_content = "".join(
                            c.delta.content for c in chunk.choices if c.delta.content
                        )
                        if not chunk_content:
                            continue

                        str_output += chunk_content
                        # print(str_output, "str_output")
                        # Process the content character by character
                        for char in chunk_content:
                            buffer += char

                            # Check for triple backticks
                            if buffer.endswith("```"):
                                if not in_code:
                                    # Start of code block
                                    in_code = True
                                    # Print everything before the backticks
                                    print(buffer[:-3], end="")
                                    buffer = ""
                                    code_buffer = ""
                                else:
                                    # End of code block
                                    in_code = False
                                    # Remove the backticks from the end of the buffer
                                    buffer = buffer[:-3]
                                    # Add buffer to code content and render
                                    code_buffer += buffer

                                    # Check for and strip language tag
                                    if (
                                        "\n" in code_buffer
                                        and code_buffer.index("\n") < 15
                                    ):
                                        first_line, rest = code_buffer.split("\n", 1)
                                        if (
                                            first_line.strip()
                                            and not "```" in first_line
                                        ):
                                            code_buffer = rest

                                    # Render the code block
                                    render_code_block(code_buffer)

                                    # Reset buffers
                                    buffer = ""
                                    code_buffer = ""
                            elif in_code:
                                # Just add to code buffer
                                code_buffer += char
                                if len(buffer) >= 3:  # Keep buffer small while in code
                                    buffer = buffer[-3:]
                            else:
                                # Regular text - print if buffer gets too large
                                if len(buffer) > 100:
                                    print(buffer[:-3], end="")
                                    buffer = buffer[
                                        -3:
                                    ]  # Keep last 3 chars to check for backticks

                    # Handle any remaining content
                    if in_code:
                        render_code_block(code_buffer)
                    else:
                        print(buffer, end="")

                    if str_output:
                        output = str_output
            except:
                output = None

            print("\n")

            if isinstance(output, str):
                save_conversation_message(
                    command_history,
                    conversation_id,
                    "assistant",
                    output,
                    wd=current_path,
                    model=model,
                    provider=provider,
                    npc=npc_name,
                )

            # if there are attachments in most recent user sent message, save them
            # save_attachment_to_message(command_history, message_id, # file_path, attachment_name, attachment_type)

            if (
                result["output"] is not None
                and not user_input.startswith("/")
                and not isinstance(result, dict)
            ):
                print("final", result)

        except (KeyboardInterrupt, EOFError):
            if current_npc:
                print(f"\nExiting {current_npc.name} mode.")
                current_npc = None
            else:
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    main()
