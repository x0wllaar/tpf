from dataclasses import dataclass

@dataclass
class SocketSpec:
    port: int
    target: str

    @staticmethod
    def from_string(spec: str):
        comps = []
        b_depth = 0
        c_comp = ""
        for c in list(spec):
            if c == "[":
                b_depth += 1
            if c == "]":
                b_depth -= 1
            if c == ":" and b_depth == 0:
                comps.append(c_comp)
                c_comp = ""
                continue
            c_comp += c
        if len(c_comp) > 0:
            comps.append(c_comp)

        if len(comps) < 1:
            raise ValueError(f"Incorrect socket spec {spec}, too few components")

        if len(comps) > 2:
            raise ValueError(f"Incorrect socket spec {spec}, too many components")

        if len(comps) == 1:
            port = int(comps[0])
            return SocketSpec(
                target="localhost",
                port=port
            )

        if len(comps) == 2:
            target = str(comps[0])
            port = int(comps[1])
            return SocketSpec(
                target=target,
                port=port
            )

        assert False
