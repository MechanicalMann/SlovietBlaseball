from sloviet.encoder import CheckerboardEncoder, RingEncoder


def main():
    cipher = CheckerboardEncoder('blaseboard.cfg')
    print(cipher.encode('Hello world'))