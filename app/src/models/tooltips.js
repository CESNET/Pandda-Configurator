export default {
    'masterPassword': 'Master password for encrypting sensitive configuration data.',
    'collectorHost': 'Hostname or IP address of the Collector server.',
    'collectorPort': 'Port number for receiving flow data.',
    'collectorProtocol': 'Transport protocol used for collection (TCP or UDP).',
    'credentialsType': 'Select default or custom credentials for authentication.',
    'fwdHost': 'Hostname or IP address to forward flow data to.',
    'fwdPort': 'Destination port for forwarded flow data.',
    'adictDataFolder': 'Directory path for storing ADiCT database files. If possible, use large data disc.',
    'probeHost': 'Hostname or IP address of the new probe server.',
    'ipfixprobeInputType': 'Input device type for ipfixprobe (e.g., NIC, file).',
    'linkID': 'Unique identifier in form of number for the monitored network link.',
    'cacheSize': 'Exponent value "n" defining ipfixprobe cache size in form of 2^n.',
    'hugepages': 'Number of GBs allocated for DPDK hugepages, only used when ipfixprobe with DPDK input is defined.',
    'activeTimeout': 'Timeout (in seconds) for active flow expiration in seconds.',
    'passiveTimeout': 'Timeout (in seconds) for inactive flow expiration in seconds.',
    'rawBlocks': 'Number of memory blocks allocated for raw packet capture.',
    'rawPackets': 'Number of packets to read per capture operation.',
    'dpdkRxQueues': 'Number of receive (RX) queues configured for the device.',
    'dpdkBurstSize': 'Number of packets processed per burst.',
    'dpdkMempoolSize': 'Size of the memory pool for packet buffers.',
    'dpdkEalOpts': 'Additional EAL (Environment Abstraction Layer) options for DPDK.',
};
