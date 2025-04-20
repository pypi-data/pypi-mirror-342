from pathlib import Path
import importlib.resources
import shutil
import os


def get_template_file_path(name: str):
    return Path.cwd() / "templates" / name


def get_template_dir_path(name: str):
    return Path.cwd() / "templates" / name


def get_target_rules_file():
    return Path.cwd() / ".cursorrules"


def get_target_rules_dir():
    return Path.cwd() / ".cursor" / "rules"


def get_target_docs_dir():
    return Path.cwd() / "docs"


def get_target_ontology_dir():
    return Path.cwd() / ".cursor" / "ontology"


def print_success(msg):
    print(f"\033[92m{msg}\033[0m")


def print_error(msg):
    print(f"\033[91m{msg}\033[0m")


def confirm_overwrite(path):
    answer = input(f"{path} 파일이 이미 존재합니다. 덮어쓰시겠습니까? [y/N]: ")
    return answer.strip().lower() == "y"


def safe_copy(src, dst, overwrite=False):
    if os.path.isdir(src):
        if os.path.exists(dst) and overwrite:
            shutil.rmtree(dst)
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
    else:
        if not os.path.exists(dst) or overwrite:
            shutil.copy(src, dst)


def safe_remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)
