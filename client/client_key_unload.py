from stem.control import Controller
from stem import ProtocolError
from typing import Iterable

def client_key_unload_command_impl(cnt: Controller, service_ids: Iterable[str]):
    service_ids = list(service_ids)
    service_ids = [sid.removesuffix(".onion") for sid in service_ids]
    for sid in service_ids:
        print(f"{sid} ->", end=" ")
        try:
            cnt.remove_hidden_service_auth(sid)
            print("Key removed")
        except ProtocolError as pe:
            if str(pe).endswith(f"No credentials for \"{sid}\""):
                print("Key was not loaded")
            else:
                raise pe
