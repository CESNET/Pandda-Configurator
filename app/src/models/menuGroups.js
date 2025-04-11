import { STATE } from './state.js'

export const MENU_GROUP = {
    GLOBAL: 'Default Access Setup',
    COLLECTOR: 'Collector',
    PROBES: 'Probes',
    RUNNER: 'Configure'
};

export const MENU_GROUP_ITEMS = [
    { state: STATE.MASTER_PASSWORD_SETUP, parent: MENU_GROUP.GLOBAL, itemText: () => 'Master Password' },
    { state: STATE.GLOBAL_SSH_INIT, parent: MENU_GROUP.GLOBAL, itemText: () => 'SSH' },

    { state: STATE.COLLECTOR_SETTINGS, parent: MENU_GROUP.COLLECTOR, itemText: () => 'Collector' },
    { state: STATE.CUSTOM_COL_CREDENTIALS, parent: MENU_GROUP.COLLECTOR, itemText: () => 'Custom Credentials' },
    { state: STATE.ADICT_SETTINGS, parent: MENU_GROUP.COLLECTOR, itemText: () => 'ADiCT' },

    { state: STATE.PROBES_CONN_INFO, parent: MENU_GROUP.PROBES, itemText: () => 'Connection Info' },
    {
        state: STATE.CUSTOM_PROBE_CREDENTIALS,
        parent: MENU_GROUP.PROBES,
        itemText: (current, total) => {
            if (!total || total == 0) {
                return 'Custom Credentials';
            }
            return `Custom Credentials ${current + 1} of ${total}`
        }
    },
    { state: STATE.AUTO_DISCOVERY, parent: MENU_GROUP.PROBES, itemText: () => 'Auto Detection' },
    {
        state: STATE.IPFIXPROBE_INPUT_SETUP,
        parent: MENU_GROUP.PROBES,
        itemText: (current, total) => {
            if (!total || total == 0) {
                return 'Input Setup';
            }
            return `Input Setup ${current + 1} of ${total}`
        }
    },

    { state: STATE.NEXT, parent: MENU_GROUP.RUNNER, itemText: () => 'Configure Machines' },
];
