from .client_key_file import ClientKeyFile
from stem.control import Controller
from stem import ProtocolError
from typing import Iterable
import os


def client_key_load_command_impl(cnt: Controller, keyfile: str, private_key: str, services: Iterable[str]):
    pkey = None
    if keyfile is not None and os.path.isfile(keyfile):
        client_key = ClientKeyFile.from_file(keyfile)
        pkey = client_key.private_key
    if private_key is not None:
        pkey = private_key

    if pkey is None:
        raise ValueError("Private key not specified")

    for srv in services:
        print(f"{srv} ->", end=" ")
        try:
            cnt.add_hidden_service_auth(srv, pkey, write=False)
            print(f"Added key")
        except ProtocolError as pe:
            if str(pe).endswith("Client for onion existed and replaced"):
                print("Replaced key")
            else:
                raise pe