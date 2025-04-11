import { STATE } from "@/models/state.js";
import { customColCredsEnabled, isAdictEnabled, findNextCustomCredentials, findPrevCustomCredentials, getNextProbeIndex, getPrevProbeIndex } from "@/models/utils";

const prevStateForAdict = (store) => {
    store.state = customColCredsEnabled(store) ? STATE.CUSTOM_COL_CREDENTIALS : STATE.COLLECTOR_SETTINGS;
    return store;
};

const prevStateForProbesConnInfo = (store) => {
    if (isAdictEnabled(store)) {
        store.state = STATE.ADICT_SETTINGS;
        return store;
    } else {
        return prevStateForAdict(store);
    }
};

const prevStateForCustomProbeCreds = (store) => {
    const prevIndex = findPrevCustomCredentials(store.config.probeList, store.probeIndex);
    if (prevIndex !== false) {
        store.probeIndex = prevIndex;
        store.state = STATE.CUSTOM_PROBE_CREDENTIALS;
    } else {
        store.state = STATE.PROBES_CONN_INFO;
    }
    return store;
};

const prevStateForAutoDiscovery = (store) => {
    const prevIndex = findPrevCustomCredentials(store.config.probeList);
    if (prevIndex !== false) {
        store.probeIndex = prevIndex;
        store.state = STATE.CUSTOM_PROBE_CREDENTIALS;
    } else {
        store.state = STATE.PROBES_CONN_INFO;
    }
    return store;
};

const prevStateFoIpfixprobe = (store) => {
    const prevProbe = getPrevProbeIndex(store.probeIndex);
    if (prevProbe !== false) {
        store.probeIndex = prevProbe;
        store.state = STATE.IPFIXPROBE_INPUT_SETUP;
    } else {
        store.state = STATE.AUTO_DISCOVERY;
    }
    return store;
};

const prevStateForNext = (store) => {
    if (store.config.probeList.length > 0) {
        store.probeIndex = store.config.probeList.length - 1;
        store.state = STATE.IPFIXPROBE_INPUT_SETUP;
    } else {
        store.state = STATE.AUTO_DISCOVERY;
    }
    return store;
};

const handleOnBack = (store) => {
    if (store.state === STATE.MASTER_PASSWORD_SETUP) {
        store.state = STATE.MASTER_PASSWORD_SETUP;
    } else if (store.state === STATE.GLOBAL_SSH_INIT) {
        store.state = STATE.MASTER_PASSWORD_SETUP;
    } else if (store.state === STATE.COLLECTOR_SETTINGS) {
        store.state = STATE.GLOBAL_SSH_INIT;
    } else if (store.state === STATE.CUSTOM_COL_CREDENTIALS) {
        store.state = STATE.COLLECTOR_SETTINGS;
    } else if (store.state === STATE.ADICT_SETTINGS) {
        store = prevStateForAdict(store);
    } else if (store.state === STATE.PROBES_CONN_INFO) {
        store = prevStateForProbesConnInfo(store);
    } else if (store.state === STATE.CUSTOM_PROBE_CREDENTIALS) {
        store = prevStateForCustomProbeCreds(store);
    } else if (store.state === STATE.AUTO_DISCOVERY) {
        store = prevStateForAutoDiscovery(store);
    } else if (store.state === STATE.IPFIXPROBE_INPUT_SETUP) {
        store = prevStateFoIpfixprobe(store);
    } else if (store.state === STATE.NEXT) {
        store = prevStateForNext(store);
    }

    return store;
};

export { handleOnBack };
