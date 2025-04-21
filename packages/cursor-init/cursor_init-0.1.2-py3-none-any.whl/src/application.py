import typer
from src.services.docs.typer import docs_app as docs_app
from src.services.mcp.typer import mcp_app as mcp_app

app = typer.Typer()
app.add_typer(docs_app, name="docs")
app.add_typer(mcp_app, name="mcp")
