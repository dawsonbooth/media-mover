import os
import shutil
from pathlib import Path
import logging


def all_files(directory, ignore_paths=[]):
    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        for d in range(len(dirnames) - 1, -1, -1):
            if dirnames[d].startswith(".") or dirnames[d].startswith("$") or Path(dirpath).joinpath(dirnames[d]).absolute() in ignore_paths:
                del dirnames[d]
        yield dirpath, dirnames, filenames


def count_files(directory):
    total = 0
    for dirpath, dirnames, filenames in all_files(directory):
        total += len(filenames)
    return total


def copy_files(source_dir, dest_dir, categories):
    source_dir = Path(source_dir).expanduser().resolve()
    dest_dir = Path(dest_dir).expanduser().resolve()

    progress = 0
    for dirpath, dirnames, filenames in all_files(source_dir, ignore_paths=[dest_dir]):
        for n, name in enumerate(filenames):
            for media in categories.keys():
                if any(name.endswith(ext) for ext in categories[media]):
                    source = Path(dirpath).joinpath(name)

                    dest_ext_dir = dest_dir.joinpath(media)
                    Path.mkdir(dest_ext_dir, parents=True, exist_ok=True)

                    dest_parent = Path(
                        f"{dest_ext_dir}/{str(source.parent.absolute()).replace(':', '')}")

                    Path.mkdir(dest_parent, parents=True, exist_ok=True)

                    dest = dest_parent.joinpath(source.name)

                    shutil.copy(source, dest)
                    logging.info(f"Copied '{name}' to '{media}'")

            progress += n
            yield progress
