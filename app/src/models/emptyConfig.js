export const createEmptyConfig = () => {
    return {
        masterPassword: '',
        globalSSHLogin: {
            user: '',
            pass: '',
            type: 'sshLoginTypeKey'
        },
        probeList: [],
        nextLinkID: 1,
        defaultPlugins: [
            { name: 'basic', enabled: "enabled", disableAllowed: false },
            { name: 'basicplus', enabled: "disabled", disableAllowed: true },
            { name: 'bstats', enabled: "disabled", disableAllowed: true },
            { name: 'dns', enabled: "disabled", disableAllowed: true },
            { name: 'dnssd', enabled: "disabled", disableAllowed: true },
            { name: 'flow_hash', enabled: "disabled", disableAllowed: true },
            { name: 'http', enabled: "disabled", disableAllowed: true },
            { name: 'icmp', enabled: "disabled", disableAllowed: true },
            { name: 'idpcontent', enabled: "disabled", disableAllowed: true },
            { name: 'mpls', enabled: "disabled", disableAllowed: true },
            { name: 'mqtt', enabled: "disabled", disableAllowed: true },
            { name: 'netbios', enabled: "disabled", disableAllowed: true },
            { name: 'nettisa', enabled: "disabled", disableAllowed: true },
            { name: 'ntp', enabled: "disabled", disableAllowed: true },
            { name: 'ovpn', enabled: "disabled", disableAllowed: true },
            { name: 'passivedns', enabled: "disabled", disableAllowed: true },
            { name: 'phists', enabled: "disabled", disableAllowed: true },
            { name: 'pstats', enabled: "disabled", disableAllowed: true },
            { name: 'quic', enabled: "disabled", disableAllowed: true },
            { name: 'rtsp', enabled: "disabled", disableAllowed: true },
            { name: 'sip', enabled: "disabled", disableAllowed: true },
            { name: 'smtp', enabled: "disabled", disableAllowed: true },
            { name: 'SSADetector', enabled: "disabled", disableAllowed: true },
            { name: 'ssdp', enabled: "disabled", disableAllowed: true },
            { name: 'stats', enabled: "disabled", disableAllowed: true },
            { name: 'tls', enabled: "disabled", disableAllowed: true },
            { name: 'vlan', enabled: "disabled", disableAllowed: true },
            { name: 'wg', enabled: "disabled", disableAllowed: true }
        ],
        collector: {
            host: '',
            port: 4739,
            proto: "TCP",
            sshCredentials: "default",
            customCredentials: {
                user: '',
                pass: '',
                type: 'sshLoginTypeKey'
            },
            adict: 'true',
            forwardingTargets: [],
        },
        adict: {
            protectedPrefixes: '',
            user: {
                name: '',
                pass: ''
            },
            dataFolder: '/data'
        },
        machineInfo: {}
    }
};
