import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0".encode()
    line = header + data
    sha = hashlib.sha1(line).hexdigest()
    if write:
        dir_name = sha[:2]
        file_name = sha[2:]

        path = repo_find() / 'objects' / dir_name
        if not path.exists():
            path.mkdir()

            with open(str(path / file_name), 'wb+') as file:
                file.write(zlib.compress(line))

    return sha


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")

    dir_path = pathlib.Path(gitdir, 'objects', obj_name[:2])
    if not dir_path.exists():
        raise Exception(f"Not a valid object name {obj_name}")

    files = [obj_name[:2] + x.name for x in pathlib.Path(dir_path).glob(f'{obj_name[2:]}*')]
    if len(files) == 0:
        raise Exception(f"Not a valid object name {obj_name}")

    return files


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    return pathlib.Path(gitdir, 'objects', obj_name[:2], obj_name[2:])


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = find_object(sha, gitdir)

    if not os.path.exists(path):
        return

    with open(str(path), "rb") as file:
        data = file.read()

    obj_data = zlib.decompress(data)

    header_end = obj_data.find(b"\x00")
    header = obj_data[:header_end]
    fmt = header[:header.find(b" ")]
    data = obj_data[header_end + 1:]
    return fmt.decode('ascii'), data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    results = []
    while len(data) != 0:
        mode_end = data.find(b' ')
        mode = int(data[:mode_end])
        data = data[mode_end + 1:]

        name_end = data.find(b'\x00')
        name = data[:name_end].decode()
        data = data[name_end + 1:]

        sha = bytes.hex(data[:20])
        data = data[20:]
        results.append((mode, name, sha))
    return results


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = pathlib.Path(os.environ['GIT_DIR'])
    fmt, data = read_object(obj_name, gitdir)
    if pretty:
        if fmt == 'blob':
            print(data.decode())
        elif fmt == 'tree':
            tree_content = read_tree(data)
            for obj in tree_content:
                print(str(obj[0]).zfill(6), read_object(obj[2], gitdir)[0], obj[2], end='\t')
                print(obj[1])
        elif fmt == 'commit':
            print(data.decode())
    else:
        print(data)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    fmt, data = read_object(tree_sha, gitdir)
    for file in read_tree(data):
        if read_object(file[2], gitdir)[0] == "tree":
            tree = find_tree_files(file[2], gitdir)
            for blob in tree:
                name = file[1] + "/" + blob[0]
            result.append((name, blob[1]))
        else:
            result.append((file[1], file[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    return zlib.decompress(raw)
