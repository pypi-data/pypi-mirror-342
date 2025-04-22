import ast
import configparser
import json
import os
import re
import shutil
import sys
import time
import tomllib
import webbrowser
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import click
import requests
import pwinput
from dotenv import load_dotenv

from almanak import Almanak, __version__


def load_api_key():
    """Loads the API key from the config file."""
    # Load environment variables first
    config_dir = Path(click.get_app_dir("almanak"))
    config_file = config_dir / "config.ini"

    config = configparser.ConfigParser()

    if config_file.exists():
        config.read(config_file)
        env = os.environ.get("ALMANAK_ENV", "prod")
        if env in config:
            return config[env].get("api_key") if config[env].get("api_key") else os.environ.get("ALMANAK_API_KEY")

    return os.environ.get("ALMANAK_API_KEY")


def get_strategy_id_from_almanak(folder: str) -> str | None:
    """Read strategy ID from .almanak file if it exists"""
    config_dir = Path(click.get_app_dir("almanak"))
    almanak_config_file = config_dir / ".almanak"

    folder = Path(folder).resolve()
    if almanak_config_file.exists():
        with open(almanak_config_file) as f:
            config = json.load(f)
            return config.get(str(folder))
    return None


def save_strategy_id_to_almanak(strategy_id: str, folder: str):
    """Save strategy ID to .almanak file"""
    config_dir = Path(click.get_app_dir("almanak"))
    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    almanak_config_file = config_dir / ".almanak"

    folder = Path(folder).resolve()
    config = {}
    # Load existing config if file exists
    if almanak_config_file.exists():
        try:
            with open(almanak_config_file) as f:
                config = json.load(f)
        except json.JSONDecodeError:
            # Handle corrupted file by starting fresh
            config = {}

    # Update config with new strategy ID
    config[str(folder)] = strategy_id

    with open(almanak_config_file, "w") as f:
        json.dump(config, f)


def initialize_client():
    """Initialize the Almanak client using the API key."""
    api_key = load_api_key()

    if not api_key:
        raise Exception("No API key found. Please run 'almanak auth' first.")

    return Almanak(api_key=api_key)


def save_api_key(api_key):
    """Saves the API key to the config file."""
    config_dir = Path(click.get_app_dir("almanak"))
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.ini"

    config = configparser.ConfigParser()

    if config_file.exists():
        config.read(config_file)

    env = os.environ.get("ALMANAK_ENV", "prod")
    if env not in config:
        config[env] = {}

    config[env]["api_key"] = api_key

    with open(config_file, "w") as f:
        config.write(f)


def format_output(status: str = None, title=None, key_value_pairs=None, items=None, delimiter=True):
    """
    Formats and prints a title, a dictionary of key-value pairs, or a list of items with consistent formatting.

    :param status: Status of the response (success, error, info).
    :param title: The section title to display (e.g., "Available Strategies").
    :param key_value_pairs: A dictionary of key-value pairs to display in a formatted manner.
    :param items: A list of items to display with numbering.
    :param delimiter: Whether to print a delimiter (separator line) around the content.
    """
    output = []
    if delimiter:
        output.append("=========================================")

    if status:
        output.append(f"[{status.upper()}]")

    if title:
        output.append(title)
        output.append("-----------------------------------------")

    if key_value_pairs:
        for key, value in key_value_pairs.items():
            output.append(f"{key:<18}: {value}")

    if items:
        for i, item in enumerate(items, start=1):
            output.append(f"{i}. {item}")

    if delimiter:
        output.append("=========================================")

    click.echo("\n".join(output))


@click.group()
@click.version_option(__version__)
def almanak():
    """Almanak CLI for managing strategies."""
    pass


@almanak.group()
def strat():
    """Commands for managing strategies."""
    pass

@almanak.group()
def dashboard():
    """Commands for managing the Almanak dashboard."""
    pass


@almanak.command()
def auth():
    """Authenticate the Almanak CLI"""

    env = os.environ.get("ALMANAK_ENV", "prod")

    match env:
        case "prod":
            url = "https://app.almanak.co/settings/api-keys"
        case "stage":
            url = "https://stage.almanak.co/settings/api-keys"
        case _:
            click.echo("Environment variable ALMANAK_ENV has an invalid value. Please set it to 'prod' or 'stage'.")
            return

    click.echo(f"Opening {url} in your default browser...")
    webbrowser.open(url)

    click.echo(f"Authenticating against {env.upper()} environment")

    time.sleep(2)

    api_key = pwinput.pwinput(prompt="Please enter your API key: ")
    try:
        Almanak(api_key=api_key, _env=env)
        format_output(
            status="success",
            title="API Key Validation",
            key_value_pairs={"Message": "API key validated successfully."},
        )
    except Exception as e:
        format_output(
            status="error",
            title="API Key Validation Failed",
            key_value_pairs={"Error": str(e)},
        )
        return

    save_api_key(api_key)
    format_output(
        status="success",
        title="API Key Stored",
        key_value_pairs={
            "Message": f"API key for {env.upper()} environment stored successfully. You can now use the Almanak CLI.",
            "Environment": env.upper(),
        },
    )


