import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    path = gitdir / ref
    if not path.exists():
        with open(str(path), 'w+') as file:
            file.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    ...


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == 'HEAD':
        return resolve_head(gitdir)

    with open((gitdir / refname).as_posix(), 'r') as file:
        content = file.read()
    return content


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    if not is_detached(gitdir):
        ref_name = get_ref(gitdir)
        if (gitdir / ref_name).exists():
            return ref_resolve(gitdir, ref_name)


def is_detached(gitdir: pathlib.Path) -> bool:
    head = gitdir / "HEAD"

    with open(str(head), "r") as f:
        content = f.read().strip()

    return not content.startswith('ref: ')


def get_ref(gitdir: pathlib.Path) -> str:
    head = str(gitdir / "HEAD")

    with open(head, 'r') as file:
        content = file.read().strip()
        ref_name = content[content.find(' ') + 1:]
    return ref_name
