from flask import Flask, render_template, request
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import new as Random
from base64 import b64encode, b64decode

app = Flask(__name__)

#Set up the RSA keys
randon_generator = Random().read
set_of_keys = RSA.generate(1024, randon_generator)

public_key = set_of_keys.publickey()

# Defining Routes
@app.route('/')
def index():
        return render_template('index.html')
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        message = request.form['message']
        isEncry = request.form['isEncry']
        
        # Validating input
        if message == '':
            return render_template('index.html', message='Please enter required fields')
        elif len(message) > 200 and isEncry == 'true':
            return render_template('index.html', message='Please insert an string with less than 200 characters')
        # Encrypting Message        
        if isEncry == 'true':
            bit_message = b64encode(message.encode())
            cyphered_encryption = PKCS1_v1_5.new(set_of_keys)
            encrypted_message = b64encode(cyphered_encryption.encrypt(bit_message)).decode()

            return render_template('index.html' , encrypted=encrypted_message, type='Encrypted')
        # Decrypting Message
        else:
            bit_message = b64decode(message.encode())
            cyphered_decryption = PKCS1_v1_5.new(set_of_keys)
            encrypted_message = b64decode(cyphered_decryption.decrypt(bit_message,16)).decode()
            return render_template('index.html' , encrypted=encrypted_message, type='Decrypted')


if __name__ == '__main__':
        
        app.run()