@strat.command("list")
def list_strategies():
    """List all available strategies on the Almanak platform."""
    try:
        client = initialize_client()

        artifacts_list = client.library.strategies.list()

        if not artifacts_list:
            format_output(status="info", title="No Strategies Found")
            return

        format_output(
            status="success",
            title="Available Strategies:",
            items=[f"{artifact.name} (ID: {artifact.id})" for artifact in artifacts_list],
        )

    except Exception as e:
        format_output(
            status="error",
            title="Failed to Fetch Strategies",
            key_value_pairs={"Error": str(e)},
        )


@strat.command("describe")
@click.option("--strategy-name", required=True, help="The name of the strategy to retrieve.")
@click.option(
    "--version",
    help="Specific version of the strategy to retrieve. If not provided, returns all versions.",
)
def get_strategy(strategy_name, version):
    """Retrieve the details of a strategy. If version is specified, retrieves that specific version."""
    try:
        client = initialize_client()

        if version:
            # Get specific version
            result = client.library.strategies.versions.retrieve(strategy_name, version)
            if not result or not result.data:
                format_output(
                    status="error",
                    title=f"Strategy '{strategy_name}' version '{version}' not found",
                )
                return

            version_info = result.data[0]  # Get the first item from data list

            # Format version-specific output
            format_output(
                status="success",
                title=f"Details for Strategy: {strategy_name} (Version {version})",
                key_value_pairs={
                    "Version": version_info.name,
                    "Author": version_info.author,
                    "Created At": version_info.date_created,
                    "Description": version_info.description or "No description available",
                    "Is Public": "Yes" if version_info.is_public else "No",
                    "Metadata": (json.dumps(version_info.metadata, indent=2) if version_info.metadata else "No metadata"),
                },
            )
        else:
            # Get strategy info and all versions
            strategy_result = client.library.strategies.retrieve(strategy_name)
            versions_result = client.library.strategies.versions.list(strategy_name)

            if not strategy_result or not strategy_result.data:
                format_output(status="error", title=f"Strategy '{strategy_name}' not found")
                return

            strategy = strategy_result.data[0]

            # Prepare versions information
            versions_info = []
            for v in versions_result:
                versions_info.append(
                    f"Version: {v.name}\n"
                    f"   Author: {v.author}\n"
                    f"   Created: {v.date_created}\n"
                    f"   Description: {v.description or 'No description available'}\n"
                    f"   Public: {'Yes' if v.is_public else 'No'}\n"
                    f"   Metadata: {json.dumps(v.metadata, indent=2) if v.metadata else 'No metadata'}"
                )

            format_output(
                status="success",
                title=f"Details for Strategy: {strategy.name}",
                key_value_pairs={
                    "Author": strategy.author,
                    "Description": strategy.description or "No description available",
                    "Public": "Yes" if strategy.is_public else "No",
                    "Created At": strategy.date_created,
                    "Latest Version": strategy.latest_version_artifact.name,
                    "Latest Version Metadata": (json.dumps(strategy.latest_version_artifact.metadata, indent=2) if strategy.latest_version_artifact.metadata else "No metadata"),
                },
                items=versions_info,  # Add all versions as a list
            )

    except Exception as e:
        format_output(
            status="error",
            title="Failed to retrieve strategy",
            key_value_pairs={"Error": str(e)},
        )


def get_ignore_patterns(working_dir, ignore_file=None):
    """
    Get ignore patterns from .almanakignore or .gitignore files.

    Args:
        working_dir (str): The working directory path
        ignore_file (str, optional): Custom ignore file path

    Returns:
        list: List of ignore patterns
    """
    ignore_patterns = []

    # Priority: custom ignore file > .almanakignore > .gitignore
    ignore_files = [
        ignore_file,
        os.path.join(working_dir, ".almanakignore"),
        os.path.join(working_dir, ".gitignore"),
    ]

    for file_path in ignore_files:
        if file_path and os.path.isfile(file_path):
            with open(file_path) as f:
                patterns = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
                ignore_patterns.extend(patterns)
            break  # Use first found ignore file

    # Add default patterns
    default_patterns = [
        ".git/",
        "__pycache__/",
        "*.pyc",
        ".DS_Store",
        ".env",
        ".venv/",
        "venv/",
        ".idea/",
        ".vscode/",
        "local_storage/",
    ]
    ignore_patterns.extend(default_patterns)

    return ignore_patterns


def should_ignore_file(file_path, ignore_patterns):
    """
    Check if a file should be ignored based on ignore patterns.

    Args:
        file_path (str): The file path to check
        ignore_patterns (list): List of ignore patterns

    Returns:
        bool: True if file should be ignored, False otherwise
    """
    file_path = Path(file_path)
    relative_path = str(file_path.as_posix())

    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            # Directory pattern
            if any(parent.name == pattern[:-1] for parent in file_path.parents):
                return True
        elif fnmatch(relative_path, pattern) or fnmatch(file_path.name, pattern):
            return True
    return False


