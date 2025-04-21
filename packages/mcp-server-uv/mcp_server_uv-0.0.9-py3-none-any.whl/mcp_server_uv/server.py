import logging
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)
from enum import Enum
from pydantic import BaseModel
import subprocess
from typing import List, Optional
import os

class UVPipList(BaseModel):
    project_path: str

class UVPipInstall(BaseModel):
    project_path: str
    packages: List[str]
    dev: bool = False

class UVPipUninstall(BaseModel):
    project_path: str
    packages: List[str]

class UVPipUpgrade(BaseModel):
    project_path: str
    packages: Optional[List[str]] = None

class UVPipCompile(BaseModel):
    project_path: str
    requirements_file: str = "requirements.txt"

class UVPipSync(BaseModel):
    project_path: str

class UVInit(BaseModel):
    project_path: str
    name: str

class UVAdd(BaseModel):
    project_path: str
    packages: List[str]
    dev: bool = False

class UVTree(BaseModel):
    project_path: str
    package: Optional[str] = None

class UVLock(BaseModel):
    project_path: str

class UVRun(BaseModel):
    project_path: str
    command: str

class UVBuild(BaseModel):
    project_path: str

class UVPublish(BaseModel):
    project_path: str
    repository: Optional[str] = None

class UVRemove(BaseModel):
    project_path: str
    packages: List[str]
    dev: bool = False

class UVSync(BaseModel):
    project_path: str

class UVTools(str, Enum):
    PIP_LIST = "uv_pip_list"
    PIP_INSTALL = "uv_pip_install"
    PIP_UNINSTALL = "uv_pip_uninstall"  # Changed from PIP_REMOVE
    PIP_UPGRADE = "uv_pip_upgrade"
    PIP_COMPILE = "uv_pip_compile"
    PIP_SYNC = "uv_pip_sync"
    INIT = "uv_init"
    ADD = "uv_add"
    REMOVE = "uv_remove"
    SYNC = "uv_sync"  # Changed: now using dedicated uv sync command
    LOCK = "uv_lock"
    RUN = "uv_run"
    TREE = "uv_tree"
    BUILD = "uv_build"
    PUBLISH = "uv_publish"

def run_uv_command(cmd: List[str], cwd: str) -> str:
    try:
        # Add colors to the output for better readability
        env = {"FORCE_COLOR": "1", **dict(os.environ)}
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True, env=env)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        logging.error(f"UV command failed: {' '.join(cmd)}\nError: {error_msg}")
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Unexpected error running UV command: {' '.join(cmd)}\nError: {error_msg}")
        return f"Error: {error_msg}"

def uv_pip_list(project_path: str) -> str:
    """List installed packages."""
    return run_uv_command(["uv", "pip", "list", "--include-editable"], project_path)

def uv_pip_install(project_path: str, packages: List[str], dev: bool = False) -> str:
    """Install Python packages using UV."""
    cmd = ["uv", "pip", "install"]
    if dev:
        cmd.append("--dev")
    cmd.extend(packages)
    return run_uv_command(cmd, project_path)

def uv_pip_uninstall(project_path: str, packages: List[str]) -> str:
    """Remove Python packages using UV pip uninstall."""
    cmd = ["uv", "pip", "uninstall", "--yes"]
    cmd.extend(packages)
    return run_uv_command(cmd, project_path)

def uv_pip_upgrade(project_path: str, packages: Optional[List[str]] = None) -> str:
    """Upgrade Python packages using UV."""
    cmd = ["uv", "pip", "install", "--upgrade"]
    if packages:
        cmd.extend(packages)
    else:
        cmd.append("--all")
    return run_uv_command(cmd, project_path)

def uv_pip_compile(project_path: str, requirements_file: str = "requirements.txt", upgrade: bool = False, generate_hashes: bool = True) -> str:
    """Compile requirements.txt using UV with enhanced security features."""
    cmd = ["uv", "pip", "compile"]
    if upgrade:
        cmd.append("--upgrade")
    if generate_hashes:
        cmd.append("--generate-hashes")
    # Use relative path
    cmd.append(os.path.basename(requirements_file))
    return run_uv_command(cmd, project_path)

