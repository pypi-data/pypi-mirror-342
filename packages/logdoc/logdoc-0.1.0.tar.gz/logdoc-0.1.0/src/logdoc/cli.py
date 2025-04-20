import os
import shutil
import argparse
import json
from datetime import datetime
from logdoc.core.header_injector import inject_headers
from logdoc.logger import log_event



def link_module(target_project, mode="copy", target_path=None):
    source_path = os.path.dirname(__file__)
    default_target = os.path.join(target_project, "src", "logdoc")
    final_target = target_path if target_path else default_target

    log_event("link-module start", {"project": target_project, "mode": mode})

    if os.path.exists(final_target):
        backup = f"{final_target}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(final_target, backup)
        print(f"🔁 Existing logdoc moved to: {backup}")

    if mode == "copy":
        shutil.copytree(source_path, final_target)
        print(f"✅ logdoc source copied to project as {final_target}")
    elif mode == "symlink":
        os.symlink(source_path, final_target)
        print(f"✅ logdoc symlinked to project as {final_target}")
    else:
        raise ValueError("Unsupported mode: choose 'copy' or 'symlink'")

    log_event("link-module completed", {"target": final_target, "mode": mode})
    print("🎯 Project ready for deployment with logdoc")


def main():
    parser = argparse.ArgumentParser(description="Link logdoc module to another project.")
    parser.add_argument("target_project", help="Path to the project where logdoc should be linked")
    parser.add_argument("--mode", choices=["copy", "symlink"], default="copy", help="Linking mode")
    parser.add_argument("--target-path", help="Optional override for target path")
    parser.add_argument("--inject", action="store_true", help="Inject headers into the target project")

    args = parser.parse_args()
    link_module(args.target_project, args.mode, args.target_path)

    if args.inject:
        src_dir = os.path.join(args.target_project, "src")
        log_event("inject-headers", {"path": src_dir})
        inject_headers(src_dir)


if __name__ == "__main__":
    main()