def extract_strategy_parameters_static(file_path: str, strategy_class: str) -> dict[str, Any] | None:
    """
    Extract parameter information from the strategy class using static code analysis.

    Args:
        file_path: Path to the strategy file
        strategy_class: Name of the strategy class to analyze

    Returns:
        Dictionary containing parameter information or None if class not found
    """
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == strategy_class:
                # Find the __init__ method
                init_method = next(
                    (n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == "__init__"),
                    None,
                )

                if not init_method:
                    return {}

                strategy_parameters = {}

                # Skip the first argument (self)
                for arg in init_method.args.args[1:]:
                    param_info = {
                        "optional": False,
                    }

                    # Get type annotation if it exists
                    if arg.annotation:
                        param_info["type"] = ast.unparse(arg.annotation)

                    # Check for default value
                    arg_idx = init_method.args.args.index(arg)
                    defaults_idx = arg_idx - (len(init_method.args.args) - len(init_method.args.defaults))
                    if defaults_idx >= 0:
                        default_value = init_method.args.defaults[defaults_idx]
                        param_info["optional"] = True
                        try:
                            param_info["default"] = ast.literal_eval(default_value)
                        except ValueError:
                            # If we can't evaluate the default value, store it as a string
                            param_info["default"] = ast.unparse(default_value)

                    strategy_parameters[arg.arg] = param_info

                return strategy_parameters

        return None
    except Exception as e:
        raise Exception(f"Failed to extract strategy parameters: {str(e)}")


def validate_strategy_preset(preset: dict, working_dir: Path):
    preset_title = preset.get("title")
    if not preset_title:
        raise ValueError("title not found in preset")
    if not preset.get("description"):
        raise ValueError("description not found in preset")
    if not preset.get("chain"):
        raise ValueError("chain not found in preset")

    strategy_config_path_parts = Path(preset["config"]).parts
    strategy_config_path = working_dir / Path(*strategy_config_path_parts)
    if not strategy_config_path.exists():
        raise ValueError(f"strategy config path {strategy_config_path} does not exist for preset {preset_title}")
    try:
        config_data = json.load(open(strategy_config_path))
        if not config_data:
            raise ValueError(f"strategy config file {strategy_config_path} is empty for preset {preset_title}")
    except Exception as e:
        raise ValueError(f"strategy config file {strategy_config_path} is invalid for preset {preset_title}") from e
    print(f"Validated strategy config file exists for preset {preset_title}")

    permissions_path_parts = Path(preset["permissions"]).parts
    permissions_path = working_dir / Path(*permissions_path_parts)
    if not permissions_path.exists():
        raise ValueError(f"permissions path {permissions_path} does not exist for preset {preset_title}")
    print(f"Validated permissions file exists for preset {preset_title}")

    env_path_parts = Path(preset["env"]).parts
    env_path = working_dir / Path(*env_path_parts)
    if not env_path.exists():
        raise ValueError(f"env path {env_path} does not exist for preset {preset_title}")
    print(f"Validated env file exists for preset {preset_title}")


def validate_pyproject_contents(pyproject_toml: Path, working_dir: str) -> bool:
    pyproject_data = tomllib.load(open(pyproject_toml, "rb"))
    if not pyproject_data.get("tool") or not pyproject_data["tool"].get("presets"):
        format_output(
            status="error",
            title="Validation error",
            key_value_pairs={"Error": "[tool.presets] section not found in pyproject.toml"},
        )
        return False
    if not pyproject_data["tool"] or not pyproject_data["tool"].get("metadata"):
        format_output(
            status="error",
            title="Validation error",
            key_value_pairs={"Error": "[tool.metadata] section not found in pyproject.toml"},
        )
        return False

    if not pyproject_data["tool"]["metadata"].get("human_readable_name"):
        format_output(
            status="error",
            title="Validation error",
            key_value_pairs={"Error": "human_readable_name not found in [tool.metadata]"},
        )
        return False

    strategy_presets = pyproject_data["tool"]["presets"]
    for strategy_preset_name, strategy_preset in strategy_presets.items():
        try:
            validate_strategy_preset(strategy_preset, Path(working_dir))
        except Exception as e:
            format_output(
                status="error",
                title=f"Invalid Strategy Preset: {strategy_preset_name}",
                key_value_pairs={
                    "Error": str(e),
                    "Preset Name": strategy_preset_name,
                },
            )
            return False

    return True

