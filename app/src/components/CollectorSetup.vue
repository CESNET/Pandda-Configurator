<script setup>
import { ref, defineEmits, defineProps, onMounted } from 'vue';
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

const collector = ref(props.store.config.collector);

const newFwdHost = ref('');
const newFwdPort = ref(4739);
const newFwdProto = ref('TCP');

const addFwdTarget = (event) => {
    if (event) {
        event.cancelBubble = true;
    }

    var form = document.getElementById('new-fwd-form');
    form.classList.add('was-validated');
    if (form.checkValidity() === false) {
        return;
    }

    if (newFwdHost.value.trim() !== '') {
        collector.value.forwardingTargets.push({
            host: newFwdHost.value,
            port: newFwdPort.value,
            proto: newFwdProto.value,
        });
        newFwdHost.value = '';
        newFwdPort.value = 4739;
        newFwdProto.value = 'TCP';

        form.classList.remove('was-validated');
    }
}

const deleteFwdTarget = (index) => {
    collector.value.forwardingTargets.splice(index, 1);
};

const validate = () => {
    var form = document.getElementById('col-setup-form');
    form.classList.add('was-validated');
    return form.checkValidity();
};

const setPluginAsAlwaysEnabled = (pluginName) => {
    const index = props.store.config.defaultPlugins.findIndex(e => e.name === pluginName);
    props.store.config.defaultPlugins[index].enabled = "enabled";
    props.store.config.defaultPlugins[index].disableAllowed = false;
};

const setPluginAsDisabled = (pluginName) => {
    const index = props.store.config.defaultPlugins.findIndex(e => e.name === pluginName);
    props.store.config.defaultPlugins[index].enabled = "disabled";
    props.store.config.defaultPlugins[index].disableAllowed = true;
};

const onFormSubmit = () => {
    if (!validate()) {
        return;
    }

    props.store.config.collector = collector.value;
    if (collector.value.adict === 'true') {
        setPluginAsAlwaysEnabled('idpcontent');
    } else {
        setPluginAsDisabled('idpcontent');
    }
    emit('submit', EMIT_TYPE.SET_COLLECTOR_SETTINGS, props.store);
}

onMounted(async () => {
    document.getElementById("collectorHost").focus();
});
</script>

<template>
    <h1 class="component-title">Collector Setup</h1>
    <div class="container">
        <form id="col-setup-form" @submit.prevent @keyup.enter="onFormSubmit" class="needs-validation" novalidate>
            <div class="row mb-2">
                <div class="input-group">
                    <label class="input-group-text col-2" for="collectorHost">Host</label>
                    <input class="form-control" id="collectorHost" type="text" v-model="collector.host" required />
                    <InfoTooltip tooltipKey="collectorHost" />
                    <div class="invalid-feedback">
                        Host cannot be empty!
                    </div>
                </div>
            </div>

            <div class="row mb-2">
                <div class="input-group">
                    <label class="input-group-text col-2" for="port">Port</label>
                    <input class="form-control" type="number" id="port" v-model="collector.port" min="1" max="65535"
                        required />
                    <InfoTooltip tooltipKey="collectorPort" />
                    <div class="invalid-feedback">
                        Port must be from range 1-65535!
                    </div>
                </div>
            </div>

            <div class="row mb-2">
                <div class="input-group">
                    <span class="input-group-text col-2" for="protocol">Protocol</span>
                    <select class="form-select" id="protocol" v-model="collector.proto" required>
                        <option value="TCP">TCP</option>
                        <option value="UDP">UDP</option>
                    </select>
                    <InfoTooltip tooltipKey="collectorProtocol" />
                    <div class="invalid-feedback">
                        Protocol must be specified!
                    </div>
                </div>
            </div>

            <div class="row mb-2">
                <div class="input-group">
                    <span class="input-group-text col-2" for="credentialType">Credentials</span>
                    <select class="form-select" id="credentialType" v-model="collector.sshCredentials" required>
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
                <div class="input-group">
                    <span class="input-group-text col-2" for="adict">ADiCT Enabled</span>
                    <select class="form-select" id="adict" v-model="collector.adict" required>
                        <option value="true">Yes</option>
                        <option value="false">No</option>
                    </select>
                    <InfoTooltip tooltipKey="collectorADiCT" />
                    <div class="invalid-feedback">
                        You must specify if ADiCT will be enabled!
                    </div>
                </div>
            </div>
        </form>

        <form id="new-fwd-form" @submit.prevent @keyup.enter="addFwdTarget" class="needs-validation" novalidate>
            <div class="row mb-2">
                <h5>Forwarding targets</h5>
                <p>
                    Forwarding targets define an additional set of hosts (collectors), where the main central collector
                    will forward (send a copy) of the network flow telemetry.
                    <br />
                    For more info, see <a class="link-primary" target="_blank"
                        href="https://pandda.cesnet.cz/en/configurator#collector-setup-page">PANDDA
                        documentation</a> page.
                </p>
            </div>

            <div class="row mb-2" @submit.prevent @keyup.enter="addFwdTarget">
                <div class="col">
                    <div class="input-group">
                        <label class="input-group-text" for="newFwdHost">Host</label>
                        <input class="form-control" id="newFwdHost" type="text" v-model="newFwdHost" required />
                        <InfoTooltip tooltipKey="fwdHost" />
                        <div class="invalid-feedback">
                            Host cannot be empty!
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="input-group">
                        <label class="input-group-text" for="newFwdPort">Port</label>
                        <input class="form-control" id="newFwdPort" type="number" v-model="newFwdPort" min="1"
                            max="65535" required />
                        <InfoTooltip tooltipKey="fwdPort" />
                        <div class="invalid-feedback">
                            Port must be from range 1-65535!
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="input-group">
                        <span class="input-group-text" for="newFwdProtocol">Protocol</span>
                        <select class="form-select rounded-end" id="newFwdProtocol" v-model="newFwdProto" required>
                            <option value="TCP">TCP</option>
                            <option value="UDP">UDP</option>
                        </select>
                        <div class="invalid-feedback">
                            Protocol must be specified!
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mb-3">
                <div class="col">
                    <button class="btn btn-info w-100" type="button" @click="addFwdTarget(null)">Add</button>
                </div>
            </div>
        </form>

        <h6>Configured forwarding targets</h6>
        <div class="row mb-3">
            <div class="col">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th class="text-light bg-secondary" scope="col">Target Host</th>
                            <th class="text-light bg-secondary" scope="col">Target Port</th>
                            <th class="text-light bg-secondary" scope="col">Protocol</th>
                            <th class="text-light bg-secondary" scope="col">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="target in collector.forwardingTargets" :key="target">
                            <td class="col">{{ target.host }}</td>
                            <td class="col">{{ target.port }}</td>
                            <td class="col">{{ target.proto }}</td>
                            <td class="col"><a class="link-danger" @click="deleteFwdTarget(index)">Delete</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <button class="btn btn-primary w-100" type="button" @click="$emit('back', props.store)">Back</button>
            </div>
            <div class="col">
                <button class="btn btn-success w-100" type="button" @click="onFormSubmit">Next</button>
            </div>
        </div>

    </div>
</template>

<style scoped>
.font-size-12em {
    margin-top: 4px;
}

.w-100 {
    width: 100%;
}
</style>
