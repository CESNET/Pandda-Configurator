const deviceToIfc = (dpdkDevices, device) => {
    const info = dpdkDevices.find(e => e.device == device);
    return info !== null ? info.ifc : '';
};

export const checkInterfaces = (dpdkDevices, instances, newInstance) => {
    for (let idx = 0; idx < instances.length; ++idx) {
        if (instances[idx].inputType == 'PCAP') {
            continue;
        }

        if (instances[idx].inputType == 'RAW' && newInstance.inputType == 'DPDK') {
            const rawIfc = instances[idx].raw.ifcName;
            const dpdkIfc = deviceToIfc(dpdkDevices, newInstance.dpdk.device);
            if (rawIfc == dpdkIfc) {
                return false;
            }
        }

        if (instances[idx].inputType == 'DPDK' && newInstance.inputType == 'RAW') {
            const rawIfc = newInstance.raw.ifcName;
            const dpdkIfc = deviceToIfc(dpdkDevices, instances[idx].dpdk.device);
            if (rawIfc == dpdkIfc) {
                return false;
            }
        }
    }
    return true;
};
