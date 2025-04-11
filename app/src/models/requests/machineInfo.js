export const sendMachineInfo = async (masterPassword, host) => {
    try {
        const response = await fetch('http://localhost:8081/MACHINE_INFO', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'host': host,
                'masterPassword': masterPassword
            })
        });
        return await response.json();
    } catch (error) {
        console.log(error);
        return false;
    }
};
