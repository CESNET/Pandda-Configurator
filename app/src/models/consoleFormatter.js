export const formatToConsole = (output) => {
    if (output == null) {
        return new Array();
    }

    return output.map(e => {
        return e.replace(/\n/gm, '');
    });
};
