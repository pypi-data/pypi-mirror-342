# -*- coding: UTF-8 -*-
# python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from devolib.util_log import LOG_D
from devolib.util_str import bytes_to_str_with_hex, str_to_bytes, bytes_to_str

# MARK: sim

'''
关于填充: PKCS7
标准 PKCS#7 填充方案利用的仅是最后一个字节来存储填充长度.
如果需要填充 3 个字节，则填充 \x03\x03\x03。
如果需要填充 1 个字节，则填充 \x01。

只要分块大小别变态大（大于255），该填充算法就没有问题
'''

'''
@brief sim encryption
'''
def sim_encrypt_decrypt(bytes, salt):
    result = bytearray(bytes)
    for i in range(len(result)): # 逐字节进行 XOR 操作
        result[i] ^= salt
    return result

def sim_cipher_encrypt(plain_text, salt):
    return sim_encrypt_decrypt(plain_text, salt)

def sim_cipher_decrypt(cipher_bytes, salt):
    return sim_encrypt_decrypt(cipher_bytes, salt)

# MARK: aes

# 生成随机的AES密钥（16, 24, 或 32 字节）
def generate_key(key_size=32):
    return get_random_bytes(key_size)

# 填充函数
def custom_pad(value, block_size=16):
    while len(value.encode('utf-8')) % 16 != 0:
        value += '\x00'  # 补全, 明文和key都必须是16的倍数
    return value.encode('utf-8')

def aes_encrypt(data: str, key: bytes) -> str:
    # 创建 AES cipher 对象
    cipher = AES.new(key, AES.MODE_CBC)
    
    # 将数据填充到 16 字节的倍数
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    
    # 以 Base64 格式返回，加密的文本以及初始化向量（iv）
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ciphertext = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ciphertext

def aes_encrypt_without_b64(data: str, key: bytes, iv: bytes) -> bytes:
    # 确保密钥和IV的长度符合 AES 标准要求
    assert len(key) in {16, 24, 32}, f"Invalid key length. Must be 16, 24, or 32 bytes. Now is {key.count}"
    assert len(iv) == 16, "IV must be 16 bytes"

    # LOG_D(f"aes key len: {len(key)}, value: {key}")
    # LOG_D(f"aes iv len: {len(iv)}, value: {iv}")
    
    # 创建 AES cipher 对象
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # LOG_D(f"aes block len: {AES.block_size}")
    # LOG_D(f"aes data: {data}")
    
    # 将数据填充到 16 字节的倍数
    str1 = custom_pad(data, AES.block_size)
    # str1 = pad(data.encode(), AES.block_size)
    # str1 = data.encode()

    LOG_D(f"aes str1: {str1}")
    LOG_D(f"aes str1 bytes: {bytes_to_str_with_hex(str1)}")

    ct_bytes = cipher.encrypt(str1)
    
    return ct_bytes

'''
@brief AES 解密
'''
def aes_decrypt(iv: str, ciphertext: str, key: bytes) -> str:
    # 解码 Base64 编码的 iv 和 ciphertext
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)
    
    # 创建 AES cipher 对象
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 解密并去除填充
    pt_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return pt_bytes.decode()

def custom_unpad(data: bytes, block_size: int) -> bytes:
    return data.rstrip(b'\x00')

def aes_decrypt_without_b64(encrypted_bytes: bytes, key: bytes, iv: bytes) -> bytes:
    # 确保密钥和 IV 长度符合 AES 标准要求
    assert len(key) in {16, 24, 32}, f"Invalid key length. Must be 16, 24, or 32 bytes. Now is {len(key)}"
    assert len(iv) == 16, "IV must be 16 bytes"

    LOG_D(f"aes encrypted_bytes: {encrypted_bytes}")
    LOG_D(f"aes key: {key}")
    LOG_D(f"aes iv: {iv}")
    
    # 使用 AES 解密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    LOG_D(f"aes decrypted_bytes: {decrypted_bytes}")
    
    # 去除填充并解码为字符串
    return custom_unpad(decrypted_bytes, AES.block_size)

#MARK: main
'''
@brief Main test
'''

if __name__ == '__main__':
    '''
    Test sim
    '''
    key = "--"
    salt = 0xAA

    LOG_D(f"plain text: {key}")

    cipher_bytes = str_to_bytes(key)
    LOG_D(f"cipher bytes: {bytes_to_str_with_hex(cipher_bytes, ', 0x')}")

    # 加密密钥
    encrypted_bytes = sim_cipher_encrypt(str_to_bytes(key), salt)
    LOG_D(f"encrypted bytes: {bytes_to_str_with_hex(encrypted_bytes, ', 0x')}")

    # 解密密钥
    decrypted_key = sim_cipher_decrypt(encrypted_bytes, salt)
    LOG_D(f"decrypted text: {bytes_to_str(decrypted_key)}")

    '''
    Test aes
    '''
    LOG_D(f"===========> test aes")

    iv_key = "---"
    aes_key = "---"
    plain_text = "i am rot"
    LOG_D(f"plain text: {plain_text}")
    
    # 加密
    encrypted_data = aes_encrypt_without_b64(plain_text, str_to_bytes(aes_key), str_to_bytes(iv_key))
    print(f"Encrypted text: {encrypted_data}")
    print(f'Encrypted bytes: {bytes_to_str_with_hex(encrypted_data, " ")}')
    
    # 解密
    decrypted_bytes = aes_decrypt_without_b64(encrypted_data, str_to_bytes(aes_key), str_to_bytes(iv_key))
    print(f"Decrypted bytes: {decrypted_bytes}")
    print(f"Encrypted text: {bytes_to_str(decrypted_bytes)}")


    '''
    Test with bytes
    '''
    CASE_NAME = "[Test with bytes] "

    CIPHER_FOR_CIPHER_BYTES = [0xc7, 0xc4, 0xc5, 0xda, 0xcb, 0xcf, 0xcc, 0xcd, 0xc2, 0xc3, 0xc0, 0xc4, 0xc5, 0xda, 0xdb, 0xd8]
    CIPHER_FOR_CIPHER_SALT = 0xAA
    CIPHER_FOR_CIPHER_IV = [0x9b, 0x98, 0xcb, 0xcb, 0xec, 0xee, 0xf9, 0xeb, 0xc1, 0xcb, 0xc7, 0xcc, 0xce, 0xd9, 0xcb, 0x9b]

    cipher_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_BYTES, salt=CIPHER_FOR_CIPHER_SALT)
    iv_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_IV, salt=CIPHER_FOR_CIPHER_SALT)
    conf_str_encrypted = aes_encrypt_without_b64(plain_text, cipher_decrypted, iv_decrypted)

    print(f'{CASE_NAME}Encrypted bytes: {bytes_to_str_with_hex(conf_str_encrypted, " ")}')
