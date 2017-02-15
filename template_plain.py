import socket
import struct

RHOST = "${host}"
RPORT = ${port}
LHOST = "127.0.0.1"
LPORT = ${port}

def remote(host, port):
    return socket.create_connection((host, port))

def process(*args):
    import subprocess
    p = subprocess.Popen(args, 
            stdin=subprocess.PIPE.stdin,
            stdout=subprocess.PIPE.stdout,
            stderr=subprocess.PIPE.stderr)
    return p.communicate()[0]

def interact(s):
    import telnetlib
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

p32 = lambda x: struct.pack('<I', x)
u32 = lambda x: struct.unpack('<I', x)[0]

conn = None

if len(sys.argv) > 1:
    if sys.argv[1] == 'r':
        conn = remote(RHOST, RPORT)
    elif sys.argv[1] == 'l':
        conn = remote(LHOST, LPORT)
else:
    conn = process(['${binary}'])
    # conn = process(['${binary}'], env={'LD_PRELOAD': '${libc}'})

# preparing for exploitation

# interact()
