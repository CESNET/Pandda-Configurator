<script setup>
import { ref } from 'vue';
import { STATE } from '@/models/state.js';
import { MENU_GROUP, MENU_GROUP_ITEMS } from '@/models/menuGroups.js'
import { filterCustomCredsOnly } from '@/models/utils';

import logo from "@/assets/images/pandda_cesnet_logo.png";

const props = defineProps({
    store: {
        type: Object,
        required: true
    }
});

const menuGroups = Object.values(MENU_GROUP);
const l1Elements = ref(new Array());
const l2Elements = ref(new Array());
const l1index = ref(0);
const l2index = ref(0);

const findActiveL1Item = (currentState) => {
    if (currentState === null) {
        return MENU_GROUP_ITEMS[0];
    }
    return MENU_GROUP_ITEMS.find(element => element.state == currentState);
};

const prepareMenu = (currentState, config, itemIndex) => {
    const activeL1Item = findActiveL1Item(currentState);
    l1index.value = Object.values(MENU_GROUP).findIndex(element => element === activeL1Item.parent);

    l1Elements.value = menuGroups.map((element, index) => {
        let classes = 'btn w-100';
        classes += index <= l1index.value ? ' btn-secondary' : ' btn-outline-secondary';
        classes += element == activeL1Item.parent ? ' bold-text' : '';
        return {
            itemText: element,
            class: classes
        };
    });

    const l2Items = MENU_GROUP_ITEMS.filter(element => element.parent == activeL1Item.parent);
    l2index.value = l2Items.findIndex(e => e.state === currentState);
    l2Elements.value = l2Items.map((element, index) => {
        let classes = 'btn w-100';
        classes += index <= l2index.value ? ' btn-secondary' : ' btn-outline-secondary';
        classes += element.state == currentState ? ' bold-text' : '';

        if (element.state == currentState && element.state == STATE.CUSTOM_PROBE_CREDENTIALS) {
            const customCredsOnly = filterCustomCredsOnly(config.probeList);
            const index = customCredsOnly.findIndex(e => e.host === config.probeList[itemIndex].host);

            console.log('cconly', customCredsOnly, index);

            return {
                itemText: element.itemText(index, customCredsOnly.length),
                class: classes
            };
        } else if (element.state == currentState && element.state == STATE.IPFIXPROBE_INPUT_SETUP) {
            return {
                itemText: element.itemText(itemIndex, config.probeList.length),
                class: classes
            };
        } else {
            return {
                itemText: element.itemText(),
                class: classes
            };
        }
    });
};

prepareMenu(props.store.state, props.store.config, props.store.probeIndex);
</script>

<template>
    <div class="padding-top-20px">
        <div class="text-center">
            <img class="mb-3 img-max" :src="logo" alt="PANDDA logo">

            <div class="row">
                <div class="btn-group w-100" role="group">
                    <button v-for="item in l1Elements" :key="item" type="button" :class="item.class" disabled>
                        {{ item.itemText }}
                    </button>
                </div>
            </div>

            <hr class="delimiter-line border-top border-2 bg-light" />

            <div class="row">
                <div class="btn-group w-100" role="group">
                    <button v-for="item in l2Elements" :key="item" type="button" :class="item.class" disabled>
                        {{ item.itemText }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.img-max {
    max-width: 256px;
}

.arrow {
    max-width: 16px;
}

.padding-top-20px {
    padding-top: 20px;
}

.bold-text {
    font-weight: bold;
}

.btn:disabled {
    opacity: unset;
}
</style>
