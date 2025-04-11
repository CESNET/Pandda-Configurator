import { STATE } from "@/models/state";
import { customColCredsEnabled, isAdictEnabled, findNextCustomCredentials, getNextProbeIndex } from "@/models/utils";

const setMasterPassword = (store) => {
    store.state = STATE.GLOBAL_SSH_INIT;
    return store;
};

const setGlobalSSHCredentials = (store) => {
    store.state = STATE.COLLECTOR_SETTINGS;
    return store;
};

const setProbesConnInfo = (store) => {
    let nextCustomCredsIndex = findNextCustomCredentials(store.config.probeList);
    if (nextCustomCredsIndex !== false) {
        store.state = STATE.CUSTOM_PROBE_CREDENTIALS;
        store.probeIndex = nextCustomCredsIndex;
    } else {
        store.state = STATE.AUTO_DISCOVERY;
    }
    return store;
};

const setCredentials = (store, isCollector) => {
    if (isCollector) {
        if (isAdictEnabled(store)) {
            store.state = STATE.ADICT_SETTINGS;
        } else {
            store.state = STATE.PROBES_CONN_INFO;
        }
    } else {
        let nextCustomCredsIndex = findNextCustomCredentials(store.config.probeList, store.probeIndex);
        if (nextCustomCredsIndex !== false) {
            store.probeIndex = nextCustomCredsIndex;
        } else {
            store.state = STATE.AUTO_DISCOVERY;
        }
    }
    return store;
};

const setMachineInfo = (store) => {
    if (store.config.probeList.length > 0) {
        store.state = STATE.IPFIXPROBE_INPUT_SETUP;
        store.probeIndex = 0;
    } else {
        store.state = STATE.NEXT;
    }
    return store;
};

const setInstances = (store) => {
    let nextProbe = getNextProbeIndex(store.probeIndex, store.config.probeList.length);
    if (nextProbe !== false) {
        store.probeIndex = nextProbe;
    } else {
        store.state = STATE.NEXT;
    }
    return store;
};

const setCollectorSettings = (store) => {
    if (customColCredsEnabled(store)) {
        store.state = STATE.CUSTOM_COL_CREDENTIALS;
    } else if (isAdictEnabled(store)) {
        store.state = STATE.ADICT_SETTINGS;
    } else {
        store.state = STATE.PROBES_CONN_INFO;
    }
    return store;
};

const setAdictSettings = (store) => {
    store.state = STATE.PROBES_CONN_INFO;
    return store;
};

export {
    setMasterPassword,
    setGlobalSSHCredentials,
    setProbesConnInfo,
    setCredentials,
    setMachineInfo,
    setInstances,
    setCollectorSettings,
    setAdictSettings
};
