from dataclasses import dataclass
from typing import List
def _parse_forward_spec(spec: str) -> List[str]:
    components = []
    br_depth = 0
    cur_component = ""

    for c in list(spec):
        if c == "[":
            br_depth += 1
        if c == "]":
            br_depth -= 1
        if c == ":" and br_depth == 0:
            components.append(cur_component)
            cur_component = ""
            continue
        cur_component += c
    if len(cur_component) > 0:
        components.append(cur_component)

    return components

@dataclass
class ForwardSpec:
    remote_port: int
    local_port: int
    local_ip: str

    @staticmethod
    def from_str(spec: str):
        components = _parse_forward_spec(spec)
        if len(components) < 0:
            raise ValueError(f"Bad forwarding spec {spec}, too few components")
        if len(components) > 3:
            raise ValueError(f"Bad forwarding spec {spec}, too many components (did you surround IPv6 address with [])")
        if len(components) == 1:
            rport = int(components[0])
            return ForwardSpec(remote_port=rport, local_port=rport, local_ip="localhost")
        if len(components) == 2:
            rport = int(components[0])
            lport = int(components[1])
            return ForwardSpec(remote_port=rport, local_port=lport, local_ip="localhost")
        if len(components) == 3:
            rport = int(components[0])
            lip = str(components[1])
            lport = int(components[2])
            return ForwardSpec(remote_port=rport, local_port=lport, local_ip=lip)

        assert False
