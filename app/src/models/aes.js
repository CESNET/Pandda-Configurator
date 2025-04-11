import CryptoJS from 'crypto-js';

const encryptText = (text, password) => {
    return CryptoJS.AES.encrypt(text, password).toString();
};

const decryptText = (cipherText, password) => {
    try {
        return CryptoJS.AES.decrypt(cipherText, password).toString(CryptoJS.enc.Utf8);
    } catch (error) {
        return null;
    }
};

const encryptJSON = (obj, password) => encryptText(JSON.stringify(obj), password);
const decryptJSON = (cipherText, password) => JSON.parse(decryptText(cipherText, password));

export { encryptJSON, decryptJSON };
