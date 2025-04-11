<script setup>
import { ref, defineEmits, defineProps, toRaw, onMounted } from 'vue';
import { EMIT_TYPE } from '@/models/emits';
import InfoTooltip from '@/components/InfoTooltip.vue';

const emit = defineEmits([
    'submit',
    'back'
]);

const props = defineProps({
    store: {
        type: Object
    }
});

const probeList = ref(structuredClone(toRaw(props.store.config.probeList)));

const newProbeHost = ref('');
const newProbeSSHCredentials = ref('default');

const validate = () => {
    var form = document.getElementById('new-probe-form');
    form.classList.add('was-validated');
    return form.checkValidity();
};

const addServer = (event) => {
    if (!validate()) {
        return;
    }

    if (newProbeHost.value.trim() !== '') {
        probeList.value.push({
            host: newProbeHost.value,
            sshCredentials: newProbeSSHCredentials.value,
            customCredentials: {
                user: '',
                pass: '',
                type: 'sshLoginTypeKey'
            },
            ipfixprobeInstances: [],
            hugepages: 4
        });
        newProbeHost.value = '';
        newProbeSSHCredentials.value = 'default';
        document.getElementById('new-probe-form').classList.remove('was-validated');
    }
    if (event) {
        event.cancelBubble = true;
    }
};

const deleteServer = (index) => {
    probeList.value.splice(index, 1);
};

onMounted(async () => {
    document.getElementById("newProbeHost").focus();
});

const onFormSubmit = () => {
    props.store.config.probeList = probeList.value;
    emit('submit', EMIT_TYPE.SET_PROBES_CONN_INFO, props.store);
}
</script>

<template>
    <h1 class="component-title">Probes Setup</h1>

    <div class="mb-1">
        <h5>Add New Monitoring Probe</h5>
    </div>
    <form id="new-probe-form" @submit.prevent @keyup.enter="addServer" class="needs-validation" novalidate>
        <div class="row mb-2">
            <div class="input-group">
                <label class="input-group-text col-2" for="newProbeHost">Host</label>
                <input class="form-control" id="newProbeHost" type="text" v-model="newProbeHost" required />
                <InfoTooltip tooltipKey="probeHost" />
                <div class="invalid-feedback">
                    Host cannot be empty!
                </div>
            </div>
        </div>
        <div class="row mb-2">
            <div class="input-group">
                <span class="input-group-text col-2" for="credentialType">Credentials</span>
                <select class="form-select" id="credentialType" v-model="newProbeSSHCredentials" required>
                    <option value="default">Default credentials</option>
                    <option value="custom">Custom credentials</option>
                </select>
                <InfoTooltip tooltipKey="credentialsType" />
                <div class="invalid-feedback">
                    Credentials must be specified!
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <div class="col">
                <button class="btn btn-info w-100" type="button" @click="addServer(null)">Add</button>
            </div>
        </div>
    </form>

    <div class="mb-1">
        <h5>Monitoring Probes</h5>
    </div>
    <div class="mb-3">
        <table class=" table table-sm">
            <thead>
                <tr>
                    <th class="text-light bg-secondary" scope="col">Host</th>
                    <th class="text-light bg-secondary" scope="col">Credentials</th>
                    <th class="text-light bg-secondary" scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="probe, index in probeList" :key="probe">
                    <td class="col">{{ probe.host }}</td>
                    <td class="col">{{ probe.sshCredentials }}</td>
                    <td class="col"><a class="link-danger" @click="deleteServer(index)">Delete</a></td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="row" @keyup.enter="$emit('set-probes-conn-info', probeList)">
        <div class=" col">
            <button class="btn btn-primary w-100" type="button" @click="$emit('back', props.store)">Back</button>
        </div>
        <div class="col">
            <button class="btn btn-success w-100" type="button" @click="onFormSubmit">Next</button>
        </div>
    </div>
</template>
