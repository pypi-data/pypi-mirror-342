import asyncio
import json
import os
import pathlib
import platform
import socket
import subprocess
import sys
import time
import argparse # Added
from importlib import metadata # Added
from typing import Any, Dict, List

import requests
import websockets

DEFAULT_PORT: int = 19222

# --- Function to get package version ---
def get_package_version() -> str:
    """Retrieves the package version using importlib.metadata."""
    try:
        return metadata.version('auto-claude')
    except metadata.PackageNotFoundError:
        return "unknown" # Or handle as an error

# --- Existing functions (get_trusted_tools, inject_script, is_port_open, get_claude_config_path, get_claude_config, start_claude) remain the same ---
# ... (Keep existing functions here) ...
def get_trusted_tools(claude_config: Dict[str, Any]) -> List[str]:
    """
    Get the list of trusted tools from the Claude MCP config.
    """
    trusted_tools: List[str] = []
    if 'mcpServers' in claude_config:
        for server in claude_config['mcpServers'].values():
            if 'autoapprove' in server:
                trusted_tools.extend(server['autoapprove'])
    return trusted_tools


async def inject_script(
    claude_config: Dict[str, Any], port: int = DEFAULT_PORT
) -> None:
    """
    Inject the script into the Claude Desktop App.
    """
    # Get active targets (windows, tabs)
    response: requests.Response = requests.get(f"http://localhost:{port}/json")
    targets: List[Dict[str, Any]] = response.json()

    # Extract trusted tools from config
    trusted_tools: List[str] = get_trusted_tools(claude_config)

    # Add trusted tools to `js_to_inject`
    # TODO: Use 'with open(...)' for safer file handling
    js_to_inject: str = open(pathlib.Path(__file__).parent / "inject.js").read()
    js_with_tools: str = js_to_inject.replace(
        "const trustedTools = [];", f"const trustedTools = {json.dumps(trusted_tools)};"
    )

    # Optionally target a specific tab (e.g., based on URL)
    target: Dict[str, Any] = next(
        t for t in targets if "url" in t and "claude" in t["url"].lower()
    )

    ws_url: str = target["webSocketDebuggerUrl"]
    max_attempts: int = 10
    for attempt in range(max_attempts):
        try:
            # The 'ws' variable gets its type from the context manager
            async with websockets.connect(ws_url) as ws:
                # Execute JS code
                await ws.send(
                    json.dumps(
                        {
                            "id": 1,
                            "method": "Runtime.evaluate",
                            "params": {
                                "expression": js_with_tools,
                                "contextId": 1,
                                "replMode": True,
                            },
                        }
                    )
                )
                result: Any = await ws.recv()  # Type can vary, Any is safe
                result_str = str(result)  # Ensure it's a string for comparison
                # Check if the response string contains key success indicators
                if '"id":1' in result_str and '"value":true' in result_str:
                    success_message = (
                        "\n\033[92mSuccessfully injected auto-approve script.\n"
                        "Note: Auto-approval only applies to tools listed as 'autoapprove' "
                        "in your Claude config file.\033[0m\n"
                    )
                    print(success_message)
                    return
                else:
                    print(f"Attempt {attempt + 1}: Unexpected result:", result_str)
        except Exception as e:
            print(f'Attempt {attempt + 1} failed:', e)
        if attempt < max_attempts - 1:
            await asyncio.sleep(1)
    raise ValueError('Max retry attempts reached without success')


def is_port_open(port: int, host: str = "localhost") -> bool:
    """
    Check if a port is open on a given host.

    Useful to check if the Claude Desktop App is running in debug mode.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def get_claude_config_path() -> pathlib.Path:
    """
    Get the path to the Claude MCP config file.
    """
    # Determine the operating system
    os_name: str = platform.system()
    config_path: pathlib.Path

    # macOS
    if os_name == "Darwin":
        config_path = (
            pathlib.Path.home()
            / "Library"
            / "Application Support"
            / "Claude"
            / "claude_desktop_config.json"
        )

    # Windows
    elif os_name == "Windows":
        config_path = (
            pathlib.Path(os.environ["APPDATA"])
            / "Claude"
            / "claude_desktop_config.json"
        )

    else:
        raise OSError(f"Unsupported operating system: {os_name}")

    return config_path


def get_claude_config() -> Dict[str, Any]:
    """
    Get the Claude MCP config.
    """
    config_path: pathlib.Path = get_claude_config_path()
    claude_config: Dict[str, Any]
    # Read Claude MCP config
    try:
        # TODO: Specify encoding explicitly, e.g., encoding="utf-8"
        with open(config_path, "r") as f:
            claude_config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Claude config file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in config file at {config_path}")

    return claude_config


def start_claude(port: int = DEFAULT_PORT) -> None:
    """
    Start the Claude Desktop App.
    """
    # Determine the operating system
    os_name: str = platform.system()

    # macOS
    if os_name == "Darwin":
        subprocess.run(
            ["open", "-a", "Claude", "--args", f"--remote-debugging-port={port}"],
            check=True,
        )

    # Windows
    elif os_name == "Windows":
        subprocess.run(
            ["start", "", "Claude", f"--remote-debugging-port={port}"],
            shell=True,
            check=True,
        )

    else:
        raise OSError(f"Unsupported operating system: {os_name}")

    # Wait for the port to become available
    max_attempts: int = 10
    for _ in range(max_attempts):
        if is_port_open(port):
            break
        time.sleep(1)
    else:
        raise TimeoutError(f"Failed to connect to port {port} after multiple attempts")


# --- Modified async_main to accept port ---
async def async_main(port: int) -> None: # Modified signature
    """
    Async entry point
    """
    # Port is now passed as an argument
    start_claude(port)
    await asyncio.sleep(1) # Give Claude time to start fully
    await inject_script(get_claude_config(), port)


def main() -> None:
    """
    Entry point for the auto-claude CLI.
    """
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description="Automatically approve trusted tools in Claude Desktop App."
    )
    parser.add_argument(
        'port',
        type=int,
        nargs='?', # Make port optional
        default=DEFAULT_PORT,
        help=f"Remote debugging port for Claude (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {get_package_version()}', # Use retrieved version
        help="Show program's version number and exit."
    )
    args = parser.parse_args()

    # --- Main Logic ---
    try:
        # Pass the parsed port to async_main
        asyncio.run(async_main(args.port))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
