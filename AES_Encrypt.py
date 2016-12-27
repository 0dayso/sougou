# -*- coding: utf-8 -*-

"""
File Name : 'AES_Encrypt.py'
Description:
    Used in Mobile_Sogou_SPD.py
    AES encrption using ECB Mode
Author: 'gonghao'
Date: '2016/04/11' '15:18'
"""

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend
import base64


class AES_Encrypt(object):
    """
    AES Encrypt and Decrypt Processes Using ECB Mode
    """
    def __init__(self, key):
        u"""
        参数初始化
        """
        self.key = key

    def padding(self, text):
        u"""
        文本Padding方法：
        如果text不足16位就用空格补足为16位，
        如果大于16当时不是16的倍数，那就补足为16的倍数。
        """
        add = 16 - (len(text) % 16)
        return text + ('\0' * add)

    def encrypt(self, text):
        u"""
        加密过程
        """
        pad_text = self.padding(text)
        encryptor = Cipher(
            algorithms.AES(self.key),
            modes.ECB(),
            backend=default_backend()
        ).encryptor()

        ciphertext = encryptor.update(pad_text) + encryptor.finalize()

        return base64.b64encode(ciphertext)

    def decrypt(self, ciphertext):
        u"""
        解密过程
        """
        ciphertext = base64.b64decode(ciphertext)
        decryptor = Cipher(
            algorithms.AES(self.key),
            modes.ECB(),
            backend=default_backend()
        ).decryptor()

        pad_text = decryptor.update(ciphertext) + decryptor.finalize()
        return pad_text.replace('\0', '').strip()

if __name__ == '__main__':
    pc = AES_Encrypt('Sogou$Haoma$Tong')
    text = "hid=863784025395950&is=460023518863880&r=10110&dev=android&appvers=4.0.2.43271&rom=Tlg1MDVKXzQuNC4y&aid=8914b8b211b8f829&pid=32917970361c5334d15b6f38e54f1344&nm1=&cid=gsm_460_00_20944_230719238&search_type=1&words=13127771331&place=&lng=0.0&lat=0.0\0\0\0\0\0\0\0\0"
    en = pc.encrypt(text)
    print u"加密后: " + en
    de = pc.decrypt(en)
    print u"解密后: " + de
