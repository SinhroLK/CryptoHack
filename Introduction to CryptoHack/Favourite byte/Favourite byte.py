import pwn
data = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'
unhexedData = bytearray.fromhex(data)
print(unhexedData.decode())
for i in range(256):
    if(pwn.xor(unhexedData,i.to_bytes()).decode().startswith('crypto')):
        print(pwn.xor(unhexedData,i.to_bytes()).decode())