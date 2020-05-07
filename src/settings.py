from pathlib import Path


HOME_DIRECTORY = Path("~").expanduser()
CATEGORIES = {
    "image": ["png", "jpg", "jpeg"],
    "video":  ["avi", "mpg", "mpeg", "mov", "m4v"],
    "music": ["mp3", "wav", "m4a"]
}
