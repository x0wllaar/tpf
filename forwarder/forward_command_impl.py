from .socket_spec import SocketSpec
import socket
import threading
import socks
import signal

_spl = threading.Lock()


def _sprint(s: str):
    _spl.acquire(blocking=True)
    try:
        print(s)
    finally:
        _spl.release()


def forward_socket(frs: socket.socket, tos: socket.socket):
    while True:
        try:
            data = frs.recv(4096)
            if not data:
                tos.close()
                return
            tos.sendall(data)
        except ConnectionResetError:
            tos.close()
            return
        except ConnectionAbortedError:
            tos.close()
            return
        except OSError as e:
            tos.close()
            if not str(e).endswith("something that is not a socket"):
                raise e
            return
        except Exception as e:
            tos.close()
            raise e

def connect_socks_socket(c_socket: socket.socket, to_spec: SocketSpec, proxy_spec: None|SocketSpec):
    ups_socket = socks.socksocket()
    if proxy_spec is not None:
        ups_socket.set_proxy(proxy_type=socks.SOCKS5, addr=proxy_spec.target, port=proxy_spec.port)

    try:
        ups_socket.connect((to_spec.target, to_spec.port))
    except Exception as e:
        c_socket.close()
        raise e

    _sprint("Upstream connected")

    th1 = threading.Thread(target=forward_socket, args=(c_socket, ups_socket))
    th2 = threading.Thread(target=forward_socket, args=(ups_socket, c_socket))
    th1.start()
    th2.start()

    _sprint("Started forwarding")

    th1.join()
    th2.join()

    _sprint("Stopped forwarding")

def forward_command_impl(fr: str, to: str, useproxy: bool, proxy_addr: str):
    fr_spec = SocketSpec.from_string(fr)
    to_spec = SocketSpec.from_string(to)

    proxy_spec = None
    if useproxy:
        proxy_spec = SocketSpec.from_string(proxy_addr)

    l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    l_socket.bind((fr_spec.target, fr_spec.port))
    l_socket.listen()

    if proxy_spec is None:
        _sprint(f"Forwarding {fr_spec.target}:{fr_spec.port} -> {to_spec.target}:{to_spec.port}")
    else:
        _sprint(f"Forwarding {fr_spec.target}:{fr_spec.port} -> {proxy_spec.target}:{proxy_spec.port} -> {to_spec.target}:{to_spec.port}")

    _sprint("Press Ctrl-C to quit")
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    while True:
        client_socket, address = l_socket.accept()
        _sprint(f"New connection from {address}")
        fth = threading.Thread(target=connect_socks_socket, args=(client_socket, to_spec, proxy_spec))
        fth.start()
