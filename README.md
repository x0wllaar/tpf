# tpf

A 0-bullshit tool to forward ports using Tor

## Why?

Are you:
* Behind restrictive NAT?
* Behind an overly restrictive firewall?
* Fed up with bullshit from services like ngrok?

Do you want to forward ports:
* From behind all imaginable NATs and firewalls?
* Without exposing your machine's IP?
* With secure end-to-end encryption?
* With secure authentication?
* For any TCP-based protocol?

Were you looking for a simple tool that can do all that?

Now, [there is such a tool](https://en.wikipedia.org/wiki/There_is_such_a_party!).

## How do I use `tpf`?

To forward RDP with native Tor key-based authentication:

Generate your client keypair on your client machine:

    tpf client key --keyfile key.ckey generate
    Public key: PUBLIC_KEY_BASE32

Copy this public key to your server machine 
(hint: you can use [Onionshare](https://onionshare.org) 
for that).

Run Tor Browser on your client. 
Make sure it connects and is connected to the Tor network.

Start the onion service on your server,
with client authentication enabled:

    tpf service --keyfile service.skey serve --detached --clientkey PUBLIC_KEY_BASE32 3389
    Serving on ONION_ADDR
    ...

On your client computer, make sure Tor Browser is running
and connected, and load your client key into Tor:

    tpf client key --keyfile key.ckey load ONION_ADDR

On your client computer, use the `forward` command of `tpf`
to forward ports via Tor (this is not needed for simple HTTP sharing):

    tpf forward --fromaddr 33389 --toaddr ONION_ADDR:3389
    Forwarding localhost:33391 -> 127.0.0.1:9150 -> ONION_ADDR:3389

Connect to localhost:33389 with your RDP client of choice.

To stop the forwarding, on the server run:

    tpf service --keyfile service.skey stop
