import typer
from cursor_init.services.docs.typer import docs_app as docs_app
from cursor_init.services.mcp.typer import mcp_app as mcp_app

app = typer.Typer(
    no_args_is_help=True,
    help="Cursor 프로젝트를 관리하는 프로그램입니다.",
)
app.add_typer(docs_app, name="docs")
app.add_typer(mcp_app, name="mcp")
