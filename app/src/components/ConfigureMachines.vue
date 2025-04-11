<script setup>
import { ref, defineEmits, onMounted } from 'vue';
import { formatToConsole } from '@/models/consoleFormatter.js';
import { submitConfig } from '@/models/requests/submitConfig.js';
import { runAnsible } from '@/models/requests/runAnsible.js';
import { checkAnsibleStatus } from '@/models/requests/checkAnsibleStatus.js';
import { parseAnsibleOutput } from '@/models/ansibleOutputParser';

defineEmits([
    'back'
]);

const props = defineProps({
    store: {
        type: Object,
        required: true
    },
});

const runningPid = ref(0);
const cmdOutput = ref(new Array());
let timer = null;
const hosts = ref(new Array());
const selectedHost = ref('All');
const ansibleResult = ref(0);
let releaseDisabled = ref(true);

const warnAboutLeave = (event) => {
    event.preventDefault();
    event.returnValue = "";
};

const extractMachinesFromConfig = () => {
    let hosts = new Array();
    hosts.push('All');
    hosts.push(props.store.config.collector.host);
    for (let index = 0; index < props.store.config.probeList.length; ++index) {
        if (!hosts.includes(props.store.config.probeList[index].host)) {
            hosts.push(props.store.config.probeList[index].host);
        }
    }
    return hosts;
};

const obtainedConfig = ref({});

const submitAgain = async () => {
    const config = await submitConfig(props.store.config.masterPassword, props.store.config);
    if (config !== false) {
        obtainedConfig.value = config;
        hosts.value = extractMachinesFromConfig(JSON.parse(config));
        releaseDisabled.value = false;
    }
};

const release = async () => {
    window.addEventListener("beforeunload", warnAboutLeave);
    const response = await runAnsible(props.store.config.masterPassword, selectedHost.value);
    if (response !== false) {
        runningPid.value = response.PID;
        cmdOutput.value = new Array();
        timer = setInterval(checkStatus, 1000);
    }
}

const checkStatus = async () => {
    const response = await checkAnsibleStatus(runningPid.value);
    if (response !== false) {
        cmdOutput.value = formatToConsole(response.output);
        if (!response.isRunning) {
            clearInterval(timer);
            timer = null;
            runningPid.value = 0;
            window.removeEventListener("beforeunload", warnAboutLeave);
            ansibleResult.value = parseAnsibleOutput(cmdOutput.value);
            $('#ansibleFinishedModal').modal();
        }
    }
}

onMounted(async () => {
    submitAgain();
});
</script>

<template>
    <h1 class="component-title">Configure Machines</h1>

    <div class="row mb-2">
        <p>
            Monitoring infrastructure based on the inputted configuration will be installed via Ansible at this stage.
            You can either select to install all machines, or choose a specific machine to install. If you wish to see
            the exact output of the running Ansible, you can expand the Console card.
        </p>
        <p>
            <strong>Do not close or reload the page while the Ansible is running!</strong>
        </p>
    </div>

    <div class="row mb-2">
        <div class="input-group">
            <span class="input-group-text col-3" for="hostToConfigure">Server to Configure</span>
            <select class="form-select rounded-end" id="hostToConfigure" v-model="selectedHost">
                <option v-for="host in hosts" :key="host" :value="host">{{ host }}</option>
            </select>
        </div>
    </div>
    <div class="row mb-3">
        <div class="col">
            <button v-if="runningPid == 0" class="btn btn-success w-100" type="button" @click="release"
                :disabled="releaseDisabled">Release
                PANDDA</button>
            <button v-else class="btn btn-success w-100" type="button" disabled>
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Installing {{ selectedHost }}...
            </button>
        </div>
    </div>

    <div id="accordion" class="mb-3">
        <div class="card">
            <div class="card-header" id="headingOne">
                <h5 class="mb-0">
                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="false"
                        aria-controls="collapseOne">Console</button>
                </h5>
            </div>

            <div id="collapseOne" class="collapse collapsed" aria-labelledby="headingOne" data-parent="#accordion">
                <div class="card-body">
                    <div class="alert alert-dark console-viewer" role="alert" id="console">
                        <span v-for="line in cmdOutput">{{ line }}<br /></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row mb-2">
        <div class="col">
            <button class="btn btn-primary w-100" type="button" @click="$emit('back', props.store)">Back</button>
        </div>
    </div>

    <div class="modal fade" id="ansibleFinishedModal" tabindex="-1" role="dialog"
        aria-labelledby="ansibleFinishedModalTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="ansibleFinishedModal">Provision finished!</h5>
                    <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p v-if="ansibleResult == 0">
                        Ansible provisioning finished successfully!
                        <br />
                        You can check the Ansible output in the Console.
                    </p>
                    <p v-else-if="ansibleResult == 2">
                        Ansible provisioning <span class="text-danger fw-bold">finished with errors!</span>
                        <br />
                        Check the Ansible output in the Console!
                    </p>
                    <p v-else>
                        Ansible provisioning <span class="text-danger fw-bold">failed unexpectedly!</span>
                        <br />
                        Check the Ansible output in the Console!
                    </p>
                </div>
                <div class="modal-footer">
                    <button v-if="ansibleResult == 0" type="button" class="btn btn-secondary"
                        data-dismiss="modal">Close</button>
                    <button v-else type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.console-viewer {
    height: 360px;
    overflow: auto;
}

.space {
    min-width: 12px;
    display: inline-block;
}

.btn-link-text {
    text-decoration: underline;
}
</style>