def validate_dashboard_ui(working_dir: str):
    dashboard_ui_path = Path(working_dir) / "dashboard" / "ui.py"
    if not dashboard_ui_path.exists():
        format_output(
            status="info",
            title="Dashboard UI file not found. Skipping dashboard UI validation.",
        )
        return True
    
    try:
        import sys
        import os
        import subprocess
        import tempfile
        import time
        from threading import Thread
        from queue import Queue, Empty
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        original_dir = os.getcwd()
        os.chdir(working_dir)
        local_storage = "./local_storage"
        local_storage_path = Path(local_storage).resolve()
        working_dir = Path(".").resolve()

        if not local_storage_path.exists():
            local_storage_path = Path(working_dir) / ".." / local_storage
            if not local_storage_path.exists():
                format_output(
                    status="success",
                    title="Local storage file not found. Skipping dashboard UI validation.",
                )
                return True


        dashboard_ui_path = working_dir / "dashboard" / "ui.py"
        
        if not dashboard_ui_path.exists():
            format_output(
                status="error",
                title="Dashboard UI file not found",
                key_value_pairs={
                    "Error": f"Could not find dashboard/ui.py in {working_dir}",
                },
            )
            return
        
        print(f"Starting Streamlit server")

        pyproject_file = working_dir / "pyproject.toml"

        pyproject_data = tomllib.loads(open(pyproject_file).read())

        config = json.loads(open(local_storage_path / "config" / "config.json").read())
        strategy_preset_data = None
        for strategy_preset_name, strategy_preset in pyproject_data["tool"]["presets"].items():
            config_path = strategy_preset.get("config")

            config_data = json.loads(open(config_path).read())
            if config_data == config:
                print(f"Found matching preset {strategy_preset_name}")
                strategy_preset_data = strategy_preset
                break

        if not strategy_preset_data:
            strategy_preset_data = list(pyproject_data["tool"]["presets"].values())[0]


        if not strategy_preset_data.get("env"):
            format_output(
                status="error",
                title="Environment file not found",
                key_value_pairs={"Error": "Required environment file not found in the preset"},
            )
            return False
    
    
        env_file_location = Path(working_dir) / Path(strategy_preset_data["env"])
        if not env_file_location.exists():
            format_output(
                status="error",
                title="Environment file not found",
                key_value_pairs={"Error": f"Could not find {env_file_location} in {working_dir}"},
            )
            return False

        load_dotenv(env_file_location)

        db_path = local_storage_path.joinpath("agent.db").absolute()

        if not db_path.exists():
            format_output(
                status="success",
                title="Dashboard UI file is valid",
            )
            return True
    
        os.environ.update(
            {
                "STORAGE_DIR": str(local_storage_path.absolute()),
            }
        )


        port = 44444
                
        # Start the streamlit process in the background
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", str(dashboard_ui_path), 
                "--server.headless=true", f"--server.port={port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Track errors
        error_found = False
        error_messages = []
        
        # Setup queues to capture output
        stdout_queue = Queue()
        stderr_queue = Queue()
        
        def read_output(pipe, queue, is_stderr=False):
            for line in iter(pipe.readline, ''):
                if is_stderr:
                    print(f"\033[91mSTDERR:\033[0m {line.strip()}")
                else:
                    print(f"\033[94mSTDOUT:\033[0m {line.strip()}")
                if any(pattern.lower() in line.lower() for pattern in error_patterns):
                    error_messages.append(line.strip())
                    nonlocal error_found
                    error_found = True
                queue.put(line)
            pipe.close()
        
        # Common error patterns to look for
        error_patterns = [
            "Error:", "Exception:", "Traceback", 
            "ModuleNotFoundError:", "ImportError:", "SyntaxError:",
            "NameError:", "AttributeError:", "TypeError:", "ValueError:",
            "KeyError:", "IndentationError:", "IndexError:", "RuntimeError:",
            "ZeroDivisionError:", "FileNotFoundError:", "PermissionError:",
            "ConnectionError:", "OSError:", "IOError:", "AssertionError:",
            "UnboundLocalError:", "LookupError:", "StopIteration:",
            "RecursionError:", "OverflowError:", "UnicodeError:", "TabError:"
        ]
        
        # Start reader threads
        stdout_thread = Thread(target=read_output, args=(process.stdout, stdout_queue, False))
        stderr_thread = Thread(target=read_output, args=(process.stderr, stderr_queue, True))
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()
        
        # Wait for Streamlit to start
        time.sleep(2)
        
        # Use Selenium to load the page instead of requests
        browser = None
        try:
            print("Starting Chrome in headless mode to test dashboard...")
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            # Create a browser instance
            browser = webdriver.Chrome(options=chrome_options)
            
            # Load the Streamlit app
            url = f"http://localhost:{port}"
            print(f"Loading dashboard at {url}...")
            browser.get(url)
            
            # Wait for page to load completely (wait for Streamlit reactivity)
            time.sleep(5)
            
            # Check if there are any error messages in the browser console
            browser_logs = browser.get_log('browser')
            for log in browser_logs:
                if log['level'] == 'SEVERE':
                    error_messages.append(f"Browser Console Error: {log['message']}")
                    error_found = True
                    print(f"Browser Console Error: {log['message']}")
            
            # Wait to see if loading the page causes any errors (monitoring stdout/stderr)
            print("Waiting for potential errors after page load...")
            error_check_start = time.time()
            while time.time() - error_check_start < 5:  # Wait up to 10 seconds for errors
                # Check if process died
                if process.poll() is not None:
                    print(f"Process exited after page load with code {process.returncode}")
                    error_found = True
                    break
                
                # Already checking stderr in the read_output thread
                if error_found:
                    break
                
                time.sleep(1)
            
            # Final collection of all output
            stdout_data = []
            stderr_data = []
            
            try:
                while True:
                    stdout_data.append(stdout_queue.get_nowait())
            except Empty:
                pass
            
            try:
                while True:
                    stderr_data.append(stderr_queue.get_nowait())
            except Empty:
                pass
            
            stdout_text = "".join(stdout_data)
            stderr_text = "".join(stderr_data)
            
            if error_found or process.returncode != None and process.returncode != 0:
                print("\n=== ERRORS DETECTED ===")
                
                if error_messages:
                    print("Error messages found:")
                    for msg in error_messages:
                        print(f"  {msg}")
                
                format_output(
                    status="error",
                    title="Dashboard UI validation failed",
                    key_value_pairs={
                        "Error": "Found errors in dashboard logs or browser console",
                        "stdout": stdout_text.strip(),
                        "stderr": stderr_text.strip()
                    },
                )
                return False
            
        except Exception as e:
            print(f"Selenium error: {str(e)}")
            error_found = True
            error_messages.append(f"Selenium error: {str(e)}")
            
            # Collect all output
            stdout_data = []
            stderr_data = []
            
            try:
                while True:
                    stdout_data.append(stdout_queue.get_nowait())
            except Empty:
                pass
            
            try:
                while True:
                    stderr_data.append(stderr_queue.get_nowait())
            except Empty:
                pass
            
            stdout_text = "\n".join(stdout_data)
            stderr_text = "\n".join(stderr_data)
            
            format_output(
                status="error",
                title="Dashboard UI validation failed",
                key_value_pairs={
                    "Error": f"Selenium error: {str(e)}",
                    "stdout": stdout_text.strip(),
                    "stderr": stderr_text.strip()
                },
            )
            return False
        finally:
            # Close the browser
            if browser:
                browser.quit()
            
            # Terminate the Streamlit process
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                
    except Exception as e:
        import traceback
        traceback.print_exc()
        format_output(
            status="error",
            title="Dashboard UI validation failed",
            key_value_pairs={"Error": str(e)},
        )
        return False
    
    format_output(
        status="success",
        title="Dashboard UI file is valid",
    )
    return True