def uv_pip_sync(project_path: str, requirements_file: str = "requirements.txt") -> str:
    """Synchronize virtual environment with requirements.txt."""
    cmd = ["uv", "pip", "sync"]
    # Use relative path
    cmd.append(os.path.basename(requirements_file))
    return run_uv_command(cmd, project_path)

def uv_sync(project_path: str) -> str:
    """Sync project dependencies based on pyproject.toml and lockfile."""
    return run_uv_command(["uv", "sync"], project_path)

def uv_init(project_path: str, name: str) -> str:
    """Initialize a new Python project with UV."""
    return run_uv_command(["uv", "init", name], project_path)

def uv_add(project_path: str, packages: List[str], dev: bool = False) -> str:
    """Add dependencies to the project using UV."""
    cmd = ["uv", "add"]
    if dev:
        cmd.append("--dev")
    cmd.extend(packages)
    return run_uv_command(cmd, project_path)

def uv_remove(project_path: str, packages: List[str], dev: bool = False) -> str:
    """Remove dependencies from the project's pyproject.toml using UV."""
    cmd = ["uv", "remove"]
    if dev:
        cmd.append("--dev")
    cmd.extend(packages)
    return run_uv_command(cmd, project_path)

def uv_lock(project_path: str) -> str:
    """Create or update the project's lockfile."""
    return run_uv_command(["uv", "lock"], project_path)

def uv_run(project_path: str, command: str) -> str:
    """Run a command in the project environment."""
    import shlex
    # Use shlex.split for safer command splitting
    cmd = ["uv", "run"] + shlex.split(command)
    return run_uv_command(cmd, project_path)

def uv_tree(project_path: str, package: Optional[str] = None) -> str:
    """View the dependency tree for the project or a specific package."""
    cmd = ["uv", "tree"]
    if package:
        cmd.append(package)
    return run_uv_command(cmd, project_path)

def uv_build(project_path: str) -> str:
    """Build the project into distribution archives."""
    return run_uv_command(["uv", "build"], project_path)

def uv_publish(project_path: str, repository: Optional[str] = None) -> str:
    """Publish the project to a package index."""
    cmd = ["uv", "publish"]
    if repository:
        cmd.extend(["--repository", repository])
    return run_uv_command(cmd, project_path)

