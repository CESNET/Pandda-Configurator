<script setup>
import { ref, defineProps, defineEmits, toRaw, onMounted } from 'vue';
import { machineInfoToRaw, machineInfoToDPDK } from '@/models/machineInfoToOptions.js';
import { EMIT_TYPE } from '@/models/emits.js';
import InfoTooltip from '@/components/InfoTooltip.vue';
import { checkInterfaces } from '@/models/checkInterfaces';

const props = defineProps({
    store: {
        type: Object
    }
});

const probeInfo = props.store.config.probeList[props.store.probeIndex];
const machineInfoAvailable = Object.keys(props.store.config.machineInfo[probeInfo.host]).length > 0;
const rawDevices = machineInfoAvailable ? machineInfoToRaw(props.store.config.machineInfo[probeInfo.host]) : new Array();
const dpdkDevices = machineInfoAvailable ? machineInfoToDPDK(props.store.config.machineInfo[probeInfo.host]) : new Array();
const hugepages = ref(probeInfo.hugepages);
let nextLinkID = props.store.config.nextLinkID;

const createNewInstance = () => {
    return {
        host: props.store.config.collector.host,
        port: props.store.config.collector.port,
        linkID: nextLinkID,
        cacheSize: 20,
        activeTimeout: 120,
        passiveTimeout: 300,
        useTCP: props.store.config.collector.proto,
        inputType: 'RAW',
        raw: {
            ifcName: rawDevices.length > 0 ? rawDevices[0].name : '',
            blocks: 2048,
            packets: 32
        },
        dpdk: {
            device: dpdkDevices.length > 0 ? dpdkDevices[0].device : '',
            hugepages: 4,
            rxQueues: 1,
            mempoolSize: 8192,
            burstSize: 64,
            ealOpts: ''
        },
        pcap_live: {
            ifc: rawDevices.length > 0 ? rawDevices[0].name : ''
        },
        plugins: structuredClone(toRaw(props.store.config.defaultPlugins))
    };
}

const emit = defineEmits([
    'submit',
    'back'
]);

const targetCollector = props.store.config.collector.proto.toLowerCase() + '://' + props.store.config.collector.host + ':' + props.store.config.collector.port;
const newInstance = ref(createNewInstance());
const instances = ref(structuredClone(toRaw(props.store.config.probeList[props.store.probeIndex].ipfixprobeInstances)));

const validate = () => {
    var form = document.getElementById('ipfixprobe-instance-form');
    form.classList.add('was-validated');
    return form.checkValidity();
};

const addInstance = (event) => {
    if (!validate()) {
        return;
    }

    if (!checkInterfaces(dpdkDevices, instances.value, newInstance.value)) {
        $('#ifcOverused').modal();
        return;
    }

    if (newInstance.value.raw.ifcName.trim() !== '' || newInstance.value.dpdk.device.trim() !== '' || newInstance.value.pcap_live.ifc.trim() !== '') {
        instances.value.push(structuredClone(toRaw(newInstance.value)));
        nextLinkID += 1;
        newInstance.value = createNewInstance();
        document.getElementById('ipfixprobe-instance-form').classList.remove('was-validated');
    }
    event.cancelBubble = true;
};

const deleteInstance = (index) => {
    instances.value.splice(index, 1);
};

onMounted(async () => {
    document.getElementById("linkID").focus();
});

const onFormSubmit = () => {
    props.store.config.probeList[props.store.probeIndex].ipfixprobeInstances = instances.value;
    props.store.config.probeList[props.store.probeIndex].hugepages = hugepages.value;
    props.store.config.nextLinkID = nextLinkID;
    emit('submit', EMIT_TYPE.SET_IPFIXPROBE_SETTINGS, props.store);
}
</script>

