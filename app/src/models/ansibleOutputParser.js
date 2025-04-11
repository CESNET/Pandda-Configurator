export const parseAnsibleOutput = (output) => {
    if (output.length < 2) {
        return 1;
    }

    try {
        const resultLine = output[output.length - 2];
        const matchFailed = resultLine.match(/failed=(\d+)/);
        const cntFailed = matchFailed ? parseInt(matchFailed[1], 10) : null;

        if (cntFailed === null) {
            return 1;
        } else if (cntFailed > 0) {
            return 2;
        } else {
            return 0;
        }
    } catch (error) {
        console.log(error);
        return 1;
    }
};
