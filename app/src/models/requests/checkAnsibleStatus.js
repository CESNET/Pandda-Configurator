export const checkAnsibleStatus = async (pid) => {
    try {
        const response = await fetch('http://localhost:8081/ANSIBLE_STATUS', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'pid': pid
            })
        });
        const json = await response.json();
        return json;
    } catch (error) {
        console.log(error);
        return false;
    }
};
