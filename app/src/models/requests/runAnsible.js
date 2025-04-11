export const runAnsible = async (masterPassword, host) => {
    try {
        const response = await fetch('http://localhost:8081/ANSIBLE_RUN', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'host': host,
                'password': masterPassword
            })
        });
        const json = await response.json();
        return json;
    } catch (error) {
        console.log(error);
        return false;
    }
};