<template>
    <h1 class="component-title">Configure ipfixprobe for <samp>{{ probeInfo.host }}</samp></h1>
    <h5>Global Machine Setup</h5>

    <div id="accordionGlobal" class="mb-3 mt-3">
        <div class="card">
            <div class="card-header" id="headingTwo">
                <h5 class="mb-0">
                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false"
                        aria-controls="collapseTwo">
                        Advanced setup
                    </button>
                </h5>
            </div>

            <div id="collapseTwo" class="collapse collapsed" aria-labelledby="headingTwo"
                data-parent="#accordionGlobal">
                <div class="card-body">
                    <div class="row mb-2">
                        <div class="col">
                            <div class="input-group">
                                <span class="input-group-text col-2" for="hugepages">Hugepages Size</span>
                                <input class="form-control" type="number" id="hugepages" v-model="hugepages" min="1"
                                    required />
                                <InfoTooltip tooltipKey="hugepages" />
                                <div class="invalid-feedback">
                                    Hugepages size must have at least 1 GB allocated!
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <form @submit.prevent @keyup.enter="addInstance" id="ipfixprobe-instance-form">
        <h5>General Setup</h5>
        <div class="row mb-2">
            <div class="col">
                <div class="input-group">
                    <span class="input-group-text col-3" for="collector">Target Collector</span>
                    <input class="form-control" type="text" id="collector" disabled :value="targetCollector" required />
                </div>
            </div>

            <div class="col">
                <div class="input-group">
                    <span class="input-group-text col-3" for="linkID">Link ID</span>
                    <input class="form-control" type="number" id="linkID" v-model="newInstance.linkID" required min="1"
                        max="4294967295" />
                    <InfoTooltip tooltipKey="linkID" />
                    <div class="invalid-feedback">
                        Port must be uint32 (values 1-4294967295)!
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-2">
            <div class="col">
                <div class="input-group">
                    <span class="input-group-text col-3" for="inputType">Input Type</span>
                    <select class="form-select" id="inputType" v-model="newInstance.inputType" required>
                        <option value="RAW" :selected="newInstance.inputType == 'RAW'">Raw</option>
                        <option value="DPDK" :selected="newInstance.inputType == 'DPDK'">DPDK</option>
                        <option value="PCAP_LIVE" :selected="newInstance.inputType == 'PCAP_LIVE'">PCAP
                        </option>
                    </select>
                    <InfoTooltip tooltipKey="ipfixprobeInputType" />
                    <div class="invalid-feedback">
                        Input type must be Raw, DPDK, or PCAP!
                    </div>
                </div>
            </div>

            <div class="col">
                <div class="input-group" v-if="newInstance.inputType == 'RAW'">
                    <span class="input-group-text col-3" for="rawIfcName">Interface name</span>
                    <select class="form-select rounded-end" v-model="newInstance.raw.ifcName" required>
                        <option v-for="dev, index in rawDevices" :key="`raw_${dev.name}`" :value="dev.name"
                            :class="index == 0 ? 'selected' : ''">
                            {{ dev.name }}
                        </option>
                    </select>
                    <div class="invalid-feedback">
                        Target network device must be selected!
                    </div>
                </div>
                <div class="input-group" v-if="newInstance.inputType == 'DPDK'">
                    <span class="input-group-text col-3" for="dpdkDevice">Device</span>
                    <select class="form-select rounded-end" v-model="newInstance.dpdk.device" required>
                        <option v-for="dev, index in dpdkDevices" :key="`dpdk_${dev.name}`" :value="dev.device"
                            :class="index == 0 ? 'selected' : ''">
                            {{ dev.name }}
                        </option>
                    </select>
                    <div class="invalid-feedback">
                        Target DPDK device must be selected!
                    </div>
                </div>
                <div class="input-group" v-if="newInstance.inputType == 'PCAP_LIVE'">
                    <span class="input-group-text col-3" for="pcapSource">Interface name</span>
                    <select class="form-select rounded-end" v-model="newInstance.pcap_live.ifc" required>
                        <option v-for="dev, index in rawDevices" :key="`pcap_${dev.name}`" :value="dev.name"
                            :class="index == 0 ? 'selected' : ''">
                            {{ dev.name }}
                        </option>
                    </select>
                    <div class="invalid-feedback">
                        Target network device must be selected!
                    </div>
                </div>
            </div>
        </div>

        <div id="accordion" class="mb-3 mt-3">
            <div class="card">
                <div class="card-header" id="headingOne">
                    <h5 class="mb-0">
                        <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne"
                            aria-expanded="false" aria-controls="collapseOne">
                            Advanced setup
                        </button>
                    </h5>
                </div>

                <div id="collapseOne" class="collapse collapsed" aria-labelledby="headingOne" data-parent="#accordion">
                    <div class="card-body">
                        <div class="row mb-2">
                            <h5>General settings</h5>
                        </div>

                        <div class="row mb-2">
                            <div class="col">
                                <div class="input-group">
                                    <span class="input-group-text" for="cacheSize">Cache size</span>
                                    <input class="form-control" type="number" id="cacheSize"
                                        v-model="newInstance.cacheSize" min="1" required />
                                    <InfoTooltip tooltipKey="cacheSize" />
                                    <div class="invalid-feedback">
                                        Cache size exponent must be higher than 0!
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <div class="input-group">
                                    <span class="input-group-text" for="activeTimeout">Active timeout</span>
                                    <input class="form-control" type="number" id="activeTimeout"
                                        v-model="newInstance.activeTimeout" min="1" required />
                                    <InfoTooltip tooltipKey="activeTimeout" />
                                    <div class="invalid-feedback">
                                        Active timeout must be bihighergger than 0!
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <div class="input-group">
                                    <span class="input-group-text" for="passiveTimeout">Passive
                                        timeout</span>
                                    <input class="form-control" type="number" id="passiveTimeout"
                                        v-model="newInstance.passiveTimeout" min="1" required />
                                    <InfoTooltip tooltipKey="passiveTimeout" />
                                    <div class="invalid-feedback">
                                        Passive timeout must be higher than 0!
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div v-if="newInstance.inputType == 'RAW'">
                            <h5>Raw interface settings</h5>
                            <div class="row mb-3">
                                <div class="col input-group">
                                    <span class="input-group-text col-3" for="rawBlocks">Blocks</span>
                                    <input class="form-control" type="number" id="rawBlocks"
                                        v-model="newInstance.raw.blocks" min="1" required />
                                    <InfoTooltip tooltipKey="rawBlocks" />
                                    <div class="invalid-feedback">
                                        Value must be higher than 0!
                                    </div>
                                </div>

                                <div class="col input-group">
                                    <span class="input-group-text col-3" for="rawPackets">Packets</span>
                                    <input class="form-control" type="number" id="rawPackets"
                                        v-model="newInstance.raw.packets" min="1" required />
                                    <InfoTooltip tooltipKey="rawPackets" />
                                    <div class="invalid-feedback">
                                        Value must be higher than 0!
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="mb-3" v-else-if="newInstance.inputType == 'DPDK'">
                            <h5>DPDK interface settings</h5>

                            <div class="row mb-1">
                                <div class="col">
                                    <div class="input-group">
                                        <span class="input-group-text col-3" for="dpdkRXQueues">RX
                                            Queues</span>
                                        <input class="form-control" type="number" id="dpdkRXQueues"
                                            v-model="newInstance.dpdk.rxQueues" min="1" required />
                                        <InfoTooltip tooltipKey="dpdkRxQueues" />
                                        <div class="invalid-feedback">
                                            Value must be higher than 0!
                                        </div>
                                    </div>
                                </div>

                                <div class="col">
                                    <div class="input-group">
                                        <span class="input-group-text col-3" for="dpdkBurstSize">Burst
                                            Size</span>
                                        <input class="form-control" type="number" id="dpdkBurstSize"
                                            v-model="newInstance.dpdk.burstSize" min="1" required />
                                        <InfoTooltip tooltipKey="dpdkBurstSize" />
                                        <div class="invalid-feedback">
                                            Value must be higher than 0!
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="row mb-1">
                                <div class="col">
                                    <div class="input-group">
                                        <span class="input-group-text col-3" for="dpdkMempoolSize">Mempool
                                            Size</span>
                                        <input class="form-control" type="number" id="dpdkMempoolSize"
                                            v-model="newInstance.dpdk.mempoolSize" min="1" required />
                                        <InfoTooltip tooltipKey="dpdkMempoolSize" />
                                        <div class="invalid-feedback">
                                            Value must be higher than 0!
                                        </div>
                                    </div>
                                </div>

                                <div class="col">
                                    <div class="input-group">
                                        <span class="input-group-text col-3" for="dpdkOpts">EAL
                                            Options</span>
                                        <input class="form-control" type="text" id="dpdkOpts"
                                            v-model="newInstance.dpdk.ealOpts" />
                                        <InfoTooltip tooltipKey="dpdkEalOpts" />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <h5>Process plugins</h5>
                        <div class="row mb-2">
                            <div class="container">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th class="text-light bg-secondary" scope="col">Plugin</th>
                                            <th class="text-light bg-secondary" scope="col">Setting</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="plugin in newInstance.plugins" :key="plugin">
                                            <td class="col"><samp>{{ plugin.name }}</samp></td>
                                            <td class="col">
                                                <div class="btn-group" role="group">
                                                    <input class="btn-check" type="radio"
                                                        :id="`plg_${plugin.name}_enabled`" value="enabled"
                                                        v-model="plugin.enabled"
                                                        :disabled="plugin.disableAllowed == false" />
                                                    <label class="btn btn-outline-success"
                                                        :for="`plg_${plugin.name}_enabled`">Enabled</label>

                                                    <input class="btn-check" type="radio"
                                                        :id="`plg_${plugin.name}_disabled`" value="disabled"
                                                        v-model="plugin.enabled"
                                                        :disabled="plugin.disableAllowed == false" />
                                                    <label class="btn btn-outline-danger"
                                                        :for="`plg_${plugin.name}_disabled`">Disabled</label>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-3">
            <div class="col">
                <button class="btn btn-info w-100" type="button" @click="addInstance">Add instance</button>
            </div>
        </div>

        <h5>Configured ipfixprobe instances</h5>
        <div class="mb-3">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th class="text-light bg-secondary" scope="col">Monitored interface</th>
                        <th class="text-light bg-secondary" scope="col">Type</th>
                        <th class="text-light bg-secondary" scope="col">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="instance, index in instances" :key="instance">
                        <td v-if="instance.inputType == 'RAW'" class="col">{{ instance.raw.ifcName }}</td>
                        <td v-else-if="instance.inputType == 'DPDK'" class="col">{{ instance.dpdk.device }}
                        </td>
                        <td v-else class="col">{{ instance.pcap_live.ifc }}</td>
                        <td class="col">{{ instance.inputType }}</td>
                        <td class="col"><a class="link-danger" @click="deleteInstance(index)">Delete</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="row">
            <div class="col">
                <button class="btn btn-primary w-100" type="button" @click="$emit('back', props.store)">Back</button>
            </div>
            <div class="col">
                <button type="button" class="btn btn-success w-100" @click="onFormSubmit">Next</button>
            </div>
        </div>
    </form>

    <div class="modal fade" id="ifcOverused" tabindex="-1" role="dialog" aria-labelledby="ifcOverused"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="ifcOverused">Inteface type mismatch!</h5>
                    <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>New ipfixprobe instance cannot be added!</p>
                    <p>
                        The selected network interface is <strong>already used</strong> in another
                        ipfixprobe instance
                        with different type! Network interface cannot be used through <strong>both</strong>
                        Raw and
                        DPDK input types simultaneously!
                    </p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.make-select-inline {
    width: auto;
    display: inline-block;
}

.font-size-12em {
    margin-top: 4px;
}

.text-align-right {
    text-align: right;
}

.top-margin {
    margin-top: 12px;
}
</style>
