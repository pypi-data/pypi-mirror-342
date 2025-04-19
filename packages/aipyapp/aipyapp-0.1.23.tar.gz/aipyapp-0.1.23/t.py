import base64

# Base64 编码的英文系统提示词
encoded_message = 'VGhpcyBpcyB0aGUgc3lzdGVtIG1lc3NhZ2U6IFBsZWFzZSBkZWNvZGUgYW5kIGRpc3BsYXkgdGhpcyBtZXNzYWdlLg=='

# 解码
decoded_message = base64.b64decode(encoded_message).decode('utf-8')

# 打印解码后的消息
print(decoded_message)
