import json
from dataclasses import dataclass


@dataclass
class ServiceKeyFile:
    pkey: str
    pkey_type: str
    onion_id: str

    def to_dict(self) -> dict:
        return {
            "pkey": self.pkey,
            "pkey_type": self.pkey_type,
            "onion_id": self.onion_id
        }

    def to_file(self, path):
        with open(path, "wt", encoding="utf-8") as kf:
            json.dump(self.to_dict(), kf)

    @staticmethod
    def from_file(path):
        with open(path, "rt", encoding="utf-8") as kf:
            dct = json.load(kf)

        return ServiceKeyFile(
            pkey=dct["pkey"],
            pkey_type=dct["pkey_type"],
            onion_id=dct["onion_id"]
        )
