import React, { useState } from 'react';
import axios from 'axios';

const Form = () => {
  const [text, setText] = useState('');
  const [encryptedText, setEncryptedText] = useState('');
  const [decryptedText, setDecryptedText] = useState('');

  const handleEncrypt = async () => {
    try {
      const response = await axios.post('http://localhost:5000/encrypt', { text });
      setEncryptedText(response.data.encryptedText);
      setDecryptedText(''); // Clear the decrypted text when a new encryption occurs
    } catch (error) {
      console.error('Error encrypting text:', error);
    }
  };

  const handleDecrypt = async () => {
    try {
      const response = await axios.post('http://localhost:5000/decrypt', { encryptedText });
      setDecryptedText(response.data.decryptedText);
    } catch (error) {
      console.error('Error decrypting text:', error);
    }
  };

  return (
    <div>
      <h1>RSA Encryption/Decryption</h1>
      <div>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to encrypt"
        />
      </div>
      <button onClick={handleEncrypt}>Encrypt</button>
      <div>
        <textarea
          value={encryptedText}
          onChange={(e) => setEncryptedText(e.target.value)}
          placeholder="Encrypted text will appear here"
        />
      </div>
      <button onClick={handleDecrypt}>Decrypt</button>
      <div>
        <textarea
          value={decryptedText}
          readOnly
          placeholder="Decrypted text will appear here"
        />
      </div>
    </div>
  );
};

export default Form;
