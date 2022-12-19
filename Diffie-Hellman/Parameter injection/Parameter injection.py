# p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
# g = 0x02
# A = 0xb137607fb2f2bf9b95ed720cea932423d219839eb31633554cf065cc92b5e26d2ecc62db733b16d980c121864aa6036c21fb940958de2476e9b46c620930e2055463bda1a1a8a959cf29ef8e48752a930a9548377d2bf992dbab33dc7a09b689e9574ac8019b5f9a7b43598d20dd906c3540aeb044a82f9c31983b976fc51e37e55f045f0aa05a54d3de428918f665a1ff1d208d8cde6d3d3c99b806a9f025c9291cbb97b211897feb5e4726757652c25262439ae547fb316e008937e8186422
# B = 0xcf11994ba107c76c5b481ef2eca1e46c312b45ca076dce5335408dc02f59d721a5b028f47595b486944728ffe401ee5b30f4a185d879db718c3bf428dc6ab18133b6b0db4761073d7ea1d2b1174975930649e7713a2beb3c60273d0f3ebe4b7ebe0bbc2e3c9f507c0a61183003f3ca27a343f0e592343bd94dffbe12ba34b2b49035b081e899b5a7f9ff9b8f0b5d9846689500244a8a6e84c3a8089dfae07bd5053f9db04801a89419fdd6d6110c129758289107ea82a91dff9dcee857e23ca2
# iv = 'c2abb188cd91c8bffc1d5d116098a7c3'
# enc_flag = 'b034dddd5537927a4f176ad4de99dff299163e961740bd77fb40409060cc0854'


from Crypto.Util.Padding import unpad
from json import loads, dumps
from Crypto.Cipher import AES
from hashlib import sha1
from pwn import remote

def decrypt_flag(shared_secret, iv, ciphertext):
    key = sha1(str(shared_secret).encode()).digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    plaintext = AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext)
    return plaintext.decode()

# send random info to Bob and ignore answer
io = remote("socket.cryptohack.org", 13371)
io.readline()
io.sendline(dumps({"p":"0x123", "g":"0x123", "A":"0x123"}).encode())
io.readline()

# send B = 1, so then 
# shared secret = pow(B, a, p) = 1 for any a
io.sendline(dumps({"B":"0x01"}).encode())
io.readuntil(b"from Alice: ")
recv = loads(io.readline())
iv, ciphertext = recv["iv"], recv["encrypted_flag"]

shared_secret = 1
print(decrypt_flag(shared_secret, iv, ciphertext))