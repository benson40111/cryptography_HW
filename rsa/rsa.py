'''
egcd and modinv function are copy form
https://gist.github.com/jeremy5189/891660
'''

from fractions import gcd

class RSA():
    def __init__(self, message):
        self.message = message
        ascii_message = []
        ascii_message = [ord(x) for x in self.message]
        self.ascii_message = ascii_message
        self.d = 0
        self.n = 0
        self.encrypted_ascii = None

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def encrypt(self):
        p = 61
        q = 53
        self.n = p * q
        phi = (p - 1) * (q - 1)
        e = 0
        for i in range(2, phi+1):
            if gcd(i, phi) == 1:
                e = i
                break
        self.d = self.modinv(e, phi)
        public_key = []
        public_key.extend([self.n, e])
        self.encrypted_ascii = [int((pow(x, e)) % self.n) for x in self.ascii_message]
        encrypted_message = ''.join(chr(i) for i in self.encrypted_ascii).encode()
        return public_key, self.d, encrypted_message

    def decrypt(self):
        decrypted_message = [int((pow(x, self.d)) % self.n) for x in self.encrypted_ascii]
        decrypted_message = ''.join(chr(i) for i in decrypted_message)
        return decrypted_message
