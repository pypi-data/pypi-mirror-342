import typer
from typing import Optional

mcp_app = typer.Typer(
    help="MCP 서버 관리 명령어. add/list 등 기능 제공.",
    no_args_is_help=True,
)


@mcp_app.command("add")
def add_cmd(name: Optional[str] = None, token: Optional[str] = None):
    """MCP 서버를 등록합니다."""
    print(f"[예시] MCP 서버 {name} 등록 (token: {token})")


@mcp_app.command("list")
def list_cmd():
    """등록된 MCP 서버 목록을 출력합니다."""
    print("[예시] 등록된 MCP 서버 목록을 출력합니다.")
