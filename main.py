import click
from typing import Iterable


@click.group()
@click.pass_context
def main(ctx: click.Context):
    ctx.ensure_object(dict)


@main.group("service")
@click.option("--keyfile", type=click.Path(), required=True)
@click.pass_context
def service_cmd(ctx: click.Context, keyfile: str):
    ctx.ensure_object(dict)
    ctx.obj["KEYFILE"] = str(keyfile)


@service_cmd.command("generate")
@click.pass_context
def service_keygen_cmd(ctx: click.Context):
    ctx.ensure_object(dict)
    keyfile = ctx.obj["KEYFILE"]


@service_cmd.command("serve")
@click.option('--detached/--no-detached', default=False)
@click.option('--clientkeys', type=click.Path(exists=True))
@click.argument('fwd_spec', nargs=-1, required=True)
@click.pass_context
def service_serve_cmd(ctx: click.Context, detached: bool, clientkeys: str, fwd_spec: Iterable[str]):
    ctx.ensure_object(dict)
    keyfile = ctx.obj["KEYFILE"]


@service_cmd.command("stop")
@click.pass_context
def service_stop_cmd(ctx: click.Context, detached: bool, fwd_spec: Iterable[str]):
    ctx.ensure_object(dict)
    keyfile = ctx.obj["KEYFILE"]


if __name__ == "__main__":
    main(obj={})
