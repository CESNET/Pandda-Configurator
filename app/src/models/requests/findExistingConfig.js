export const findExistingConfig = async () => {
    try {
        const rawResponse = await fetch('http://localhost:8081/PANDDA_LOAD_CONFIG', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        });
        const response = await rawResponse.json();
        return response;
    } catch (error) {
        console.log(error);
        return '';
    }
};
