import click
from typing import Iterable

from controller import connect_controller
from service.service_serve import serve_command_impl

@click.group()
@click.option("--controlport", type=int, default=9151)
@click.pass_context
def main(ctx: click.Context, controlport: int):
    ctx.ensure_object(dict)
    ctx.obj["CONTROLPORT"] = controlport


@main.group("service")
@click.option("--keyfile", type=click.Path(), required=False)
@click.pass_context
def service_cmd(ctx: click.Context, keyfile: str):
    ctx.ensure_object(dict)
    ctx.obj["SERVICEKEYFILE"] = keyfile
    ctx.obj["CONTROLLER"] = connect_controller(ctx.obj["CONTROLPORT"])


@service_cmd.command("serve")
@click.option('--detached/--no-detached', default=False)
@click.option('--clientkeyfile', type=click.Path(exists=True))
@click.option("--clientkey", multiple=True)
@click.argument('fwd_spec', nargs=-1, required=True)
@click.pass_context
def service_serve_cmd(ctx: click.Context, detached: bool, clientkeyfile: str,
                      clientkey: Iterable[str], fwd_spec: Iterable[str]):
    ctx.ensure_object(dict)
    cnt = ctx.obj["CONTROLLER"]
    keyfile = ctx.obj["SERVICEKEYFILE"]
    serve_command_impl(detached, cnt=cnt, service_key_file=keyfile, client_key_file=clientkeyfile,
                       client_keys=clientkey, fwd_specs=fwd_spec)


@service_cmd.command("stop")
@click.option("--serviceid")
@click.pass_context
def service_stop_cmd(ctx: click.Context, serviceid: str):
    ctx.ensure_object(dict)
    keyfile = ctx.obj["KEYFILE"]


if __name__ == "__main__":
    main(obj={})
