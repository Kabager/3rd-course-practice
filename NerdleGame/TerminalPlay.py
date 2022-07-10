import random
import re
from Calculus import modinv


class OperationDefiner:
    def __init__(self, operation=None):
        operations = dict()
        operations["+"] = lambda a, b, n: (a + b) % n
        operations["-"] = lambda a, b, n: (a - b) % n
        operations["*"] = lambda a, b, n: (a * b) % n
        operations["/"] = lambda a, b, n: (a * modinv(b, n)) % n

        if operation:
            self.str = operation
            self.operation = operations[self.str]
            return

        self.str = random.choice(list(operations.keys()))
        self.operation = operations[self.str]

    def __call__(self, a, b, n):
        return self.operation(a, b, n)

    def __str__(self):
        return self.str


class GameEngine:
    def __init__(self):
        # Размер игрового поля
        self.guess_word = self.generate_expresssion(8)
        self.game_field = ["?" for _ in range(len(self.guess_word))]
        self.alphabet = [str(i) for i in range(10)]
        self.alphabet.extend(['+', '-', '/', '*', '='])
        # Количество попыток
        self.total_attempts = 8

    def generate_expresssion(self, length):
        modulus = [101, 103, 107, 109, 113,
                   127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                   233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
                   353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                   467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
                   607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
                   739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
                   877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991]
        self.n = random.choice(modulus)

        while True:
            operation = OperationDefiner()
            a = random.randrange(1, self.n)
            b = random.randrange(1, self.n)
            c = operation(a, b, self.n)
            s = [char for char in str(a) + str(operation) + str(b) + '=' + str(c)]
            if len(s) == length:
                return s

    def draw(self):
        print(''.join(self.game_field) + f" mod {self.n}", ' '.join(self.alphabet),
             f'Осталось {self.total_attempts} попыток!', sep='\n')

    def update(self):
        player_answer = input()
        if len(player_answer) != len(self.guess_word):
            print("Ваше выражение неверной длины")
            return

        try:
            a, o, b, __, c = re.split(r'(\+|\-|\*|\/|\=)', player_answer)
            a, b, c = map(int, (a, b, c))
            o = OperationDefiner(o)

            if o(a, b, self.n) != c:
                raise ValueError

        except:
            print("Неверное выражение")
            return

        for i in range(len(self.guess_word)):
            if player_answer[i] == self.guess_word[i]:
                self.game_field[i] = player_answer[i]

            elif player_answer[i] not in self.guess_word and player_answer[i] in self.alphabet:
                self.alphabet.remove(player_answer[i])

        self.total_attempts -= 1

    def check_win(self):
        return "?" not in self.game_field

    def game_start(self):
        while self.total_attempts != 0:
            self.draw()
            self.update()
            if self.check_win():
                print("Win!")
                return

        print("Lose!")
        print(f"Исходное выражение было: {''.join(self.guess_word)}")


engine = GameEngine()
engine.game_start()
print('\n', "Для выхода введите любой символ...", "Для повтора введите R", sep='\n')

while input() == "R":
    engine = GameEngine()
    engine.game_start()
    print('\n', "Для выхода введите любой символ...", "для повтора введите R", sep='\n')
