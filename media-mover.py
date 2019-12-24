import glob
import shutil
import os
from pathlib import Path
from tqdm import tqdm


def copy_files(source, destination, extension):
    Path.mkdir(destination, parents=True, exist_ok=True)

    for path in source.rglob('*.' + extension):
        if any(p.name.startswith(".") or p.name.startswith("$") for p in path.parents):
            continue

        parent_dir = Path(str(path.parent.absolute()).replace(':', ''))
        final_dir = Path.joinpath(destination, parent_dir)

        Path.mkdir(final_dir, parents=True, exist_ok=True)

        final_path = Path.joinpath(final_dir, Path(path.name))

        shutil.copy(path, final_path)


HOME_DIRECTORY = Path("/")
extensions = {
    "image": ["png", "jpg", "jpeg"],
    "video":  ["avi", "mpg", "mpeg", "mov", "m4v"],
    "music": ["mp3", "wav"]
}

if __name__ == "__main__":
    for media in tqdm(extensions.keys(), desc="Total progress"):
        for ext in tqdm(extensions[media], desc=media.capitalize() + " progress"):
            copy_files(HOME_DIRECTORY, Path(media), ext)
