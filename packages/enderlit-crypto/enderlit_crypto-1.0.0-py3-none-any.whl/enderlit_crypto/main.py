
import random
import string

def _insert_noise(text, rate=0.25):
    count = round(len(text) * rate)
    positions = sorted(random.sample(range(len(text) + count), count))
    result = []
    i = 0
    for pos in range(len(text) + count):
        if i < len(positions) and pos == positions[i]:
            result.append(random.choice(string.ascii_letters + string.digits))
            i += 1
        else:
            result.append(text[0])
            text = text[1:]
    return ''.join(result)

def _replace_spaces(text):
    return ''.join(random.choice(string.digits) if c == ' ' else c for c in text)

def enderlit_crypt(text, weekday):
    alpha1 = 'abcdefghijklmnop'
    if weekday in [0, 2, 4, 6]:  # пон, среда, пятн, вск
        subs = {c: chr(122 - i) for i, c in enumerate(alpha1)}
        nums = {chr(i): str(j) for i, j in zip(range(113, 123), range(10))}
    else:  # вт, чт, суб
        shift = 16
        subs = {c: chr(((ord(c) - 97 + shift) % 26) + 97) for c in alpha1}
        nums = {chr(i): str(j) for i, j in zip(range(113, 123), reversed(range(10)))}
    text = text.lower()
    text = _replace_spaces(text)
    result = ''
    for char in text:
        if char in subs:
            result += subs[char]
        elif char in nums:
            result += nums[char]
        elif char.isalnum():
            result += char
    result = _insert_noise(result)
    return result + '_by_Enderlit_2025'

def enderlit_decrypt(text, weekday):
    text = text.replace('_by_Enderlit_2025', '')
    alpha1 = 'abcdefghijklmnop'
    if weekday in [0, 2, 4, 6]:
        subs = {chr(122 - i): c for i, c in enumerate(alpha1)}
        nums = {str(j): chr(i) for i, j in zip(range(113, 123), range(10))}
    else:
        shift = 16
        subs = {chr(((ord(c) - 97 + shift) % 26) + 97): c for c in alpha1}
        nums = {str(j): chr(i) for i, j in zip(range(113, 123), reversed(range(10)))}
    valid_chars = set(subs.keys()) | set(nums.keys())
    filtered = ''.join(c for c in text if c in valid_chars)
    result = ''
    for c in filtered:
        if c in subs:
            result += subs[c]
        elif c in nums:
            result += ' '
    return result + '_by_Enderlit_2025'
