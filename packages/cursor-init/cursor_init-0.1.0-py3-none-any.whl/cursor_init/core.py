from .utils import (
    get_template_file_path,
    get_template_dir_path,
    get_target_rules_file,
    get_target_rules_dir,
    get_target_docs_dir,
    confirm_overwrite,
    safe_copy,
    safe_remove,
    get_target_ontology_dir,
)
from pathlib import Path


def copy_with_confirm(src_ctx, dst, force, label, errors):
    try:
        with src_ctx as src:
            if dst.exists() and not force:
                if not confirm_overwrite(dst):
                    errors.append(f"{label}: 사용자에 의해 건너뜀")
                    return False
                else:
                    safe_copy(src, dst, overwrite=True)
            else:
                safe_copy(src, dst, overwrite=force)
        return True
    except Exception as e:
        errors.append(f"{label}: {e}")
        return False


def init_project(force: bool = False):
    errors: list[str] = []
    success = True

    copy_targets = [
        {
            "src_ctx": get_template_file_path(".cursorrules"),
            "dst": get_target_rules_file(),
            "label": ".cursorrules",
        },
        {
            "src_ctx": get_template_dir_path("rules"),
            "dst": get_target_rules_dir(),
            "label": "rules/",
        },
        {
            "src_ctx": get_template_dir_path("docs"),
            "dst": get_target_docs_dir(),
            "label": "docs/",
        },
        {
            "src_ctx": get_template_dir_path("ontology"),
            "dst": get_target_ontology_dir(),
            "label": "ontology/",
        },
    ]

    for target in copy_targets:
        result = copy_with_confirm(
            target["src_ctx"], target["dst"], force, target["label"], errors
        )
        if not result:
            success = False

    return {"success": success, "errors": errors}
