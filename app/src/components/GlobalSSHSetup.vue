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
    }
});

const sshLoginInfo = ref(props.store.config.globalSSHLogin);

const sshPubKey = ref('');

const imgPath = ref(showImg);
const showPassword = ref(false);

const validate = () => {
    var form = document.getElementById('global-ssh-form');
    form.classList.add('was-validated');
    return form.checkValidity();
};

const onGenerateNew = () => {
    $('#generateKeyModal').modal();
}

const getRSAKey = async (force) => {
    const response = await getSSHKey(force);
    if (sshPubKey !== false) {
        sshPubKey.value = response;
    }
};

const toggleShow = () => {
    showPassword.value = !showPassword.value;
    imgPath.value = showPassword.value ? hideImg : showImg;
};

onMounted(async () => {
    getRSAKey(false);
    document.getElementById("sshUser").focus();
});

const onModalSubmit = (generateNew) => {
    if (generateNew) {
        getRSAKey(true);
    }
};

const onSubmit = () => {
    if (!validate()) {
        return;
    }

    props.store.config.globalSSHLogin = sshLoginInfo;
    emit('submit', EMIT_TYPE.SET_SSH_LOGIN, props.store);
}
</script>

<template>
    <h1 class="component-title">SSH Credentials</h1>
    <form id="global-ssh-form" @submit.prevent class="needs-validation" novalidate @keyup.enter.prevent="onSubmit">
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
            <button class="btn btn-info w-100" type="button" @click="onGenerateNew()">Generate new SSH key pair</button>
        </div>
        <div class="mb-3" v-else>
            <p>Incorrent SSH login type selected!</p>
        </div>

        <div class="modal fade" id="generateKeyModal" tabindex="-1" role="dialog"
            aria-labelledby="generateKeyModalTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="existingFoundModalTitle">Generate new SSH keypair</h5>
                        <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p>Do you want to generate new SSH keypair?</p>
                        <p class="text-danger fw-bold">Note: Existing SSH keypair will be permanently overriden!</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-light" data-dismiss="modal"
                            @click="onModalSubmit(false)">Cancel</button>
                        <button type="button" class="btn btn-danger" data-dismiss="modal"
                            @click="onModalSubmit(true)">Generate</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col">
                <button class="btn btn-primary w-100" type="button" @click="$emit('back', props.store)">Back</button>
            </div>
            <div class="col">
                <button class="btn btn-success w-100" type="button" @click="onSubmit">Next</button>
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
