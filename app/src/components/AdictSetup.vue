<script setup>
import { ref, defineEmits, defineProps, onMounted } from 'vue';
import { registerValidator, errorMessageForId, validatePath, validateProtectedRanges } from '@/models/formValidators';
import { EMIT_TYPE } from '@/models/emits';
import InfoTooltip from '@/components/InfoTooltip.vue';

import showImg from "@/assets/images/show.png";
import hideImg from "@/assets/images/hide.png";

const props = defineProps({
    store: {
        type: Object
    }
});

const emit = defineEmits([
    'submit',
    'back'
]);

const adictSettings = ref(props.store.config.adict);

const imgPath = ref(showImg);
const showPassword = ref(false);

const cancelEvent = (event) => {
    event.cancelBubble = true;
    event.preventDefault();
    return false;
}

const toggleShow = () => {
    showPassword.value = !showPassword.value;
    imgPath.value = showPassword.value ? hideImg : showImg;
};

const validate = () => {
    var form = document.getElementById('adict-setup-form');
    form.classList.add('was-validated');
    return form.checkValidity();
};

const onFormSubmit = () => {
    if (!validate()) {
        return;
    }

    props.store.config.adict = adictSettings.value;
    emit('submit', EMIT_TYPE.SET_ADICT_SETTINGS, props.store);
}

onMounted(async () => {
    registerValidator('dataFolder', () => {
        validatePath('dataFolder');
    });
    registerValidator('protectedPrefixes', () => {
        validateProtectedRanges('protectedPrefixes');
    });

    document.getElementById("protectedPrefixes").focus();
});
</script>

<template>
    <h1 class="component-title">ADiCT Setup</h1>
    <div class="container">
        <form id="adict-setup-form" @submit.prevent @keyup.enter="onFormSubmit" class="needs-validation" novalidate>
            <h5>Storage Settings</h5>

            <div class="row mb-2">
                <div class="input-group">
                    <label class="input-group-text col-2" for="dataFolder">Data Folder</label>
                    <input class="form-control" id="dataFolder" type="text" v-model="adictSettings.dataFolder"
                        required />
                    <InfoTooltip tooltipKey="adictDataFolder" />
                    <div class="invalid-feedback">
                        {{ errorMessageForId('dataFolder') }}
                    </div>
                </div>
            </div>

            <h5 class="mb-1 mt-3">ADiCT User Credentials</h5>
            <div class="row mb-2">
                <div class="input-group">
                    <label class="input-group-text col-2" for="username">Username</label>
                    <input class="form-control rounded-end" id="username" type="text" v-model="adictSettings.user.name"
                        required />
                    <div class="invalid-feedback">
                        Admin username cannot be empty!
                    </div>
                </div>
            </div>

            <div class="row mb-2">
                <div class="input-group">
                    <label class="input-group-text col-2" for="newUserPass">Password</label>
                    <input :type="showPassword ? 'text' : 'password'" class="form-control" id="newUserPass"
                        v-model="adictSettings.user.pass" required />
                    <button class="btn btn-light border rounded-end" type="button" @click="toggleShow"><img
                            class="passwd-icon-size" :src="imgPath" alt="Submit"></button>
                    <div class="invalid-feedback">
                        Admin password cannot be empty!
                    </div>
                </div>
            </div>

            <div class="row mb-1 mt-3">
                <h5>ADiCT Monitored IP Ranges</h5>
                <p>
                    Here you can customize monitored IP prefixes: ranges of IP addresses for which data will be
                    collected.
                    <br />
                    There must be one IP address or one IP range in CIDR format on each line.
                </p>
            </div>

            <div class="row mb-3" @keyup.enter="cancelEvent">
                <div class="input-group">
                    <textarea class="form-control rounded-end" id="protectedPrefixes"
                        v-model="adictSettings.protectedPrefixes" placeholder="Monitored IP prefixes..."
                        required></textarea>
                    <div class="invalid-feedback">
                        {{ errorMessageForId('protectedPrefixes') }}
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col">
                    <button class="btn btn-primary w-100" type="button"
                        @click="$emit('back', props.store)">Back</button>
                </div>
                <div class="col">
                    <button class="btn btn-success w-100" type="button" @click="onFormSubmit">Next</button>
                </div>
            </div>
        </form>
    </div>
</template>

<style scoped>
.passwd-icon-size {
    width: 100%;
    max-width: 20px;
}
</style>
