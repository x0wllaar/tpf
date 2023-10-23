from stem.control import Controller
from typing import Iterable
from .service_key_file import ServiceKeyFile
import os


def stop_command_impl(cnt: Controller, service_key_file: str, service_ids: Iterable[str]):
    all_ids = list(service_ids)
    if service_key_file is not None and os.path.isfile(service_key_file):
        service_key = ServiceKeyFile.from_file(service_key_file)
        all_ids.append(service_key.onion_id)
    all_ids = [sid.removesuffix(".onion") for sid in all_ids]

    for sid in all_ids:
        print(f"Stopping {sid}.onion ->", end=" ")
        r_res = cnt.remove_ephemeral_hidden_service(sid)
        if r_res:
            print("Stopped")
        else:
            print("Was not running")
