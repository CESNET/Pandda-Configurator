<script setup>
import { ref } from 'vue';
import Navbar from '@/components/Navbar.vue';
import MasterPasswordSetup from '@/components/MasterPasswordSetup.vue';
import GlobalSSHSetup from '@/components/GlobalSSHSetup.vue';
import ProbesConnInfo from '@/components/ProbesConnInfo.vue';
import CustomCredentials from '@/components/CustomCredentials.vue';
import AutoDetection from '@/components/AutoDetection.vue';
import IpfixprobeSetup from '@/components/IpfixprobeSetup.vue';
import CollectorSetup from '@/components/CollectorSetup.vue';
import AdictSetup from '@/components/AdictSetup.vue';
import ConfigureMachines from '@/components/ConfigureMachines.vue';
import Footer from '@/components/Footer.vue';

import { STATE } from '@/models/state.js'
import { createEmptyStore } from '@/models/store.js';
import { handleOnBack } from '@/models/onBack';
import { handleOnSubmit } from '@/models/onSubmit';

const appStore = ref(createEmptyStore());

const handleEmitSubmit = (emitName, store, custom) => {
    appStore.value = handleOnSubmit(emitName, store, custom);
};

const handleEmitBack = (componentStore) => {
    appStore.value = handleOnBack(componentStore);
};
</script>

<template>
    <Navbar :key="[appStore]" :store="appStore" />

    <div class="content-box">
        <div v-if="appStore.state === STATE.MASTER_PASSWORD_SETUP">
            <MasterPasswordSetup :store="appStore" @submit="handleEmitSubmit" />
        </div>
        <div v-else-if="appStore.state === STATE.GLOBAL_SSH_INIT">
            <GlobalSSHSetup :store="appStore" @submit="handleEmitSubmit" @back="handleEmitBack" />
        </div>
        <div v-else-if="appStore.state === STATE.COLLECTOR_SETTINGS">
            <CollectorSetup :store="appStore" @submit="handleEmitSubmit" @back="handleEmitBack" />
        </div>
        <div v-else-if="appStore.state === STATE.CUSTOM_COL_CREDENTIALS">
            <CustomCredentials :store="appStore" :isCollector="true" @submit="handleEmitSubmit" @back="handleEmitBack">
            </CustomCredentials>
        </div>
        <div v-else-if="appStore.state === STATE.ADICT_SETTINGS">
            <AdictSetup :store="appStore" @submit="handleEmitSubmit" @back="handleEmitBack" />
        </div>
        <div v-else-if="appStore.state === STATE.PROBES_CONN_INFO">
            <ProbesConnInfo :store="appStore" @submit="handleEmitSubmit" @back="handleEmitBack" />
        </div>
        <div v-else-if="appStore.state === STATE.CUSTOM_PROBE_CREDENTIALS">
            <CustomCredentials :key="[appStore, appStore.probeIndex]" :store="appStore" :isCollector="false"
                @submit="handleEmitSubmit" @back="handleEmitBack">
            </CustomCredentials>
        </div>
        <div v-else-if="appStore.state === STATE.AUTO_DISCOVERY">
            <AutoDetection :store="appStore" @submit="handleEmitSubmit" @back="handleEmitBack">
            </AutoDetection>
        </div>
        <div v-else-if="appStore.state === STATE.IPFIXPROBE_INPUT_SETUP">
            <IpfixprobeSetup :key="[appStore, appStore.probeIndex]" :store="appStore" @submit="handleEmitSubmit"
                @back="handleEmitBack" />
        </div>
        <div v-else-if="appStore.state === STATE.NEXT">
            <ConfigureMachines :store="appStore" @back="handleEmitBack" />
        </div>
    </div>

    <Footer></Footer>
</template>
