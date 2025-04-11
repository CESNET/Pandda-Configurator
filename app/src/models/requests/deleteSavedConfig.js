export const deleteSavedConfig = async () => {
    try {
        await fetch('http://localhost:8081/PANDDA_DELETE_CONFIG', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        });
        return true;
    } catch (error) {
        console.log(error);
        return false;
    }
};
