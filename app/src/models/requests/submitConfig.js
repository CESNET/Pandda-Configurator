import { encryptJSON } from '@/models/aes.js';

export const submitConfig = async (masterPassword, config) => {
    try {
        const response = await fetch('http://localhost:8081/PANDDA_CREATE_CONFIG', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'config': config,
                'encrypted': encryptJSON(config, masterPassword)
            })
        });
        return JSON.stringify(await response.json());
    } catch (error) {
        console.log(error);
        return false;
    }
};
