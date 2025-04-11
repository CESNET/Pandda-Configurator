const filterCustomCredsOnly = (probeList) => {
    return probeList.filter(probe => probe.sshCredentials === 'custom');
};

const findNextCustomCredentials = (probeList, startIndex = -1) => {
    const index = probeList.findIndex((probe, index) => index > startIndex && probe.sshCredentials === 'custom');
    return index === -1 ? false : index;
}

const findPrevCustomCredentials = (probeList, startIndex = -1) => {
    startIndex = startIndex === -1 ? probeList.length : startIndex;
    const index = probeList.findLastIndex((probe, index) => index < startIndex && probe.sshCredentials === 'custom');
    return index === -1 ? false : index;
}

const getNextProbeIndex = (currentIndex, maxIndex) => {
    currentIndex += 1;
    if (currentIndex >= maxIndex) {
        return false;
    }
    return currentIndex;
}

const getPrevProbeIndex = (currentIndex) => {
    currentIndex -= 1;
    if (currentIndex < 0) {
        return false;
    }
    return currentIndex;
}

const customColCredsEnabled = (store) => {
    return store.config.collector.sshCredentials === 'custom';
};

const isAdictEnabled = (store) => {
    return store.config.collector.adict === 'true';
};

export { filterCustomCredsOnly, findNextCustomCredentials, findPrevCustomCredentials };
export { getNextProbeIndex, getPrevProbeIndex };
export { customColCredsEnabled, isAdictEnabled };
