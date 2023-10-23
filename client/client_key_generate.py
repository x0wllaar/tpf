from .client_key_file import ClientKeyFile
import base64
import nacl.public
import os


#https://github.com/pastly/python-snippits/blob/master/src/tor/x25519-gen.py
def _key_str(key):
    # bytes to base 32
    key_bytes = bytes(key)
    key_b32 = base64.b32encode(key_bytes)
    # strip trailing ====
    assert key_b32[-4:] == b'===='
    key_b32 = key_b32[:-4]
    # change from b'ASDF' to ASDF
    s = key_b32.decode('utf-8')
    return s

def _generate_raw_keys() -> ClientKeyFile:
    priv_key = nacl.public.PrivateKey.generate()
    pub_key = priv_key.public_key
    return ClientKeyFile(
        private_key=_key_str(priv_key),
        public_key=_key_str(pub_key)
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
