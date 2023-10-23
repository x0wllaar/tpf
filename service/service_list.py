from stem.control import Controller


def list_command_impl(cnt: Controller):
    hsl = cnt.list_ephemeral_hidden_services(our_services=True, detached=True)
    hsl = list(hsl)
    for hs in hsl:
        print(hs)