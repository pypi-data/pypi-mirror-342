import typer
from .service import DocsService

docs_app = typer.Typer(
    help="문서(docs) 관리 명령어. 문서 생성, 프로필 목록 조회 등 기능 제공.",
    no_args_is_help=True,
)


@docs_app.command("profile-list")
def profile_list_cmd():
    """프로필 목록을 출력합니다. 프로필에 따라 문서 목록이 달라집니다."""
    service = DocsService()
    print("🔍 사용 가능한 프로필:")
    for profile in service.list_profiles():
        print(f"- {profile}")


@docs_app.command("sync")
def sync_cmd():
    """프로필에 따라 문서 목록을 동기화합니다."""
    service = DocsService()
    service.sync()


@docs_app.command("pull")
def pull_cmd(profile: str = typer.Option(..., "--profile")):
    """프로필에 따라 문서 목록을 동기화합니다."""
    service = DocsService()
    service.pull(profile)


@docs_app.command("push")
def push_cmd(profile: str = typer.Option(..., "--profile")):
    """프로필에 따라 문서 목록을 동기화합니다."""
    service = DocsService()
    service.push(profile)
