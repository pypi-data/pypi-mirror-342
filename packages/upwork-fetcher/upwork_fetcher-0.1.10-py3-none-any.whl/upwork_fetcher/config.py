import json
from pathlib import Path
from typing import Any


CONFIG_DIR = Path.home() / ".upwork_fetcher"
CONFIG_FILE = CONFIG_DIR / "config.json"
# DEFAULT_UPWORK_FETCHER_DIR = Path.home() / ".upwork_fetcher"


def load_config(config_path: Path = CONFIG_FILE):
    if not config_path.exists():
        # os.makedirs(config_path.parent, exist_ok=True)
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        data = {}
        with open(config_path, "w") as file:
            json.dump(data, file, indent=4)

        # return {"upwork_dir": str(CONFIG_DIR)}
    # print(f"loading config {config_path}")
    with open(config_path, "r") as file:
        return json.load(file)


def save_config(data: dict[str, Any]):

    with open(CONFIG_FILE, "r") as file:
        config = json.loads(file.read())

    # print(f"{data = }")

    config.update(data)

    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)
