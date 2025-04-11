export const getSSHKey = async (forceNewKey = false) => {
    try {
        const rawResponse = await fetch('http://localhost:8081/SSH_GET_KEY', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "forceNew": forceNewKey
            })
        });
        const jsonReponse = await rawResponse.json();
        return jsonReponse["pubKey"];;
    } catch (error) {
        console.log(error);
        return false;
    }
};
