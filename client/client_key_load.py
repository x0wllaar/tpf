from .client_key_file import ClientKeyFile
from stem.control import  Controller
from typing import Iterable
import os


def client_key_load_command_impl(cnt: Controller, keyfile: str, private_keys: Iterable[str], services: Iterable[str]):
    pkeys = list(private_keys)
    if keyfile is not None and os.path.isfile(keyfile):
        client_key = ClientKeyFile.from_file(keyfile)
        pkeys.append(client_key.private_key)

    for srv in services:
        print(f"{srv} ->", end=" ")
        for pk in pkeys:
            cnt.add_hidden_service_auth(srv, pk, write=False)
        print(f"Added {len(pkeys)} key{'s' if len(pkeys) > 1 else ''}")