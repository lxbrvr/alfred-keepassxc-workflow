import argparse
import os.path
import shutil
from contextlib import contextmanager
from tempfile import mkdtemp


@contextmanager
def temporary_directory():
    directory_path = mkdtemp()

    try:
        yield directory_path
    finally:
        shutil.rmtree(directory_path)


def make_alfred_file_from_source(source, version):
    archive_path = shutil.make_archive(
        base_name="keepassxc",
        format="zip",
        root_dir=source,
    )
    new_archive_name = "{name}-{version}.alfredworkflow".format(name=archive_path[:-4], version=version)
    os.rename(archive_path, new_archive_name)


def copy_source(source, destination):
    allowed_files = [
        "__init__.py",
        "alfred.py",
        "cli.py",
        "conf.py",
        "handlers.py",
        "helpers.py",
        "icon.png",
        "info.plist",
        "services.py",
        "settings.js",
    ]

    for allowed_file in allowed_files:
        shutil.copy2(src=os.path.join(source, allowed_file), dst=destination)


def print_success_message():
    print("Workflow has built successfully.")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Path to source code", required=True)
    parser.add_argument("--version", help="Workflow version", required=True)

    return parser.parse_args()


def main():
    parsed_args = parse_args()

    with temporary_directory() as tmp_directory_path:
        copy_source(source=parsed_args.source, destination=tmp_directory_path)
        make_alfred_file_from_source(source=tmp_directory_path, version=parsed_args.version)
        print_success_message()


if __name__ == "__main__":
    main()
