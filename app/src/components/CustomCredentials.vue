<script setup>
import { ref, defineProps, defineEmits, onMounted } from 'vue';
import InfoTooltip from '@/components/InfoTooltip.vue';
import { EMIT_TYPE } from '@/models/emits';
import { getSSHKey } from '@/models/requests/getSSHKey';

import showImg from "@/assets/images/show.png";
import hideImg from "@/assets/images/hide.png";

const emit = defineEmits([
    'submit',
    'back'
]);

const props = defineProps({
    store: {
        type: Object
    },
    isCollector: {
        type: Boolean,
        default: false
    }
});

const imgPath = ref(showImg);
const showPassword = ref(false);

const config = props.store.config;
const sshPubKey = ref('');
const sshLoginInfo = ref(
    props.isCollector ? config.collector.customCredentials : config.probeList[props.store.probeIndex].customCredentials
);

const host = props.isCollector ? config.collector.host : config.probeList[props.store.probeIndex].host;
const formTitle = props.isCollector ? 'Custom Credentials for Collector' : `Custom Credentials for ${host}`;

const getRSAKey = async () => {
    const response = await getSSHKey();
    if (sshPubKey !== false) {
        sshPubKey.value = response;
    }
};

const toggleShow = () => {
    showPassword.value = !showPassword.value;
    imgPath.value = showPassword.value ? hideImg : showImg;
};

const validate = () => {
    var form = document.getElementById('custom-creds-form');
    form.classList.add('was-validated');
    return form.checkValidity();
};

onMounted(async () => {
    getRSAKey();
    document.getElementById("sshUser").focus();
});

const onFormSubmit = () => {
    if (!validate()) {
        return;
    }

    if (props.isCollector) {
        props.store.config.collector.customCredentials = sshLoginInfo.value;
    } else {
        props.store.config.probeList[props.store.probeIndex].customCredentials = sshLoginInfo.value;
    }

    emit('submit', EMIT_TYPE.SET_CREDENTIALS, props.store, props.isCollector);
};
</script>

<template>
    <h1 class="component-title">{{ formTitle }}</h1>
    <form @submit.prevent @keyup.enter="onFormSubmit()" id="custom-creds-form">
        <div class="mb-2 input-group">
            <span class="input-group-text col-2" for="sshUser">SSH Username</span>
            <input class="form-control rounded-end" type="text" id="sshUser" v-model="sshLoginInfo.user" required />
            <div class="invalid-feedback">
                SSH username cannot be empty!
            </div>
        </div>

        <div class="mb-2 input-group">
            <span class="input-group-text col-2" for="sshLoginType">SSH Login Type</span>
            <select class="form-select rounded-end" id="sshLoginType" v-model="sshLoginInfo.type" required>
                <option value="sshLoginTypeKey">Key</option>
                <option value="sshLoginTypePasswd">Password</option>
            </select>
            <InfoTooltip tooltipKey="credentialsType" />
            <div class="invalid-feedback">
                Login type must be specified!
            </div>
        </div>

        <div class="mb-2 input-group" v-if="sshLoginInfo.type == 'sshLoginTypePasswd'">
            <label class="input-group-text col-2" for="sshPass">SSH Password</label>

            <input :type="showPassword ? 'text' : 'password'" class="form-control" id="sshPass"
                v-model="sshLoginInfo.pass" required />
            <button class="btn btn-light border rounded-end" type="button" @click="toggleShow"><img
                    class="passwd-icon-size" :src="imgPath" alt="Submit"></button>
            <div class="invalid-feedback">
                SSH password cannot be empty!
            </div>
        </div>
        <div class="mb-3 mt-3" v-else-if="sshLoginInfo.type == 'sshLoginTypeKey'">
            <h5>SSH Public Key</h5>
            <div class="alert alert-secondary ssh-key" role="alert">
                <samp>{{ sshPubKey }}</samp>
            </div>
        </div>
        <div class="mb-3" v-else>
            <p>Incorrent SSH login type selected!</p>
        </div>

        <div class="row">
            <div class="col">
                <button class="btn btn-primary w-100" type="button" @click="$emit('back', props.store)">Back</button>
            </div>
            <div class="col">
                <button class="btn btn-success w-100" type="button" @click="onFormSubmit()">Next</button>
            </div>
        </div>
    </form>
</template>

<style scoped>
.passwd-icon-size {
    width: 100%;
    max-width: 24px;
}

.ssh-key {
    word-break: break-all;
}
</style>
