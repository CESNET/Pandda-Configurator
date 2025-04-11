<script setup>
import { ref, defineEmits } from 'vue';
import { formatToConsole } from '@/models/consoleFormatter';
import { sendCreateInventory } from '@/models/requests/createInventory';
import { sendMachineInfo } from '@/models/requests/machineInfo';
import { EMIT_TYPE } from '@/models/emits';

const emit = defineEmits([
    'submit',
    'back'
]);

const props = defineProps({
    store: {
        type: Object,
        required: true
    },
});

const machineInfoToView = (machineInfo) => {
    const keys = Object.keys(machineInfo);
    let views = new Array();
    for (let idx = 0; idx < keys.length; ++idx) {
        if (Object.keys(machineInfo[keys[idx]]).length == 0) {
            views.push({
                host: keys[idx],
                cpu: 'Error',
                memory: 'Error',
                net_devs: 'Error',
                dpdk_devs: 'Error',
            })
        } else {
            const current = machineInfo[keys[idx]];
            views.push({
                host: keys[idx],
                cpu: current.cpu_info.cpu_count,
                memory: current.mem_info.memory_in_kB,
                net_devs: current.net_interfaces.join(', '),
                dpdk_devs: current.dpdk_devices.map(e => e.device).join(', '),
            });
        }
    }
    return views;
};

let currentHost = ref('');
const cmdOutput = ref(new Array());

let machineInfo = props.store.config.machineInfo;
const machineInfoView = ref(machineInfoToView(machineInfo));
const nextDisabled = ref(true);
const isRunning = ref(false);

const warnAboutLeave = (event) => {
    event.preventDefault();
    event.returnValue = "";
};

const extractMachinesFromConfig = (config) => {
    let hosts = new Array();
    hosts.push(config.collector.host);
    for (let index = 0; index < config.probeList.length; ++index) {
        if (!hosts.includes(config.probeList[index].host)) {
            hosts.push(config.probeList[index].host);
        }
    }

    return hosts;
};

const hosts = extractMachinesFromConfig(props.store.config);

const runAutoDetection = async () => {
    isRunning.value = true;
    nextDisabled.value = true;
    cmdOutput.value = new Array();
    window.addEventListener("beforeunload", warnAboutLeave);

    if (! await sendCreateInventory(props.store.config)) {
        alert('Error occurred in request, try again!');
        return;
    }

    for (let idx = 0; idx < hosts.length; ++idx) {
        currentHost.value = hosts[idx];
        const response = await sendMachineInfo(props.store.config['masterPassword'], currentHost.value);
        cmdOutput.value.push(...formatToConsole(response.ad_output));
        machineInfo[currentHost.value] = response.machine_info;
        machineInfoView.value = machineInfoToView(machineInfo);
    }

    window.removeEventListener("beforeunload", warnAboutLeave);
    currentHost.value = '';
    isRunning.value = false;
    nextDisabled.value = false;
};

const onFormSubmit = () => {
    props.store.config.machineInfo = machineInfo;
    emit('submit', EMIT_TYPE.SET_MACHINE_INFO, props.store);
}
</script>

<template>
    <h1 class="component-title">Auto Detection</h1>

    <div class="row mb-2">
        <p>
            Auto detection playbook will be run on each previously configured machine to assess its CPUs, RAM and
            network devices. Please note that <samp>dpdk-tools</samp> package <strong>will be installed</strong> on
            target machines! If you wish to see the exact output of the Ansible, you can expand the Console
            card.
        </p>
        <p>
            <strong>Do not close or reload the page while the Ansible is running!</strong>
        </p>
    </div>

    <div class="row mb-3">
        <div class="col">
            <button v-if="!isRunning" class="btn btn-success w-100" type="button" @click="runAutoDetection">Run
                auto detection</button>
            <button v-else class="btn btn-success w-100" type="button" disabled>
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Running auto detection for {{ currentHost }}...
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

    <h5>Obtained information about the machines</h5>
    <div class="mb-3">
        <table class=" table table-sm">
            <thead>
                <tr>
                    <th class="text-light bg-secondary" scope="col">Host</th>
                    <th class="text-light bg-secondary" scope="col">CPU Count</th>
                    <th class="text-light bg-secondary" scope="col">Memory in kB</th>
                    <th class="text-light bg-secondary" scope="col">Net Devices</th>
                    <th class="text-light bg-secondary" scope="col">DPDK Devices</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="view in machineInfoView" :key="view">
                    <td class="col">{{ view.host }}</td>
                    <td class="col">{{ view.cpu }}</td>
                    <td class="col">{{ view.memory }}</td>
                    <td class="col">{{ view.net_devs }}</td>
                    <td class="col">{{ view.dpdk_devs }}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="row">
        <div class="col">
            <button class="btn btn-primary w-100" type="button" :disabled="isRunning"
                @click="$emit('back', props.store)">Back</button>
        </div>
        <div class="col">
            <button class="btn btn-success w-100" type="button" :disabled="nextDisabled"
                @click="onFormSubmit">Next</button>
        </div>
    </div>
</template>

<style scoped>
.space {
    min-width: 12px;
    display: inline-block;
}

.btn-link-text {
    text-decoration: underline;
}
</style>
