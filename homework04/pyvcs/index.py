import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object

import code


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        _format = f">10I20sH{len(self.name) + 3}s"
        args = self[:-1]
        encoded_name = self.name.encode('ascii')
        return struct.pack(_format, *args, encoded_name)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        unpacked = struct.unpack(f">10I20sH{len(data) - 62}s", data)
        return GitIndexEntry(*unpacked[:-1], unpacked[-1].decode('ascii').rstrip('\x00'))


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    entries = []
    index_path = pathlib.Path(gitdir / 'index')
    if not index_path.exists():
        return entries
    with open(index_path, 'rb') as index:
        index_data = index.read()

    _, _, count = struct.unpack(">4s2I", index_data[:12])
    index_data = index_data[12:]
    for i in range(count):
        end = index_data[62:].find(b"\x00\x00\x00") + 3
        line_to_unpack = index_data[:62 + end]
        entries.append(GitIndexEntry.unpack(line_to_unpack))
        index_data = index_data[62 + end:]
    return entries


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    index_path = pathlib.Path(gitdir / 'index')

    data = b"DIRC" + struct.pack(">2I", 2, len(entries))
    for entry in entries:
        data += entry.pack()
    data += struct.pack(">20s", hashlib.sha1(data).digest())

    with open(index_path, 'wb+') as index:
        index.write(data)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    entries = read_index(gitdir)
    if not details:
        print(*[e.name for e in entries], sep='\n')
    else:
        for e in entries:
            print(int(oct(e.mode)[2:]), str(e.sha1.hex()), '0', end='\t')
            print(e.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = []
    for path in paths:
        with open(str(path), 'rb') as file:
            data = file.read()
        statinfo = os.stat(str(path))
        entry = GitIndexEntry(int(statinfo.st_ctime), 0, int(statinfo.st_mtime), 0, statinfo.st_dev,
                              statinfo.st_ino, int(oct(statinfo.st_mode)[2:]), statinfo.st_uid, statinfo.st_gid,
                              statinfo.st_size, bytes.fromhex(hash_object(data, 'blob', write)), 0,
                              str(path.as_posix()))
        entries.append(entry)
    write_index(gitdir, sorted(entries, key=lambda e: e.name))
