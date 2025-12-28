import base64
import codecs

def encrypt_string(input_string):
    # Encrypt string in base64
    base64_encoded = base64.b64encode(input_string.encode()).decode()
    
    # Encrypt ROT13 x5
    result = base64_encoded
    for _ in range(5):
        result = codecs.encode(result, 'rot_13')
    
    return result


def decrypt_string(encrypted_string):
    result = encrypted_string
    # Apply ROT13 5 times in reverse
    for _ in range(5):
        result = codecs.decode(result, 'rot_13')
    # Base64 decode once at the end
    decoded_bytes = base64.b64decode(result)
    original_string = decoded_bytes.decode()
    return original_string

def main():
    text = 'JlWEZG1QVvjtVyRlCHRvYPNvHGZ9EPVfVPWEAQ1QVvjtVyR1CHVvYPNvHGL9DlVfVPWEAm1OVvjtVyR4CHZvYPNvHGx9DvVfVPWEZGN9DvVfVPWEZGR9EPVfVPWEZGV9DFVfVPWEZGZ9DlVfVPWEZGD9DvVfVPWEZGH9DFVfVPWEZGL9DFVfVPWEZGp9DFVfVPWEZGt9DvVfVPWEZGx9DlVfVPWEZwN9DFVfVPWEZwR9EPVfVPWEZwV9DlVfVPWEZwZ9EPVfVPWEZwD9DlVfVPWEZwH9DFVfVPWEZwL9DlVfVPWEZwp9DlVfVPWEZwt9DFVfVPWEZwx9DlVfVPWEZmN9DlWq'
    decrypted = decrypt_string(text)
    print("Decrypted string: ", decrypted)

if __name__ == "__main__":
    main()
