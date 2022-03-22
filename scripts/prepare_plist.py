import argparse
import os.path
import plistlib
import sys


def read_plist(plist_dir):
    info_plist_path = os.path.join(plist_dir, "info.plist")

    with open(info_plist_path, "rb") as info_plist:
        return plistlib.loads(info_plist.read())


def clean_variables_in_plist(plist):
    for non_exportable_variable in plist["variablesdontexport"]:
        plist["variables"].update({non_exportable_variable: ""})

    plist["variables"].update({"alfred_keyword": "kp"})
    plist["variables"].update({"python_path": "/usr/bin/python3"})


def add_website_to_plist(plist):
    plist["webaddress"] = "https://github.com/lxbrvr/alfred-keepassxc-workflow"


def add_bundle_id_to_plist(plist, bundle_id):
    plist["bundleid"] = bundle_id


def add_version_to_plist(plist, version):
    plist["version"] = version


def add_description_to_plist(plist):
    plist["description"] = "Alfred workflow for fetching KeepassXC entries and coping their attributes."


def save_plist(plist, source):
    info_plist_path = os.path.join(source, "info.plist")

    with open(info_plist_path, "wb") as info_plist:
        plistlib.dump(plist, info_plist)


def ask_for_plist_backup():
    return input("Environment variables will be removed from info.plist. Continue? (y/N): ")


def has_to_continue(answer):
    return answer.lower() in ["y", "yes"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Path to source code", required=True)
    parser.add_argument("--version", help="Version", required=True)
    parser.add_argument("--bundle_id", help="Bundle id", required=True)

    return parser.parse_args()


def main():
    parsed_args = parse_args()
    answer = ask_for_plist_backup()

    if not has_to_continue(answer):
        sys.exit("Canceled by user")

    plist = read_plist(plist_dir=parsed_args.source)
    add_website_to_plist(plist)
    add_bundle_id_to_plist(plist=plist, bundle_id=parsed_args.bundle_id)
    add_version_to_plist(plist=plist, version=parsed_args.version)
    add_description_to_plist(plist)
    clean_variables_in_plist(plist=plist)
    save_plist(plist=plist, source=parsed_args.source)


if __name__ == "__main__":
    main()
