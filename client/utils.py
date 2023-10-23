import base64
import nacl.public

def key_str(key):
    # bytes to base 32
    key_bytes = bytes(key)
    key_b32 = base64.b32encode(key_bytes)
    # strip trailing ====
    assert key_b32[-4:] == b'===='
    key_b32 = key_b32[:-4]
    # change from b'ASDF' to ASDF
    s = key_b32.decode('utf-8')
    return s


def str_key(kstr: str):
    assert len(kstr) == 52
    key_b32 = kstr + "===="
    key_bytes = base64.b32decode(key_b32.encode('utf-8'))
    key = nacl.public.PrivateKey(private_key=key_bytes)
    return key

def key_str_64(key):
    key_bytes = bytes(key)
    key_b64 = base64.b64encode(key_bytes)
    s = key_b64.decode('utf-8')
    return s

def str_64_key(key_b64):
    key_bytes = base64.b64decode(key_b64.encode('utf-8'))
    key = nacl.public.PrivateKey(private_key=key_bytes)
    return key