@strat.command()
@click.option(
    "--working-dir",
    type=click.Path(exists=True),
    default=".",
    help="Working directory containing the strategy files. Defaults to the current directory.",
)
def validate(working_dir):
    """Validate the strategy file and configuration."""

    strategy_class = "Strategy"
    ignore_file = None
    pip_dependency_file = None
    file_path = os.path.join(working_dir, "strategy.py")

    # Step 1: Check if the strategy file exists
    if not os.path.isfile(file_path):
        format_output(
            status="error",
            title="File Not Found",
            key_value_pairs={
                "Working Directory": working_dir,
                "Strategy Entry File": file_path,
            },
        )
        sys.exit(1)

    try:
        # Get ignore patterns using the provided ignore_file
        ignore_patterns = get_ignore_patterns(working_dir, ignore_file)

        # Get files recursively
        files_to_upload = get_files_to_upload(working_dir, ignore_patterns)

        # Check for pip dependency file
        if pip_dependency_file:
            if os.path.isfile(pip_dependency_file):
                pip_dependency_file = os.path.basename(pip_dependency_file)
            else:
                format_output(
                    status="error",
                    title="Pip Dependency File Not Found",
                    key_value_pairs={
                        "Error": f"Specified pip dependency file '{pip_dependency_file}' not found",
                    },
                )
                return None
        else:
            # Default behavior: look for requirements.txt or requirements.pip
            pip_files = ["requirements.txt", "requirements.pip"]
            pip_dependency_file = next(
                (f for f in pip_files if os.path.isfile(os.path.join(working_dir, f))),
                "",
            )

        """validate pyproject.toml exists"""

        pyproject_toml_path = Path(working_dir) / "pyproject.toml"
        if not pyproject_toml_path.exists():
            format_output(
                status="error",
                title="pyproject.toml Not Found",
                key_value_pairs={
                    "Error": "pyproject.toml not found in the working directory",
                },
            )
            sys.exit(1)

        pyproject_data = tomllib.load(open(pyproject_toml_path, "rb"))
        is_pyproject_toml_valid = validate_pyproject_contents(pyproject_toml_path, working_dir)
        if not is_pyproject_toml_valid:
            format_output(
                status="error",
                title="pyproject.toml validation failed",
                key_value_pairs={"Error": "pyproject.toml validation failed"},
            )
            sys.exit(1)

        validation_result = {
            "pip_dependency_file": pip_dependency_file,
            "files_to_upload": files_to_upload,
            "strategy_class_name": strategy_class,
            "pyproject_data": pyproject_data,
        }

        format_output(
            status="success",
            title="Strategy Validated Successfully",
        )


        if not validate_dashboard_ui(working_dir):
            sys.exit(1)
        
        return validation_result

    except Exception as e:
        format_output(
            status="error",
            title="Validation Error",
            key_value_pairs={"Error": str(e)},
        )
        sys.exit(1)


