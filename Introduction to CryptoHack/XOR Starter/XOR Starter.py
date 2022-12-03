import pwn
string = 'label'
number = 13
print(pwn.xor(string, number).decode())
