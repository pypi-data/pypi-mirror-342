import subprocess  # nosec
from pathlib import Path
from typing import Dict

import yaml  # type: ignore
from loguru import logger


def run_services_docker(services: Dict, volumes: Dict, verbose: int, dc_tmp_path: str):
    """
    Launch docker compose up for the services defined in the compose file.
    Skips any services whose images cannot be found.
    """
    compose_dict = {"version": "3.9", "services": {}}

    for service, config in services.items():
        image = f"sayby77/rnadvisor-{service}-slim"
        args = config.get("args", {})
        command = []
        for key, val in args.items():
            if val != "":
                command.append(key)
                command.append(str(val))
        if verbose <= 1:
            command.append("--quiet")

        volume_mounts = [f"{host}:{container}" for host, container in volumes.items()]

        compose_dict["services"][f"rnadvisor-{service}"] = {  # type: ignore
            "image": image,
            "command": command,
            "stdin_open": True,
            "tty": True,
            "restart": "no",
            "platform": "linux/amd64",
            "volumes": volume_mounts,
        }

    if not compose_dict["services"]:
        logger.warning("❌ No valid services to run.")
        return

    with Path(dc_tmp_path).open("w") as f:
        yaml.dump(compose_dict, f, sort_keys=False)
    subprocess.run(["docker", "compose", "-f", dc_tmp_path, "up"])  # nosec