@strat.command()
@click.argument("strategy_id", required=False)
@click.option(
    "--working-dir",
    type=click.Path(exists=True),
    default=".",
    help="Working directory containing the strategy files. Defaults to the current directory.",
)
def push(working_dir: str, strategy_id: str):
    """Push a new version of your strategy."""

    # Change to the working directory
    original_dir = os.getcwd()
    os.chdir(working_dir)
   
    working_dir = "."
    try:
        retrieved_strategy_id = get_strategy_id_from_almanak(working_dir)
        if not retrieved_strategy_id and not strategy_id:
            format_output(
                status="error",
                title="No strategy ID found associated with that folder",
            )
            sys.exit(1)
        elif retrieved_strategy_id and not strategy_id:
            strategy_id = retrieved_strategy_id

        # First, validate the strategy
        ctx = click.get_current_context()
        validation_result = ctx.invoke(
            validate,
            working_dir=working_dir,
        )

        if not validation_result:
            click.echo("Push aborted due to validation failure.")
            sys.exit(1)

        # Get description from config if not provided via CLI
        strategy_description = validation_result["pyproject_data"]["project"]["description"]
        strategy_presets = validation_result.get("pyproject_data")
        strategy_name = validation_result["pyproject_data"]["tool"]["metadata"]["human_readable_name"]

        safe_wallets_permission = validation_result.get("safe_wallets_permission", [])
        strategy_wallets_requirements = validation_result.get("strategy_wallets_requirements", "{}")
        strategy_parameters = validation_result.get("strategy_parameters", {})

        # Use the pip file from validation if not provided
        pip = validation_result.get("pip_dependency_file")

        # Use the filtered files from validation
        file_paths = [
            str(Path(working_dir).joinpath(f).resolve().relative_to(Path.cwd()))
            for f in validation_result["files_to_upload"]
        ]

        # Initialize client
        client = initialize_client()

        click.echo(f"Pushing strategy '{strategy_name}'...")

        # Parse JSON strings to dicts
        strategy_wallets_requirements_dict = json.loads(strategy_wallets_requirements)

        # Get relative paths for config and strategy files
        working_dir_path = Path(working_dir)

        # relative_config_path = str(config_path.relative_to(working_dir_path))
        relative_strategy_path = str(Path(os.path.join(working_dir, "strategy.py")).relative_to(working_dir_path))
        metadata = {
            "safe_wallets_permission": safe_wallets_permission,
            "strategy_wallets_requirements": strategy_wallets_requirements_dict,
            "strategy_parameters": strategy_parameters,
            "strategy_class_name": "Strategy",
            "strategy_file_entrypoint": relative_strategy_path,
            # "config_file_path": relative_config_path,
            "strategy_presets": strategy_presets,
        }

        # Check for pip dependency file
        if pip:
            if os.path.isfile(os.path.join(working_dir, pip)):
                metadata["pip_dependency_file"] = pip
            else:
                click.echo(f"Warning: Specified pip dependency file '{pip}' not found.")

        pushed_strategy = client.strategy.upload_new_version(strategy_id, file_paths)

        client.strategy.update_strategy_version(
            strategy_id,
            pushed_strategy.versionId,
            metadata,
            strategy_description,
        )

        try:
            # Trigger scan
            resp = client.strategy.trigger_scan(artifact_version_id=pushed_strategy.versionId)
            if not resp["success"]:
                click.echo(f"Failed to trigger the security scan due to {resp.message}")
            click.echo("Triggered security scan successfully")
        except Exception as e:
            format_output(
                status="error",
                title=f"Failed to trigger security scan for strategy '{strategy_name} but the strategy was pushed successfully",
                key_value_pairs={"Error": str(e)},
            )

        os.chdir(original_dir)

        save_strategy_id_to_almanak(strategy_id, working_dir)
        format_output(
            status="success",
            title=f"Pushed strategy '{strategy_name}' successfully with version '{pushed_strategy.version}'.",
        )
    except json.JSONDecodeError:
        format_output(
            status="error",
            title="Invalid JSON input",
            key_value_pairs={"Error": "Please provide valid JSON for safe_wallets_permission and strategy_wallets_requirements."},
        )
        sys.exit(1)
    except Exception as e:
        format_output(
            status="error",
            title=f"Failed to push strategy '{strategy_name}'",
            key_value_pairs={"Error": str(e)},
        )
        sys.exit(1)


# Replace the existing code that gets files_to_upload with this new implementation
def get_files_to_upload(working_dir: str, ignore_patterns: list) -> list:
    """
    Recursively get all files to upload, respecting ignore patterns.
    Skips files without extensions and .gitignore files.

    Args:
        working_dir (str): Working directory path
        ignore_patterns (list): List of ignore patterns

    Returns:
        list: List of relative file paths to upload
    """
    files_to_upload = []
    working_dir_path = Path(working_dir)

    for root, dirs, files in os.walk(working_dir):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if not should_ignore_file(os.path.join(root, d), ignore_patterns)]

        for file in files:
            # Skip files without extensions and .gitignore
            if "." not in file or file == ".gitignore":
                continue

            file_path = os.path.join(root, file)
            if not should_ignore_file(file_path, ignore_patterns):
                # Get path relative to working directory
                relative_path = str(Path(file_path).relative_to(working_dir_path))
                files_to_upload.append(relative_path)

    return files_to_upload


@strat.command()
@click.argument("strategy_id", required=True)
@click.option("--version", help="Specific version of the strategy to download.")
@click.option(
    "--working-dir",
    type=click.Path(exists=True),
    default=".",
    help="Working directory to download the strategy to. Defaults to the current directory.",
)
def pull(strategy_id: str, version: str, working_dir: str):
    """Downloads your strategy."""
    try:
        client = initialize_client()
        artifacts_list = client.library.strategies.list()
        if not artifacts_list:
            format_output(status="error", title="No Strategies Found")
            return
        latest_version = None
        strategy_name = None
        is_empty_strategy = False
        for artifact in artifacts_list:
            if artifact.id == strategy_id:
                strategy_name = artifact.name
                if not artifact.latest_version_artifact:
                    is_empty_strategy = True
                    break
                latest_version = artifact.latest_version_artifact.name
                version_id = artifact.latest_version_artifact.id
                break

        if not is_empty_strategy:
            if version is not None:
                version_id = client.strategy.get_version_id_by_name(strategy_id, version)
            else:
                version = latest_version if latest_version else None

            if strategy_name is None:
                format_output(status="error", title=f"Strategy not found")
                return
            click.echo(f"Downloading version: {version}")

            strategy_download_dir = client.strategy.download_strategy(strategy_name, strategy_id, version_id, working_dir)
        else:
            os.makedirs(f"{working_dir}/{strategy_name}", exist_ok=True)

            strategy_download_dir = f"{working_dir}/{strategy_name}"

        # Save strategy ID to .almanak file
        save_strategy_id_to_almanak(strategy_id, strategy_download_dir)

        format_output(
            status="success",
            title="Strategy downloaded successfully",
            key_value_pairs={
                "Destination": strategy_download_dir,
                "Version": version,
                "Strategy ID": strategy_id,
                "Strategy Name": strategy_name,
            },
        )

    except Exception as e:
        format_output(
            status="error",
            title="Failed to download the strategy",
            key_value_pairs={"Error": str(e)},
        )
        sys.exit(1)

