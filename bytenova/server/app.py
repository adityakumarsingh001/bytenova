from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

app = Flask(__name__)
CORS(app)

# Generate RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3084
)
public_key = private_key.public_key()

# Serialize the keys
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    text = data['text'].encode()

    encrypted_text = public_key.encrypt(
        text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return jsonify({'encryptedText': encrypted_text.hex()})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    encrypted_text = bytes.fromhex(data['encryptedText'])

    decrypted_text = private_key.decrypt(
        encrypted_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return jsonify({'decryptedText': decrypted_text.decode()})

if __name__ == '__main__':
    app.run(debug=True)
