import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_content = b''
    for entry in index:
        if '/' in entry.name:
            tree_content += b"40000 "
            dir_name = entry.name[:entry.name.find('/')]
            tree_content += dir_name.encode() + b'\0'
            subdir_file = str(entry.mode).encode() + b" "
            subdir_file += entry.name[entry.name.find("/") + 1:].encode() + b"\0"
            subdir_file += entry.sha1
            file_hash = hash_object(subdir_file, fmt="tree", write=True)
            tree_content += bytes.fromhex(file_hash)
        else:
            record = f'{entry.mode} {entry.name}\0'.encode() + entry.sha1
            tree_content += record
    return hash_object(tree_content, 'tree', True)


def commit_tree(
        gitdir: pathlib.Path,
        tree: str,
        message: str,
        parent: tp.Optional[str] = None,
        author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    ...
