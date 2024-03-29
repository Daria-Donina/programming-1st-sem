import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree

os.environ["GIT_DIR"] = ".git"

def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths, True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    index = read_index(gitdir)
    tree_sha = write_tree(gitdir, index)
    return commit_tree(gitdir, tree_sha, message, author=author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    if is_detached(gitdir) and get_ref(gitdir) == obj_name:
        return
    elif get_ref(gitdir).split("/")[2] == obj_name:
        return
    elif resolve_head(gitdir) == obj_name:
        return
    elif (gitdir / 'refs' / 'heads' / obj_name).exists():
        with open(gitdir / 'refs' / 'heads' / obj_name, 'r') as file:
            obj_name = file.read()

    index = read_index(gitdir)
    for entry in index:
        if pathlib.Path(entry.name).exists():
            if '/' in entry.name:
                shutil.rmtree(entry.name[:entry.name.find('/')])
            else:
                os.remove(entry.name)

    path_to_commit = gitdir / "objects" / obj_name[:2] / obj_name[2:]
    if path_to_commit:
        with open(path_to_commit, 'rb') as file:
            raw = file.read()
        data = commit_parse(raw)
        tree_sha = data[data.find(b'tree ') + 5:data.find(b'\n')].decode()

        for file in find_tree_files(tree_sha, gitdir):
            if '/' in file[0]:
                dir_name = file[0][:file[0].find('/')]
                os.mkdir(dir_name)
            with open(file[0], 'w') as new_file:
                header, content = read_object(file[1], gitdir)
                new_file.write(content.decode())

