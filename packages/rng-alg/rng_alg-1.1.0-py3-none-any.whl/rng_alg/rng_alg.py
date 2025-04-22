import math
import random
class RNG:
    @staticmethod
    def pi_alg():
        pi_str = str(math.pi).replace('.', '')
        index1 = random.randint(0, len(pi_str) - 3)
        secti1 = int(pi_str[index1:index1 + 3])
        index2 = random.randint(0, len(pi_str) - 3)
        while index2 == index1:
            index2 = random.randint(0, len(pi_str) - 3)
        secti2 = int(pi_str[index2:index2 + 3])
        add = secti1 + secti2
        index3 = random.randint(0, len(pi_str) - 1)
        div = int(pi_str[index3])
        if div == 0:
            div = 1
        result = add / div
        print(result)
    @staticmethod
    def advanced_rng(frm, to):
        frm, to = int(frm), int(to)
        main = sum(random.randint(frm // 4, to // 4) for _ in range(4))
        print(main)
    @staticmethod
    def hex(min_val=None, max_val=None):
        if min_val is None and max_val is None:
            min_val, max_val = 1, 0xFFFFF
        elif min_val is None:
            min_val = 1
        elif max_val is None:
            max_val = 0xFFFFF
        min_val, max_val = int(min_val), int(max_val)
        random_hex = hex(random.randint(min_val, max_val))[2:].upper()
        print(random_hex)
    @staticmethod
    def special_char_gen(count=1):
        special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~€£¥§¶∞✓✔★♥♦♣♠"
        random_chars = ''.join(random.choice(special_chars) for _ in range(count))
        print(random_chars)