from sloviet.encoder import RingEncoder


def main():
    cipher = RingEncoder()
    print(cipher.encode('Hello, world!'))