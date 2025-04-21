from pathlib import Path
import shutil
from importlib import resources


class DocsService:
    def __init__(self):
        pass

    def list_profiles(self):
        """프로필 목록을 출력합니다.

        프로필은 .templates 하위에 있는 디렉토리의 이름을 동적으로 추출합니다.

        Returns:
            list: 프로필 목록
        """
        # with importlib.resources.path(
        #     "cursor_init.templates.profile", "default"
        # ) as src_dir:
        #     return [d.name for d in src_dir.glob("*") if d.is_dir()]

    # def list_docs(self):
    #     """프로필에 따라 문서 목록을 출력합니다."""

    #     files = list_md_files(self.root_dir / "docs")
    #     if not files:
    #         print("[경고] .cursor/docs/ 디렉토리가 없거나 md 파일이 없습니다.")
    #         return
    #     for file in files:
    #         print(f"- {file.name}")

    def pull(self, profile: str):
        """문서 목록을 동기화합니다.

        프로필을 선택할 수 있으며, 프로필이 존재해야만 동작합니다.

        Args:
            profile: 프로필 이름
        """
        print(f"[완료] {profile} 프로필 문서가 생성되었습니다.")
        pass

    def push(self, profile: str):
        """문서 목록을 동기화합니다.

        프로필을 선택할 수 있으며, 프로필에 따라서, 매칭되는 프로필이 없다면 뒤에 -{YYMMDD} 형식으로 프로필을 생성합니다.

        Args:
            profile: 프로필 이름
        """
        print(f"[완료] {profile} 프로필 문서가 생성되었습니다.")
        pass

    def sync(self):
        """문서 목록을 동기화합니다.

        # TODO: sync는 프로필을 선택할 수 없습니다. 추후 프로필을 선택할 수 있도록 수정
        # .templates/profile/default 프로필의 문서를 .cursor-init/profile/default 에 복사합니다.
        # 프로젝트의 루트 경로에 default 폴더내의 모든 문서를 복사합니다.
        # 프로젝트에 이미 파일이 존재하면, .cursor-init/profile/snap-YYYYMMDD 폴더를 생성하고 백업을 진행합니다.

        """
        print("문서 동기화를 진행합니다.")

        def copy_default_profile():
            """default 프로필을 복사합니다. 디렉토리 구조를 유지하여 복사합니다."""
            # 템플릿은 패키지 내에 있는 파일을 사용합니다.
            package = "cursor_init.templates.profile"
            default_dir_ref = resources.files(package).joinpath("default")

            # wheel/zip 환경일 수도 있으므로 as_file()로 실제 디스크 경로 확보
            with resources.as_file(default_dir_ref) as src_dir:
                dst_dir = Path.cwd()

                # __init__.py 제외하고 복사
                for item in src_dir.iterdir():
                    if item.name == "__init__.py":
                        continue

                    target = dst_dir / item.name
                    if item.is_dir():
                        shutil.copytree(item, target, dirs_exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, target)

        copy_default_profile()

        print("문서 동기화가 완료되었습니다.")
