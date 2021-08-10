from sloviet.cipher import OneTimePadCipher
from sloviet.encoder import CheckerboardEncoder, RingEncoder


def main():
    encoder = CheckerboardEncoder('blaseboard.cfg')
    cipher = OneTimePadCipher('otp.txt')
    plaincode = encoder.encode('Hello world')
    print(cipher.encrypt(plaincode))