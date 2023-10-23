from .client_key_file import ClientKeyFile


def client_key_print_command_impl(keyfile: str, human: bool, print_private: bool, print_public: bool):
    client_key = ClientKeyFile.from_file(keyfile)
    skey = client_key.private_key
    pkey = client_key.public_key

    skey_format = "{}"
    pkey_format = "{}"
    if human:
        skey_format = "Private key: " + skey_format
        pkey_format = "Public key: " + pkey_format

    if print_public:
        print(pkey_format.format(pkey))

    if print_private:
        print(skey_format.format(skey))