@strat.command()
@click.option(
    "--working-dir",
    type=click.Path(exists=True),
    default=".",
    help="Working directory to create a new skeleton strategy. Defaults to the current directory.",
)
def new(working_dir):
    """Create a new skeleton strategy."""
    try:
        full_path = os.path.abspath(working_dir)

        source_dir = os.path.join(os.path.dirname(__file__), "../templates/new")
        strategy_name = click.prompt("Enter a name for your strategy")
        destination_dir = f"{working_dir}/{strategy_name}"
        config_file = os.path.join(destination_dir, "config.json")
        pyproject_file = os.path.join(destination_dir, "pyproject.toml")

        if os.path.exists(source_dir):
            shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
        else:
            raise FileNotFoundError(f"Source directory {source_dir} does not exist")

        # overwrite strategy name in config file
        if os.path.exists(config_file):
            with open(config_file) as f:
                config = json.load(f)
            config["name"] = strategy_name
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)

        # update project name in pyproject.toml
        if os.path.exists(pyproject_file):
            with open(pyproject_file) as f:
                content = f.read()
            # Replace the project.name line while preserving formatting
            content = re.sub(r'^name = ".*"', f'name = "{strategy_name}"', content, flags=re.M)
            with open(pyproject_file, "w") as f:
                f.write(content)

        format_output(
            status="success",
            title="New strategy skeleton created successfully",
            key_value_pairs={
                "Destination": full_path,
            },
        )

    except Exception as e:
        format_output(
            status="error",
            title="Failed to create a new strategy",
            key_value_pairs={"Error": str(e)},
        )
        sys.exit(1)


@strat.command()
@click.option(
    "--working-dir",
    type=click.Path(exists=True),
    default=".",
    help="Working directory to download the example strategy. Defaults to the current directory.",
)
@click.option(
    "--strategy-name",
    default="tutorial_uniswap_swap",
    type=click.Choice(["tutorial_uniswap_swap", "tutorial_hello_world"]),
    help="The name of the example strategy to download. Defaults to 'tutorial_uniswap_swap'.",
)
def example(working_dir, strategy_name: str):
    """Download the example/tutorial strategies."""
    try:
        working_dir_path = Path(working_dir).resolve()
        # Get the templates directory relative to this file
        current_file = Path(__file__).resolve()
        source_dir = current_file.parent.parent.joinpath("templates").joinpath(strategy_name)
        destination_dir = working_dir_path.joinpath(strategy_name)

        if source_dir.exists():
            shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
        else:
            raise FileNotFoundError(f"Source directory {source_dir} does not exist")

        format_output(
            status="success",
            title="Example strategy created successfully",
            key_value_pairs={
                "Destination": str(destination_dir),
            },
        )

    except Exception as e:
        format_output(
            status="error",
            title="Failed to create example strategy",
            key_value_pairs={"Error": str(e)},
        )
        sys.exit(1)

@strat.command("test")
@click.option(
    "--working-dir",
    type=click.Path(exists=True),
    default=".",
    help="Working directory containing the strategy files. Defaults to the current directory.",
)
@click.option(
    "--preset",
    type=str,
    required=True,
    help="Select the strategy preset to test with.",
)
@click.option(
    "--local-storage",
    type=click.Path(),
    default="./local_storage",
    help="Path to the local storage directory for testing.",
)
@click.option(
    "--clean-restart",
    is_flag=True,
    default=False,
    help="Clean the local storage and restart the strategy.",
)
def strategy_test(working_dir, preset, local_storage, clean_restart):
    """Test the strategy locally.
    The following environment variables must be set:
    - ALCHEMY_API_KEY : Your Alchemy API key. This will be used to connect with the node provider
    - PRIVATE_KEY_*: Private keys for the EOA wallets. E.g. PRIVATE_KEY_1
    """

    """Validate required environment variables"""

    pyproject_data = tomllib.loads(open(Path(working_dir) / "pyproject.toml").read())

    """copy the current working directory containing the strategy into the framework"""
    strategy_package_name: str = pyproject_data["project"]["name"]

    import importlib.util

    almanak_src_spec = importlib.util.find_spec("src")
    if not almanak_src_spec:
        raise FileNotFoundError("almanak-src module not found")

    framework_location = Path(almanak_src_spec.origin).parent
    strategy_location = (framework_location / "strategy" / "strategies" / strategy_package_name).resolve()
    if strategy_location.exists():
        shutil.rmtree(strategy_location)
    shutil.copytree(working_dir, strategy_location)

    local_storage_directory = Path(local_storage).resolve()

    """nuke local storage directory if clean restart is set"""
    if clean_restart:
        if click.confirm(f"Cleaning the local storage directory {local_storage_directory}. Do you confirm?"):
            shutil.rmtree(local_storage_directory, ignore_errors=True)
        else:
            print("Aborting test.")
            sys.exit()

    """Create the local storage directory if it does not exist"""
    if not local_storage_directory.exists():
        local_storage_directory.mkdir(parents=True)

    config_directory = local_storage_directory / "config"

    """Create the config directory in the local storage directory"""
    config_directory.mkdir(exist_ok=True)

    strategy_preset_data = pyproject_data["tool"]["presets"][preset]

    """copy the config file from the preset into the config directory if it does not exist"""
    config_file_location = config_directory / "config.json"
    config_file_in_preset_directory = Path(working_dir) / Path(strategy_preset_data["config"])
    shutil.copy(
        config_file_in_preset_directory,
        config_file_location,
    )

    """Get config, environment variables and permissions from the selected preset used in this test run"""
    if not strategy_preset_data.get("env"):
        raise ValueError("Required environment file not found in the preset")

    env_file_location = Path(working_dir) / Path(strategy_preset_data["env"])
    load_dotenv(env_file_location)

    """Set environment variables to configure stack for local testing"""
    os.environ.update(
        {
            "ALMANAK_IS_AGENT_DEPLOYMENT": "False",
            "DEBUG_AUTO_UPLOAD_PSTATE_FILE": "True",
            "MAINLOOP_DELAY_SECONDS": "1",
            "STORAGE_DIR": local_storage,
        }
    )

    """set strategy directory"""
    """The below code mints tokens into the user wallet. We will not enable this functionality for now."""
    # from transaction_builder.protocols.uniswap_v3 import abis
    # from almanak.utils.utils import mint

    # erc20 = resources.files(abis) / "erc20_token.json"
    # with open(erc20, "r") as abi_file:
    #     erc20_abi = json.loads(abi_file.read())
    # if "test_tokens" in config:
    #     tokens: list[dict] = config["test_tokens"]
    #     for token in tokens:
    #         mint(
    #             strategy_parameters["web3"],
    #             strategy_parameters["wallet_address"],
    #             token["amount"],
    #             token["name"],
    #             token["address"],
    #             erc20_abi,
    #         )
    """start the stack as per normal"""
    from src.main import super_main

    super_main()


