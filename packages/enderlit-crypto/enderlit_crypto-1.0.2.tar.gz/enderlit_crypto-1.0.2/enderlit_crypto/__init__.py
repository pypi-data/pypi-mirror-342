import random
import string
import math

SIGNATURE = "_by_Enderlit_2025"
VALID_DIGITS = '0123456789'

def get_day_type(weekday: int):
    return 'type1' if weekday in [0, 2, 4, 6] else 'type2'

def build_cipher_maps(day_type):
    alpha_half = 'abcdefghijklmnop'
    second_half = 'qrstuvwxyz'

    if day_type == 'type1':
        alpha_map = {ch: chr(ord('z') - (ord(ch) - ord('a'))) for ch in alpha_half}
        num_map = {ch: str(i) for i, ch in enumerate(second_half)}
    else:
        shifted = [chr((ord('q') + i - ord('a')) % 26 + ord('a')) for i in range(16)]
        alpha_map = {ch: shifted[i] for i, ch in enumerate(alpha_half)}
        num_map = {ch: str(9 - i) for i, ch in enumerate(second_half)}

    reverse_alpha_map = {v: k for k, v in alpha_map.items()}
    reverse_num_map = {v: k for k, v in num_map.items()}

    return alpha_map, num_map, reverse_alpha_map, reverse_num_map

def insert_noise(text: str, rate: float = 0.25) -> str:
    chars = list(text)
    noise_count = math.ceil(len(chars) * rate)
    for _ in range(noise_count):
        noise = random.choice(string.ascii_letters + string.digits)
        pos = random.randint(0, len(chars))
        chars.insert(pos, noise)
    return ''.join(chars)

def enderlit_crypt(text, weekday):
    day_type = get_day_type(weekday)
    alpha_map, num_map, _, _ = build_cipher_maps(day_type)
    result = []

    for ch in text.lower():
        if ch == ' ':
            result.append(random.choice(VALID_DIGITS))
        elif ch in alpha_map:
            result.append(alpha_map[ch])
        elif ch in num_map:
            result.append(num_map[ch])
        elif ch.isalnum():
            result.append(ch)

    return insert_noise(''.join(result)) + SIGNATURE

def enderlit_decrypt(text, weekday):
    if text.endswith(SIGNATURE):
        text = text[:-len(SIGNATURE)]

    day_type = get_day_type(weekday)
    _, _, reverse_alpha_map, reverse_num_map = build_cipher_maps(day_type)

    result = []
    for ch in text:
        if ch in reverse_alpha_map:
            result.append(reverse_alpha_map[ch])
        elif ch in reverse_num_map:
            result.append(reverse_num_map[ch])
        elif ch in VALID_DIGITS and ch not in reverse_num_map:
            result.append(' ')

    return ''.join(result) + SIGNATURE
