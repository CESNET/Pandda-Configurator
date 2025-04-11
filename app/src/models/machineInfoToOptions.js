export const machineInfoToRaw = (machineInfo) => {
    let rawDevices = new Array();
    for (let idx = 0; idx < machineInfo.net_interfaces.length; ++idx) {
        rawDevices.push({
            name: machineInfo.net_interfaces[idx]
        });
    }

    return rawDevices;
};

export const machineInfoToDPDK = (machineInfo) => {
    let dpdkDevices = new Array();
    for (let idx = 0; idx < machineInfo.dpdk_devices.length; ++idx) {
        dpdkDevices.push({
            device: machineInfo.dpdk_devices[idx].device,
            ifc: machineInfo.dpdk_devices[idx].ifc,
            name: `${machineInfo.dpdk_devices[idx].device} (${machineInfo.dpdk_devices[idx].drv})`,
        });
    }

    return dpdkDevices;
};
