import argparse
import os.path
import plistlib


ALFRED_DIRECTORY = os.path.expanduser("~/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows/")


def read_plist(plist_dir):
    return plistlib.readPlist(os.path.join(plist_dir, "info.plist"))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Path to source code", required=True)
    return parser.parse_args()


def main():
    parsed_args = parse_args()
    plist = read_plist(parsed_args.source)
    bundle_id = plist["bundleid"]
    install_path = os.path.join(ALFRED_DIRECTORY, bundle_id)

    if os.path.exists(install_path):
        print("The path already exists:\n{0}".format(install_path))
        return

    os.symlink(parsed_args.source, install_path)


if __name__ == "__main__":
    main()
