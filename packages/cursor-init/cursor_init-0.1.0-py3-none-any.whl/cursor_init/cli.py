import typer
from .core import init_project
from .utils import print_success, print_error

app = typer.Typer()


@app.command()
def init(force: bool = typer.Option(False, "--force", "-f", help="기존 파일 덮어쓰기")):
    """프로젝트에 규칙 템플릿을 세팅합니다."""
    result = init_project(force=force)
    if result["success"]:
        print_success("✅ 템플릿 파일이 성공적으로 복사되었습니다.")
    else:
        print_error("❌ 일부 파일 복사에 실패했습니다:")
        for err in result["errors"]:
            print_error(f"  - {err}")


if __name__ == "__main__":
    app()