async def serve() -> None:
    logger = logging.getLogger(__name__)

    server = Server("mcp-git")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=UVTools.PIP_LIST,
                description="Lists installed packages in JSON format",
                inputSchema=UVPipList.model_json_schema(),
            ),
            Tool(
                name=UVTools.PIP_INSTALL,
                description="Install Python packages using UV",
                inputSchema=UVPipInstall.model_json_schema(),
            ),
            Tool(
                name=UVTools.PIP_UNINSTALL,  # Changed from PIP_REMOVE
                description="Remove Python packages from virtual environment using UV pip uninstall",
                inputSchema=UVPipUninstall.model_json_schema(),  # Changed from UVPipRemove
            ),
            Tool(
                name=UVTools.PIP_UPGRADE,
                description="Upgrade Python packages using UV",
                inputSchema=UVPipUpgrade.model_json_schema(),
            ),
            Tool(
                name=UVTools.PIP_COMPILE,
                description="Compile requirements.txt using UV",
                inputSchema=UVPipCompile.model_json_schema(),
            ),
            Tool(
                name=UVTools.PIP_SYNC,
                description="Synchronize virtual environment with requirements.txt using UV pip sync",
                inputSchema=UVPipSync.model_json_schema(),
            ),
            Tool(
                name=UVTools.SYNC,
                description="Synchronize project dependencies based on pyproject.toml and lockfile",
                inputSchema=UVSync.model_json_schema(),
            ),
            Tool(
                name=UVTools.INIT,
                description="Initialize a new Python project",
                inputSchema=UVInit.model_json_schema(),
            ),
            Tool(
                name=UVTools.ADD,
                description="Add dependencies to the project",
                inputSchema=UVAdd.model_json_schema(),
            ),
            Tool(
                name=UVTools.REMOVE,
                description="Remove dependencies from pyproject.toml using UV remove",
                inputSchema=UVRemove.model_json_schema(),
            ),
            Tool(
                name=UVTools.LOCK,
                description="Create or update the project's lockfile",
                inputSchema=UVLock.model_json_schema(),
            ),
            Tool(
                name=UVTools.RUN,
                description="Run a command in the project environment",
                inputSchema=UVRun.model_json_schema(),
            ),
            Tool(
                name=UVTools.TREE,
                description="View the dependency tree for the project",
                inputSchema=UVTree.model_json_schema(),
            ),
            Tool(
                name=UVTools.BUILD,
                description="Build the project into distribution archives",
                inputSchema=UVBuild.model_json_schema(),
            ),
            Tool(
                name=UVTools.PUBLISH,
                description="Publish the project to a package index",
                inputSchema=UVPublish.model_json_schema(),
            ),
        ]
    
    @server.call_tool()
    async def call_tool(name: str, args: dict) -> list[TextContent]:
        project_path = Path(args["project_path"])
        match name:
            case UVTools.PIP_LIST:
                result = uv_pip_list(str(project_path))
                return [TextContent(
                    type="text",
                    text=f"Installed packages:\n{result}"
                )]

            case UVTools.PIP_INSTALL:
                result = uv_pip_install(
                    str(project_path),
                    args["packages"],
                    args.get("dev", False)
                )
                return [TextContent(
                    type="text",
                    text=f"Installation result:\n{result}"
                )]

            case UVTools.PIP_UNINSTALL:  # Changed from PIP_REMOVE
                result = uv_pip_uninstall(str(project_path), args["packages"])
                return [TextContent(
                    type="text",
                    text=f"Package uninstall result:\n{result}"
                )]

            case UVTools.REMOVE:
                result = uv_remove(
                    str(project_path),
                    args["packages"],
                    args.get("dev", False)
                )
                return [TextContent(
                    type="text",
                    text=f"Package removal from pyproject.toml result:\n{result}"
                )]

            case UVTools.PIP_UPGRADE:
                result = uv_pip_upgrade(
                    str(project_path),
                    args.get("packages")
                )
                return [TextContent(
                    type="text",
                    text=f"Upgrade result:\n{result}"
                )]

            case UVTools.PIP_COMPILE:
                result = uv_pip_compile(
                    str(project_path),
                    args.get("requirements_file", "requirements.txt"),
                    args.get("upgrade", False),
                    args.get("generate_hashes", True)
                )
                return [TextContent(
                    type="text",
                    text=f"Compilation result:\n{result}"
                )]

            case UVTools.PIP_SYNC:
                result = uv_pip_sync(
                    str(project_path),
                    args.get("requirements_file", "requirements.txt")
                )
                return [TextContent(
                    type="text",
                    text=f"Requirements sync result:\n{result}"
                )]

            case UVTools.SYNC:
                result = uv_sync(str(project_path))
                return [TextContent(
                    type="text",
                    text=f"Project dependencies sync result:\n{result}"
                )]

            case UVTools.INIT:
                result = uv_init(str(project_path), args["name"])
                return [TextContent(
                    type="text",
                    text=f"Project initialization result:\n{result}"
                )]

            case UVTools.ADD:
                result = uv_add(
                    str(project_path),
                    args["packages"],
                    args.get("dev", False)
                )
                return [TextContent(
                    type="text",
                    text=f"Package addition result:\n{result}"
                )]

            case UVTools.LOCK:
                result = uv_lock(str(project_path))
                return [TextContent(
                    type="text",
                    text=f"Lock file update result:\n{result}"
                )]

            case UVTools.RUN:
                result = uv_run(str(project_path), args["command"])
                return [TextContent(
                    type="text",
                    text=f"Command execution result:\n{result}"
                )]

            case UVTools.TREE:
                result = uv_tree(
                    str(project_path),
                    args.get("package")
                )
                return [TextContent(
                    type="text",
                    text=f"Dependency tree:\n{result}"
                )]

            case UVTools.BUILD:
                result = uv_build(str(project_path))
                return [TextContent(
                    type="text",
                    text=f"Build result:\n{result}"
                )]

            case UVTools.PUBLISH:
                result = uv_publish(
                    str(project_path),
                    args.get("repository")
                )
                return [TextContent(
                    type="text",
                    text=f"Publish result:\n{result}"
                )]

            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

 
    
