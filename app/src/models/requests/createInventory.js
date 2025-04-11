export const sendCreateInventory = async (config) => {
    try {
        await fetch('http://localhost:8081/ANSIBLE_CREATE_INVENTORY', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'config': config
            })
        });
        return true;
    } catch (error) {
        console.log(error);
        return false;
    }
};
