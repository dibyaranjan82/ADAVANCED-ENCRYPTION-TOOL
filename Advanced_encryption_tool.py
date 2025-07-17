import os
import base64
from tkinter import filedialog, Tk, Button, Label, Entry
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(filepath, password):
    salt = os.urandom(16)
    key = generate_key(password, salt)
    fernet = Fernet(key)

    with open(filepath, 'rb') as file:
        data = file.read()

    encrypted = fernet.encrypt(data)

    with open(filepath + ".enc", 'wb') as file:
        file.write(salt + encrypted)

def decrypt_file(filepath, password):
    with open(filepath, 'rb') as file:
        data = file.read()

    salt = data[:16]
    encrypted = data[16:]
    key = generate_key(password, salt)
    fernet = Fernet(key)

    decrypted = fernet.decrypt(encrypted)

    with open(filepath.replace(".enc", ".dec"), 'wb') as file:
        file.write(decrypted)

# GUI
def browse_encrypt():
    path = filedialog.askopenfilename()
    encrypt_file(path, password_entry.get())
    status_label.config(text="File Encrypted Successfully!")

def browse_decrypt():
    path = filedialog.askopenfilename()
    decrypt_file(path, password_entry.get())
    status_label.config(text="File Decrypted Successfully!")

root = Tk()
root.title("Advanced Encryption Tool")
root.geometry("400x200")

Label(root, text="Enter Password:").pack()
password_entry = Entry(root, show='*', width=40)
password_entry.pack()

Button(root, text="Encrypt File", command=browse_encrypt).pack(pady=10)
Button(root, text="Decrypt File", command=browse_decrypt).pack(pady=10)

status_label = Label(root, text="")
status_label.pack()

root.mainloop()
