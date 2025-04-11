import * as emitHandlers from '@/models/emitHandlers';
import { EMIT_TYPE } from '@/models/emits';

const chooseHandler = (emitName) => {
    switch (emitName) {
        case EMIT_TYPE.SET_ADICT_SETTINGS:
            return emitHandlers.setAdictSettings;
        case EMIT_TYPE.SET_MASTER_PASSWORD:
            return emitHandlers.setMasterPassword;
        case EMIT_TYPE.SET_SSH_LOGIN:
            return emitHandlers.setGlobalSSHCredentials;
        case EMIT_TYPE.SET_PROBES_CONN_INFO:
            return emitHandlers.setProbesConnInfo;
        case EMIT_TYPE.SET_CREDENTIALS:
            return emitHandlers.setCredentials;
        case EMIT_TYPE.SET_MACHINE_INFO:
            return emitHandlers.setMachineInfo;
        case EMIT_TYPE.SET_IPFIXPROBE_SETTINGS:
            return emitHandlers.setInstances;
        case EMIT_TYPE.SET_COLLECTOR_SETTINGS:
            return emitHandlers.setCollectorSettings;
    }
};

const handleOnSubmit = (emitName, appStore, custom) => {
    const handler = chooseHandler(emitName);
    return handler(appStore, custom);
};

export { handleOnSubmit };
