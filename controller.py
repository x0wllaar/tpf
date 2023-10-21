from stem.control import Controller


def connect_controller(port: int) -> Controller:
    cnt = Controller.from_port(port=port)
    cnt.connect()
    cnt.authenticate()
    return cnt
