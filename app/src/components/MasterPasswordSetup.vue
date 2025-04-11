<script setup>
import { defineProps, ref, defineEmits, onMounted } from 'vue';
import { decryptJSON } from '@/models/aes';
import { createEmptyConfig } from '@/models/emptyConfig';
import { EMIT_TYPE } from '@/models/emits';
import { findExistingConfig } from '@/models/requests/findExistingConfig';
import { deleteSavedConfig } from '@/models/requests/deleteSavedConfig';
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
]);

const masterPassword = ref('');
const showPassword = ref(false);
const imgPath = ref(showImg);
const existingConfig = ref(null);

const toggleShow = () => {
    showPassword.value = !showPassword.value;
    imgPath.value = showPassword.value ? hideImg : showImg;
};

const validate = () => {
    var form = document.getElementById('main-passwd-form');
    form.classList.add('was-validated');
    return form.checkValidity();
};

const loadExistingConfig = async () => {
    if (!validate()) {
        return;
    }

    const foundConfig = await findExistingConfig();
    if (foundConfig.exists) {
        const decrypted = decryptJSON(foundConfig.encrypted, masterPassword.value);
        if (decrypted) {
            existingConfig.value = decrypted;
            $('#existingFoundModal').modal();
        } else {
            $('#wrongPasswordModal').modal();
        }
    } else {
        emitCurrentConfig();
    }
};

const emitCurrentConfig = () => {
    props.store.config.masterPassword = masterPassword.value;
    emit('submit', EMIT_TYPE.SET_MASTER_PASSWORD, props.store);
}

const onExistingFoundModalSubmit = (useExistingConfig) => {
    props.store.config = useExistingConfig ? existingConfig.value : createEmptyConfig();
    props.store.config.masterPassword = masterPassword.value;
    emit('submit', EMIT_TYPE.SET_MASTER_PASSWORD, props.store);
};

const onWrongPasswordModalSubmit = async (deleteAndContinue) => {
    if (deleteAndContinue) {
        await deleteSavedConfig();
        props.store.config = createEmptyConfig();
        props.store.config.masterPassword = masterPassword.value;
        emit('submit', EMIT_TYPE.SET_MASTER_PASSWORD, props.store);
    }
};

onMounted(async () => {
    document.getElementById("password").focus();
});
</script>

<template>
    <h1 class="component-title">Master Password</h1>
    <form id="main-passwd-form" @submit.prevent @keyup.enter.prevent="loadExistingConfig" class="needs-validation"
        novalidate>
        <div class="mb-3 input-group">
            <label class="input-group-text" for="password">Master Password</label>

            <input :type="showPassword ? 'text' : 'password'" class="form-control" id="password"
                v-model="masterPassword" required minlength="8" />
            <button class="btn btn-light border" type="button" @click="toggleShow">
                <img class="passwd-icon-size" :src="imgPath" alt="Submit" />
            </button>
            <InfoTooltip tooltipKey="masterPassword" />
            <div class="invalid-feedback">
                Main password must be at least 8 characters long!
            </div>
        </div>

        <div>
            <div class="col">
                <button class="btn btn-success w-100" type="button" @click="loadExistingConfig">
                    Next
                </button>
            </div>
        </div>
    </form>

    <div class="modal fade" id="existingFoundModal" tabindex="-1" role="dialog"
        aria-labelledby="existingFoundModalTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="existingFoundModalTitle">Existing configuration found!</h5>
                    <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Do you want to use existing configuration?</p>
                    <p class="text-danger fw-bold">Note: Existing configuration will be deleted if you choose to
                        start from the scratch!</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" data-dismiss="modal"
                        @click="onExistingFoundModalSubmit(true)">Use
                        existing</button>
                    <button type="button" class="btn btn-danger" data-dismiss="modal"
                        @click="onExistingFoundModalSubmit(false)">Start from
                        scratch</button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="wrongPasswordModal" tabindex="-1" role="dialog"
        aria-labelledby="wrongPasswordModalTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="wrongPasswordModalTitle">Wrong password!</h5>
                    <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>
                        Existing configuration was found on the system, but the password is wrong!
                        <br />
                        You can either enter a correct password or <label class="text-danger fw-bold">continue and
                            delete</label> the saved
                        configuration.
                    </p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" data-dismiss="modal"
                        @click="onWrongPasswordModalSubmit(false)">Try again</button>
                    <button type="button" class="btn btn-danger" data-dismiss="modal"
                        @click="onWrongPasswordModalSubmit(true)">Delete and continue</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.passwd-icon-size {
    width: 100%;
    max-width: 24px;
}
</style>