def is_anvil_running(url="http://127.0.0.1:8545"):
    payload = {"jsonrpc": "2.0", "method": "web3_clientVersion", "params": [], "id": 1}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                print(f"Anvil is running. Client version: {result['result']}")
                return True
        print(f"Failed to validate Anvil. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Anvil: {e}")

    return False



@dashboard.command("test")
@click.option("--working-dir", type=click.Path(exists=True), default=".", help="Working directory containing the strategy files. Defaults to the current directory.")
@click.option("--local-storage", type=click.Path(), default="./local_storage", help="Path to the local storage directory for testing.")
@click.option("--server-port", type=int, default=8501, help="Port to run the Streamlit server on. Defaults to 8501.")
@click.option("--preset", type=str, required=True, help="Preset to use for the dashboard.")
def dashboard_test(working_dir, local_storage, server_port, preset):
    """Test the dashboard locally using Streamlit."""
    try:
        local_storage_path = Path(local_storage).resolve()
        original_dir = os.getcwd()
        os.chdir(working_dir)

        working_dir = Path(".").resolve()

        dashboard_ui_path = working_dir / "dashboard" / "ui.py"
        
        if not dashboard_ui_path.exists():
            format_output(
                status="error",
                title="Dashboard UI file not found",
                key_value_pairs={
                    "Error": f"Could not find dashboard/ui.py in {working_dir}",
                },
            )
            sys.exit(1)

        format_output(
            status="success",
            title="Starting Streamlit server",
            key_value_pairs={
                "Dashboard UI": str(dashboard_ui_path),
                "Working Directory": str(working_dir),
            },
        )

        pyproject_file = working_dir / "pyproject.toml"
        if not pyproject_file.exists():
            format_output(
                status="error",
                title="pyproject.toml file not found",
                key_value_pairs={"Error": f"Could not find pyproject.toml in {working_dir}"},
            )
            sys.exit(1)

        pyproject_data = tomllib.loads(open(pyproject_file).read())

        strategy_preset_data = pyproject_data["tool"]["presets"][preset]

        if not strategy_preset_data.get("env"):
            raise ValueError("Required environment file not found in the preset")
    
        env_file_location = Path(working_dir) / Path(strategy_preset_data["env"])
        if not env_file_location.exists():
            format_output(
                status="error",
                title="Environment file not found",
                key_value_pairs={"Error": f"Could not find {env_file_location} in {working_dir}"},
            )
            sys.exit(1)

        load_dotenv(env_file_location)

        db_path = local_storage_path.joinpath("agent.db").absolute()

        if not db_path.exists():
            format_output(
                status="error",
                title="Database file not found",
                key_value_pairs={"Error": f"Could not find agent.db in {local_storage_path}"},
            )
            sys.exit(1)
    
        os.environ.update(
            {
                "STORAGE_DIR": str(local_storage_path.absolute()),
            }
        )

        # Run streamlit server
        import streamlit.web.cli as stcli
        
        # Save original sys.argv
        original_argv = sys.argv
        
        # Set up streamlit arguments
        sys.argv = [
            "streamlit",
            "run",
            str(dashboard_ui_path),
            f"--server.port={server_port}",
        ]
        
        try:
            stcli.main()
        except KeyboardInterrupt:
            format_output(
                status="info",
                title="Streamlit server stopped",
                key_value_pairs={
                    "Message": "Server stopped gracefully",
                },
            )
        finally:
            # Restore original sys.argv
            sys.argv = original_argv

        os.chdir(original_dir)
    except Exception as e:
        format_output(
            status="error",
            title="Failed to start dashboard",
            key_value_pairs={"Error": str(e)},
        )
        sys.exit(1)


if __name__ == "__main__":
    almanak()
