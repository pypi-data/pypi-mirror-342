#  Enderlit Crypto

Шифратор-дешифратор от Enderlit  

---

##  Установка и использование

```bash
pip install enderlit_crypto
```

```python
from enderlit_crypto import enderlit_crypt, enderlit_decrypt

# Шифруем
cipher = enderlit_crypt("Hello, world!", 1)

# Дешифруем
plain = enderlit_decrypt(cipher, 1)

print("Зашифровано:", cipher)
print("Расшифровано:", plain)
```

---

## Аргументы

- `text` – текст для шифровки/дешифровки
- `weekday` – день недели от `0` до `6`

---

## Как работает шифр

- Разные схемы подстановки
- Буквы `q-z` → цифры
- Пробелы → цифры
- Случайный мусор (25%)
- Подпись: `_by_Enderlit_2025`

---

## Лицензия

MIT License (см. LICENSE)
