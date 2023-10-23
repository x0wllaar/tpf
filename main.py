import click
from typing import Iterable

from controller import connect_controller

from service.service_serve import serve_command_impl
from service.service_stop import stop_command_impl
from service.service_list import list_command_impl

from client.client_key_generate import client_key_generate_command_impl
from client.client_key_load import client_key_load_command_impl
from client.client_key_list import client_key_list_command_impl


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
@click.argument("serviceid", nargs=-1)
@click.pass_context
def service_stop_cmd(ctx: click.Context, serviceid: str):
    ctx.ensure_object(dict)
    keyfile = ctx.obj["SERVICEKEYFILE"]
    cnt = ctx.obj["CONTROLLER"]
    stop_command_impl(cnt, keyfile, serviceid)


@service_cmd.command("list")
@click.pass_context
def service_list_cmd(ctx: click.Context):
    cnt = ctx.obj["CONTROLLER"]
    list_command_impl(cnt)


@main.group("client")
@click.pass_context
def client_cmd(ctx: click.Context):
    pass


@client_cmd.group("key")
@click.option("--keyfile", type=click.Path(), required=False)
@click.pass_context
def client_key_cmd(ctx: click.Context, keyfile: str):
    ctx.ensure_object(dict)
    ctx.obj["CLIENTKEYFILE"] = keyfile


@client_key_cmd.command("generate")
@click.option("--force/--no-force", default=False)
@click.option("--printprivate/--no-printprivate", default=False)
@click.pass_context
def client_key_generate_cmd(ctx: click.Context, force: bool, printprivate: bool):
    ctx.ensure_object(dict)
    keyfile = ctx.obj["CLIENTKEYFILE"]
    client_key_generate_command_impl(keyfile, force, printprivate)


@client_key_cmd.command("load")
@click.option("--privatekey")
@click.argument("service_ids", nargs=-1)
@click.pass_context
def client_key_load_cmd(ctx: click.Context, privatekey: str, service_ids: Iterable[str]):
    cnt = connect_controller(ctx.obj["CONTROLPORT"])
    keyfile = ctx.obj["CLIENTKEYFILE"]
    client_key_load_command_impl(cnt, keyfile, privatekey, service_ids)


@client_key_cmd.command("list")
@click.option("--printprivate/--no-printprivate", default=False)
@click.argument("service_ids", nargs=-1)
@click.pass_context
def client_key_list_cmd(ctx: click.Context, printprivate: bool, service_ids: Iterable[str]):
    cnt = connect_controller(ctx.obj["CONTROLPORT"])
    client_key_list_command_impl(cnt, service_ids, printprivate)


if __name__ == "__main__":
    main(obj={})
