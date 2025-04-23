import argparse
from npcpy.npc_sysenv import (
    NPCSH_CHAT_MODEL,
    NPCSH_CHAT_PROVIDER,
    NPCSH_IMAGE_GEN_MODEL,
    NPCSH_IMAGE_GEN_PROVIDER,
    NPCSH_API_URL,
    NPCSH_REASONING_MODEL,
    NPCSH_REASONING_PROVIDER,
    NPCSH_DB_PATH,
    NPCSH_VISION_MODEL,
    NPCSH_VISION_PROVIDER,
    NPCSH_DB_PATH,
    NPCSH_STREAM_OUTPUT,
    NPCSH_SEARCH_PROVIDER,
    print_and_process_stream
)
from npcpy.serve import start_flask_server
from npcpy.npc_compiler import (
    
    conjure_team,
    NPC,
)
from npcpy.llm_funcs import (
    check_llm_command,
    execute_llm_command,
    execute_llm_question,
    handle_tool_call,
    generate_image,
    get_embeddings,
    get_llm_response,
    get_stream,
    get_conversation,
)
from npcpy.plonk import plonk, action_space
from npcpy.search import search_web
from npcpy.shell_helpers import *
import os
import sqlite3

# check if ./npc_team exists
if os.path.exists("./npc_team"):
    npc_directory = os.path.abspath("./npc_team/")
else:
    npc_directory = os.path.expanduser("~/.npcsh/npc_team/")




