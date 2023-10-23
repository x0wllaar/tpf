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

If yes, then this simple tool may be for you.

## How?

To forward RDP with native Tor key-based authentication:

Generate your client keypair on your client machine:

    tpf client key --keyfile key.ckey generate
    Public key: PUBLIC_KEY_BASE32

Copy this public key to your server computer 
(hint: you can use [Onionshare](https://onionshare.org) 
for that).

Run Tor Browser on your client machine. 
Make sure it connects and is connected to the Tor network.

Start the onion service on your server computer,
with client authentication enabled:

    tpf service --keyfile service.skey serve --detached --clientkey PUBLIC_KEY_BASE32 3389
    Serving on ONION_ADDR
    ...

On your client computer, load your client key into Tor:

    tpf client key --keyfile key.ckey load ONION_ADDR

On your client computer, use [socat](https://sourceforge.net/projects/unix-utils/files/socat/1.7.3.2/)
to forward ports via Tor (this is not needed for simple HTTP sharing):

    socat -dd -ls tcp-listen:33389,fork socks4a:127.0.0.1:ONION_ADDR:3389,socksport=9150,socksuser=rdp1

Connect to 127.0.0.1:33389 with your RDP client of choice.

To stop the forwarding, on the server computer run:

    tpf service --keyfile service.skey stop

