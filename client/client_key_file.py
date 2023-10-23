import json
from dataclasses import dataclass


@dataclass
class ClientKeyFile:
    private_key: str
    public_key: str

    def to_dict(self) -> dict:
        return {
            "private_key": self.private_key,
            "public_key": self.public_key
        }

    def to_file(self, path: str):
        with open(path, "wt", encoding="utf-8") as kf:
            json.dump(self.to_dict(), kf)

    @staticmethod
    def from_file(path):
        with open(path, "rt", encoding="utf-8") as kf:
            dct = json.load(kf)
        return ClientKeyFile(
            private_key=dct["private_key"],
            public_key=dct["public_key"]
        )