def main():
    parser = argparse.ArgumentParser(description="NPC utilities")
    known_commands = {
        "assemble",
        "build",
        "compile",
        "chat",
        "init",
        "new",
        "plonk",
        "sample",
        "search",
        "select",
        "serve",
        "spool",
        "tools",
        "tool",
        "local_search",
        "rag",
        "search",
        "vixynt",
        "ots",
        "whisper",
    }
    has_command = any(arg in known_commands for arg in sys.argv[1:])

    # Only add prompt as default if first arg isn't a known command
    if not has_command:
        parser.add_argument(
            "prompt", nargs="?", help="Generic prompt to send to the default LLM"
        )
        parser.add_argument(
            "--model", "-m", help="model to use", type=str, default=NPCSH_CHAT_MODEL
        )
        parser.add_argument(
            "--provider",
            "-pr",
            help="provider to use",
            type=str,
            default=NPCSH_CHAT_PROVIDER,
        )

        parser.add_argument(
            "-n", "--npc", help="name of the NPC", type=str, default="sibiji"
        )
        args = parser.parse_args()
        db_conn = sqlite3.connect(NPCSH_DB_PATH)
        if args.npc is None or args.npc == "sibiji":
            npc = NPC(file="~/.npcsh/npc_team/sibiji.npc", db_conn = db_conn)
        else:
            npc = NPC(file="./npc_team/" + args.npc + ".npc", db_conn = db_conn)

        response = check_llm_command(
            args.prompt, model=args.model, provider=args.provider, npc=npc, stream=True
        )
        provider = args.provider
        model = args.model
        conversation_result = print_and_process_stream(response, provider, model)
        return

    parser.add_argument(
        "--model", "-m", help="model to use", type=str, default=NPCSH_CHAT_MODEL
    )
    parser.add_argument(
        "--provider",
        "-pr",
        help="provider to use",
        type=str,
        default=NPCSH_CHAT_PROVIDER,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Generic prompt parser (for "npc 'prompt'")

    # need it so that this prompt is just automatically resolved as the only argument if no positional ones are provided
    # parser.add_argument(
    #    "prompt", nargs="?", help="Generic prompt to send to the default LLM"
    # )

    ### ASSEMBLY LINE PARSER
    assembly_parser = subparsers.add_parser("assemble", help="Run an NPC assembly line")
    assembly_parser.add_argument("line", help="Assembly line to run")

    ### BUILD PARSER
    build_parser = subparsers.add_parser(
        "build", help="Build a NPC team into a standalone executable server"
    )
    build_parser.add_argument(
        "directory", nargs="?", default=".", help="Directory to build project in"
    )

    # chat
    chat_parser = subparsers.add_parser("chat", help="chat with an NPC")
    chat_parser.add_argument("-n", "--npc_name", help="name of npc")

    # Compile command
    compile_parser = subparsers.add_parser("compile", help="Compile an NPC")
    compile_parser.add_argument("path", help="Path to NPC file")

    # Conjure/init command
    init_parser = subparsers.add_parser("init", help="Initialize a new NPC project")
    init_parser.add_argument(
        "directory", nargs="?", default=".", help="Directory to initialize project in"
    )
    init_parser.add_argument(
        "--templates", "-t", help="agent templates(comma-separated list)", type=str
    )
    init_parser.add_argument(
        "--context",
        "-ctx",
        help="important information when merging templates",
        type=str,
    )
    ### NEW PARSER
    new_parser = subparsers.add_parser(
        "new", help="Create a new [NPC, tool, assembly_line, ]"
    )
    new_parser.add_argument(
        "type",
        help="Type of object to create",
        choices=["npc", "tool", "assembly_line"],
    )

    new_parser.add_argument(
        "--primary_directive",
        "-pd",
        help="primary directive (when making an npc)",
        type=str,
    )

    new_parser.add_argument(
        "--name",
        "-n",
        help="name",
        type=str,
    )

    new_parser.add_argument(
        "--description",
        "-d",
        help="description",
        type=str,
    )

    new_parser.add_argument("--autogen", help="whether to auto gen", default=False)

    ### plonk
    plonk_parser = subparsers.add_parser("plonk", help="computer use with plonk!")
    plonk_parser.add_argument(
        "--task",
        "-t",
        help="the task for plonk to accomplish",
        type=str,
    )
    plonk_parser.add_argument(
        "--name",
        "-n",
        help="name of the NPC",
        type=str,
    )
    plonk_parser.add_argument(
        "--spell",
        "-sp",
        help="task for plonk to carry out",
        type=str,
    )

    # sample
    sampler_parser = subparsers.add_parser(
        "sample", help="sample question one shot to an llm"
    )
    sampler_parser.add_argument("prompt", help="prompt for llm")
    sampler_parser.add_argument(
        "--npc",
        "-n",
        help="name of the NPC",
        type=str,
    )
    select_parser = subparsers.add_parser("select", help="Select a SQL model to run")
    select_parser.add_argument("model", help="Model to run")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the Flask server")
    serve_parser.add_argument("--port", "-p", help="Optional port")
    serve_parser.add_argument(
        "--cors", "-c", help="CORS origins (comma-separated list)", type=str
    )
    serve_parser.add_argument(
        "--templates", "-t", help="agent templates(comma-separated list)", type=str
    )
    serve_parser.add_argument(
        "--context",
        "-ctx",
        help="important information when merging templates",
        type=str,
    )
    ### spool
    spool_parser = subparsers.add_parser("spool", help="Start the Flask server")
    spool_parser.add_argument("-n", "--npc", default="sibiji")

    # Tools command
    tools_parser = subparsers.add_parser("tools", help="print the available tools")

    # Tool invocation
    tool_parser = subparsers.add_parser("tool", help="invoke a tool")
    tool_parser.add_argument("tool_name", help="name of the tool to invoke")
    tool_parser.add_argument(
        "--args", "-a", help="arguments for the tool", nargs="+", default=[]
    )
    tool_parser.add_argument(
        "--flags", "-f", help="flags for the tool", nargs="+", default=[]
    )

    # Local search
    local_search_parser = subparsers.add_parser("local_search", help="search locally")
    local_search_parser.add_argument("query", help="search query")
    local_search_parser.add_argument(
        "--path", "-p", help="path to search in", default="."
    )

    # RAG search
    rag_parser = subparsers.add_parser("rag", help="search for a term in the npcsh_db")
    rag_parser.add_argument("--name", "-n", help="name of the NPC", required=True)
    rag_parser.add_argument(
        "--filename", "-f", help="filename to search in", required=True
    )
    rag_parser.add_argument("--query", "-q", help="search query", required=True)

    # Web search
    search_parser = subparsers.add_parser("search", help="search the web")
    search_parser.add_argument("--query", "-q", help="search query")
    search_parser.add_argument(
        "--search_provider",
        "-sp",
        help="search provider",
        default=NPCSH_SEARCH_PROVIDER,
    )

    # Image generation
    vixynt_parser = subparsers.add_parser("vixynt", help="generate an image")
    vixynt_parser.add_argument("--height", "-ht", help="the height of the image")
    vixynt_parser.add_argument("--width", "-wd", help="the width of the image")
    vixynt_parser.add_argument("spell", help="the prompt to generate the image")

    # Screenshot analysis
    ots_parser = subparsers.add_parser("ots", help="analyze screenshot")

    # Voice chat
    whisper_parser = subparsers.add_parser("whisper", help="start voice chat")
    whisper_parser.add_argument("-n", "--npc_name", help="name of the NPC to chat with")

    args = parser.parse_args()

    # Handle NPC chat if the command matches an NPC name
    if args.command and not args.command.startswith("-"):
        try:
            # Check if command is actually an NPC name
            if os.path.exists(f"npcs/{args.command}.npc"):
                start_npc_chat(args.command)
                return
        except Exception as e:
            print(f"Error starting chat with NPC {args.command}: {e}")

    if args.command == "serve":
        if args.cors:
            # Parse the CORS origins from the comma-separated string
            cors_origins = [origin.strip() for origin in args.cors.split(",")]
        else:
            cors_origins = None
        if args.templates:
            templates = [template.strip() for template in args.templates.split(",")]
        else:
            templates = None
        if args.context:
            context = args.context.strip()
        else:
            context = None
        if args.model:
            model = args.model
        else:
            model = NPCSH_CHAT_MODEL
        if args.provider:
            provider = args.provider
        else:
            provider = NPCSH_CHAT_PROVIDER

        if context is not None and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            initialize_npc_project(
                args.directory,
                templates=templates,
                context=context,
                model=model,
                provider=provider,
            )

        start_flask_server(
            port=args.port if args.port else 5337,
            cors_origins=cors_origins,
        )
    elif args.command == "chat":
        npc_name = args.npc_name
        npc_path = get_npc_path(npc_name, NPCSH_DB_PATH)
        current_npc = NPC(file=npc_path, db_conn = sqlite3.connect(NPCSH_DB_PATH))
        return enter_spool_mode(
            model=args.model, provider=args.provider, npc=current_npc
        )

    elif args.command == "init":
        if args.templates:
            templates = [template.strip() for template in args.templates.split(",")]
        else:
            templates = None
        if args.context:
            context = args.context.strip()
        else:
            context = None
        if args.model:
            model = args.model
        else:
            model = NPCSH_CHAT_MODEL
        if args.provider:
            provider = args.provider
        else:
            provider = NPCSH_CHAT_PROVIDER

        initialize_npc_project(
            args.directory,
            templates=templates,
            context=context,
            model=model,
            provider=provider,
        )

    elif args.command == "compile":

        print("fix npc compile")

    elif args.command == "plonk":
        task = args.task or args.spell
        npc_name = args.name
        plonk(
            task,
            action_space,
            model=args.model or NPCSH_CHAT_MODEL,
            provider=args.provider or NPCSH_CHAT_PROVIDER,
        )

    elif args.command == "sample":
        db_conn = sqlite3.connect(NPCSH_DB_PATH)
        if args.npc is None or args.npc == "sibiji":
            npc = NPC(file="~/.npcsh/npc_team/sibiji.npc", db_conn=db_conn)
        else:
            npc = NPC(file="./npc_team/" + args.npc + ".npc", db_conn= db_conn)

        result = get_llm_response(
            args.prompt,
            model=args.model,
            provider=args.provider,
        )
        print(result["response"])
    elif args.command == "vixynt":
        if args.model == NPCSH_CHAT_MODEL:
            model = NPCSH_IMAGE_GEN_MODEL
        if args.provider == NPCSH_CHAT_PROVIDER:
            provider = NPCSH_IMAGE_GEN_PROVIDER
        image_path = generate_image(
            args.spell,
            model=args.model,
            provider=args.provider,
            height=int(args.height),
            width=int(args.width),
        )
        print(f"Image generated at: {image_path}")

    elif args.command == "ots":
        if args.model == NPCSH_CHAT_MODEL:
            model = NPCSH_VISION_MODEL
        if args.provider == NPCSH_CHAT_PROVIDER:
            provider = NPCSH_VISION_PROVIDER

        result = ots(
            "",
            model=args.model,
            provider=args.provider,
        )
        print(result["output"])

    elif args.command == "whisper":
        npc_name = args.npc_name
        npc_path = get_npc_path(npc_name, NPCSH_DB_PATH)
        current_npc = NPC(file=npc_path, db_conn = sqlite3.connect(NPCSH_DB_PATH))

        enter_whisper_mode(npc=current_npc)

    elif args.command == "tool":
        result = invoke_tool(
            args.tool_name,
            args=args.args,
            flags=args.flags,
        )
        print(result)

    elif args.command == "tools":
        tools = list_available_tools()
        for tool in tools:
            print(f"- {tool}")

    elif args.command == "local_search":
        results = perform_local_search(args.query, path=args.path)
        for result in results:
            print(f"- {result}")

    elif args.command == "rag":
        results = perform_rag_search(
            npc_name=args.name,
            filename=args.filename,
            query=args.query,
        )
        for result in results:
            print(f"- {result}")

    elif args.command == "search":
        results = search_web(args.query, provider=args.provider)
        for result in results:
            print(f"- {result}")

    elif args.command == "new":
        # create a new npc, tool, or assembly line
        if args.type == "npc":
            from npcpy.npc_creator import create_new_npc

            create_new_npc(
                name=args.name,
                primary_directive=args.primary_directive,
                description=args.description,
                model=args.model or NPCSH_CHAT_MODEL,
                provider=args.provider or NPCSH_CHAT_PROVIDER,
                autogen=args.autogen,
            )
        elif args.type == "tool":
            create_new_tool(
                name=args.name,
                description=args.description,
                autogen=args.autogen,
            )
        elif args.type == "assembly_line":
            create_new_assembly_line(
                name=args.name,
                description=args.description,
                autogen=args.autogen,
            )
    elif args.command == "spool":
        db_conn = sqlite3.connect(NPCSH_DB_PATH)
        if args.npc is None or args.npc == "sibiji":
            npc = NPC(file="~/.npcsh/npc_team/sibiji.npc", db_conn=db_conn)
        else:
            npc = NPC(file="./npc_team/" + args.npc + ".npc", db_conn=db_conn)
        response = enter_spool_mode(
            stream=True,
            npc=npc,
        )


if __name__ == "__main__":
    main()
