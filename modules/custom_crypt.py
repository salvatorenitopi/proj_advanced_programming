from Crypto.Cipher import AES

def pad16(string):
    BLOCK_SIZE = 16
    PADDING = '#'
    out = string + (BLOCK_SIZE - len(string) % BLOCK_SIZE) * PADDING
    return out
    
def unpad16 (string):
    BLOCK_SIZE = 16
    PADDING = '#'
    out = string.strip(PADDING)
    return out

class Crypt(object):
    def __init__(self, password):
        password = pad16(password)
        self.cipher = AES.new(password, AES.MODE_ECB)

    def encrypt(self, s):
        s = pad16(s)
        return self.cipher.encrypt(s)

    def decrypt(self, s):
        t = self.cipher.decrypt(s)
        return unpad16(t)


def encrypt(s, p):
    c = Crypt(p)
    return c.encrypt(s)


def decrypt(s, p):
    c = Crypt(p)
    return c.decrypt(s)

