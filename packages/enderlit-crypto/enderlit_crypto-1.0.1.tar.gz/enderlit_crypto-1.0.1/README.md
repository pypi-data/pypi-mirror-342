# Enderlit Crypto

шифратор-дешифратор от Enderlit  


## Установка

```
pip install enderlit_crypto
```

## Использование

```python
from enderlit_crypto import enderlit_crypt, enderlit_decrypt

cipher = enderlit_crypt("hello world", 1)
plain = enderlit_decrypt(cipher, 1)

print(cipher)
print(plain)
```
