import subprocess
from pathlib import Path


def run_cmd(cmd: str,
            cwd: Path,
            print_output: bool = True,
            no_throw: bool = False) -> str:
    print(f"[run_cmd] Running: {cmd} from {cwd}")

    ret = subprocess.run(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         universal_newlines=True,
                         cwd=cwd)
    if no_throw is False and ret.returncode:
        print(f"[run_cmd] Error {ret.returncode} raised while running cmd: {cmd}")
        print("[run_cmd] Output was:")
        print(ret.stdout)
        raise ValueError()

    if ret.returncode:
        print(f"[run_cmd] Output:\n{ret.stdout}")

    return ret.stdout.strip()


def git_setup(repo_name: str, repo_ref: str, repo_url: str, workdir: Path):
    # Force clone in https over SSH
    GIT_CONFIG = ' -c  url."https://github.com/".insteadOf="git@github.com:" -c url."https://".insteadOf="git://"'

    if not Path.exists(workdir/Path(repo_name)):
        run_cmd(f"git {GIT_CONFIG} clone {repo_url} --recurse-submodules {repo_name}", cwd=workdir)
    else:
        run_cmd("git fetch", cwd=workdir/Path(repo_name))

    run_cmd(f"git checkout {repo_ref}", cwd=workdir/Path(repo_name))
    run_cmd("git submodule update --recursive", cwd=workdir/Path(repo_name))


def merge_json(json1: dict, json2: dict, key: str):
    merged_data = []

    for obj1 in json1:
        merged_obj = obj1.copy()
        for obj2 in json2:
            if obj1[key] == obj2[key]:
                merged_obj.update(obj2)
                break
        merged_data.append(merged_obj)

    return merged_data
