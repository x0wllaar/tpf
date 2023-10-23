from stem.control import Controller, HiddenServiceCredential
from typing import Iterable, Dict
from .utils import key_str, str_64_key


def client_key_list_command_impl(cnt: Controller, service_ids: Iterable[str], print_private: bool):
    all_hs_auth: Dict[str, HiddenServiceCredential] = cnt.list_hidden_service_auth()
    sids = set(service_ids)
    if len(sids) > 0:
        all_hs_auth = {sid: cred for sid, cred in all_hs_auth.items() if sid in sids}
    else:
        all_hs_auth = {sid: cred for sid, cred in all_hs_auth.items()}

    if not print_private:
        print("serviceid", "publickey")
    else:
        print("serviceid", "publickey", "privatekey")

    for sid, cred in all_hs_auth.items():
        csk = cred.private_key
        cpk = key_str(str_64_key(csk).public_key)
        print(f"{sid} {cpk}", end="")
        if print_private:
            print(f" {csk}")
        else:
            print("")


