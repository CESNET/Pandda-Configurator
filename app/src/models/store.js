import { createEmptyConfig } from "@/models/emptyConfig";
import { STATE } from "@/models/state";

export const createEmptyStore = () => {
    return {
        state: STATE.MASTER_PASSWORD_SETUP,
        probeIndex: 0,
        config: createEmptyConfig()
    }
};
