#!/usr/bin/env python
from pwn import *

# context(terminal=['tmux', 'splitw', '-h'])  # horizontal split window
# context(terminal=['tmux', 'new-window'])  # open new window

# libc = ELF('${libc}')
elf = ELF('${binary}')
context(os='linux', arch=elf.arch)
context(log_level='debug')  # output verbose log

RHOST = "${host}"
RPORT = ${port}
LHOST = "127.0.0.1"
LPORT = ${port}

def section_addr(name, elf=elf):
    return elf.get_section_by_name(name).header['sh_addr']

conn = None
opt = sys.argv.pop(1) if len(sys.argv) > 1 else '?'  # pop option
if opt in 'rl':
    conn = remote(*{'r': (RHOST, RPORT), 'l': (LHOST, LPORT)}[opt])
elif opt == 'd':
    gdbscript = """
    # set environment LD_PRELOAD=${libc}
    b *{0}
    c
    """.format(hex(elf.symbols['main'] if 'main' in elf.symbols.keys() else elf.entrypoint))
    conn = gdb.debug(['${binary}'], gdbscript=gdbscript)
else:
    conn = process(['${binary}'])
    # conn = process(['${binary}'], env={'LD_PRELOAD': '${libc}'})
    if opt == 'a': gdb.attach(conn)

# exploit
log.info('Pwning')

conn.interactive()
