from .client_key_file import ClientKeyFile
from .utils import key_str, key_str_64
import nacl.public
import os

#https://github.com/pastly/python-snippits/blob/master/src/tor/x25519-gen.py
def _generate_raw_keys() -> ClientKeyFile:
    priv_key = nacl.public.PrivateKey.generate()
    pub_key = priv_key.public_key
    return ClientKeyFile(
        private_key=key_str_64(priv_key),
        public_key=key_str(pub_key)
    )


def client_key_generate_command_impl(keyfile: str, force: bool, print_private: bool):
    if keyfile is not None and (os.path.isfile(keyfile) and not force):
        print(f"File {keyfile} exists, skipping")
        return
    keys = _generate_raw_keys()
    if keyfile is not None:
        keys.to_file(keyfile)
    print(f"Public key: {keys.public_key}")
    if print_private:
        print(f"Private key: {keys.private_key}")
