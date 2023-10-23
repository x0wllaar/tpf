import os.path
import platform
import signal

from .fwd_spec import ForwardSpec
from .service_key_file import ServiceKeyFile
from stem.control import Controller
from typing import Iterable


def _read_client_key_file(clientkeyfile) -> list[str]:
    if clientkeyfile is None:
        return []
    with open(clientkeyfile, "rt", encoding="utf-8") as ckf:
        lines = ckf.readlines()
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if len(l) > 0]
    lines = [l for l in lines if not l.startswith("#")]
    return lines

def serve_command_impl(detached: bool, cnt: Controller, service_key_file: str, client_key_file: str, client_keys: Iterable[str], fwd_specs: Iterable[str]):
    fwd_specs = [ForwardSpec.from_str(s) for s in fwd_specs]
    client_keys = _read_client_key_file(client_key_file) + list(client_keys)
    client_keys = [k.lower() for k in client_keys]
    if len(client_keys) == 0:
        client_keys = None

    if service_key_file is not None and os.path.isfile(service_key_file):
        service_key = ServiceKeyFile.from_file(service_key_file)
    else:
        service_key = None

    ports = {f.remote_port: f"{f.local_ip}:{f.local_port}" for f in fwd_specs}
    if service_key is None:
        srv = cnt.create_ephemeral_hidden_service(ports, detached=detached, await_publication=True,
                                                  client_auth_v3=client_keys)
        if service_key_file is not None:
            sk = ServiceKeyFile(pkey=srv.private_key, pkey_type=srv.private_key_type, onion_id=srv.service_id)
            sk.to_file(service_key_file)
    if service_key is not None:
        srv = cnt.create_ephemeral_hidden_service(ports, detached=detached, await_publication=True,
                                                  key_type=service_key.pkey_type, key_content=service_key.pkey,
                                                  client_auth_v3=client_keys)
        assert srv.service_id == service_key.onion_id

    print(f"Serving on {srv.service_id}.onion:")
    for r, l in ports.items():
        print(f"{r} -> {l}")
    print("")

    if not detached:
        if platform.system() != "Windows":
            def cch(s, f):
                print("Ctrl+C pressed")
            oh = signal.getsignal(signal.SIGINT)
            signal.signal(signal.SIGINT, cch)
            print("Press Ctrl+C to stop")
            signal.pause()
            signal.signal(signal.SIGINT, oh)
        else:
            input("Press Enter to stop")
        print("Exiting...")
    else:
        print("Exiting, to stop serving, use the \"stop\" command")