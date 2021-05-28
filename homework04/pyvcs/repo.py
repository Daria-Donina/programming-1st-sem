import os
import pathlib
import typing as tp

os.environ["GIT_DIR"] = "GIT_DIR"

def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = pathlib.Path(workdir).absolute()
    path = workdir / os.environ["GIT_DIR"]
    if path.exists():
        return path
    elif workdir == workdir.parent:
        raise Exception("Not a git repository")
    else:
        return repo_find(workdir.parent)


def create_dir(path: tp.Union[str, pathlib.Path], parents: bool = False):
    path.mkdir(parents=parents)


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if pathlib.Path(workdir).is_file():
        raise Exception(f"{workdir} is not a directory")

    workdir = pathlib.Path(workdir).absolute()
    git_path = workdir / os.environ['GIT_DIR']
    create_dir(git_path)
    create_dir(git_path / 'refs' / 'heads', True)
    create_dir(git_path / 'refs' / 'tags', True)
    create_dir(git_path / 'objects', True)

    with open(git_path / 'HEAD', 'w+') as head:
        head.write('ref: refs/heads/master\n')

    with open(git_path / 'config', 'a+') as config:
        line = '[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n'
        config.write(line)

    with open(git_path / 'description', 'a+') as description:
        description.write('Unnamed pyvcs repository.\n')

    return pathlib.Path(os.environ['GIT_DIR'])
