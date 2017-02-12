from pwn import *

context(os='linux', arch='{arch}')
context.log_level = 'debug' # output verbose log

RHOST = "{host}"
RPORT = {port}
LHOST = "127.0.0.1"
LPORT = {port}

# libc = ELF('{libc}')
elf = ELF('{binary}')

def section_addr(name, elf=elf):
    return elf.get_section_by_name(name).header['sh_addr']

conn = None
if len(sys.argv) > 1:
    if sys.argv[1] == 'r':
        conn = remote(RHOST, RPORT)
    elif sys.argv[1] == 'l':
        conn = remote(LHOST, LPORT)
    elif sys.argv[1] == 'd':
        execute = """
        # set environment LD_PRELOAD={libc}
        b *{{0}}
        c
        """.format(hex(elf.symbols['main'] if 'main' in elf.symbols.keys() else elf.entrypoint))
        conn = gdb.debug(['{binary}'], execute=execute)
else:
    conn = process(['{binary}'])
    # conn = process(['{binary}'], env={{'LD_PRELOAD': '{libc}'}})

# preparing for exploitation

log.info('Pwning')

conn.interactive()
