import os
from dynaconf import Dynaconf

current_dir = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(
    settings_files=[
        os.path.join(current_dir, "settings.toml"),
        os.path.join(current_dir, ".secrets.toml"),
    ],
)


log_config = settings.get("logging", {})
auth_config = settings.get("auth", {})
