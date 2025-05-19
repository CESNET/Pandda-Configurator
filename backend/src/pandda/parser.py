def cfgForTypeRaw(insConf, instance):
    insConf['raw'] = dict()
    insConf['raw']['interface'] = instance['raw']['ifcName']
    insConf['raw']['blocks_count'] = instance['raw']['blocks']
    insConf['raw']['packets_in_block'] = instance['raw']['packets']


def cfgForTypeDPDK(insConf, instance):
    insConf['dpdk'] = dict()
    insConf['dpdk']['allowed_nics'] = instance['dpdk']['device']
    insConf['dpdk']['rx_queues'] = instance['dpdk']['rxQueues']
    insConf['dpdk']['burst_size'] = instance['dpdk']['burstSize']
    insConf['dpdk']['mempool_size'] = instance['dpdk']['mempoolSize']
    insConf['dpdk']['eal_opts'] = instance['dpdk']['ealOpts']


def cfgForTypePcap(insConf, instance):
    insConf['pcap_live'] = dict()
    insConf['pcap_live']['interface'] = instance['pcap_live']['ifc']


def cfgForProbe(central, server):
    config = dict()
    config['hugepages'] = server['hugepages']
    config['ipfixprobe_instances'] = []
    for instance in server['ipfixprobeInstances']:
        insConf = dict()
        insConf['host'] = server['host']
        insConf['type'] = instance['inputType'].lower()
        if insConf['type'] == 'raw':
            cfgForTypeRaw(insConf, instance)
        elif insConf['type'] == 'dpdk':
            cfgForTypeDPDK(insConf, instance)
        elif insConf['type'] == 'pcap_live':
            cfgForTypePcap(insConf, instance)
        insConf['cacheSize'] = instance['cacheSize']
        insConf['activeTimeout'] = instance['activeTimeout']
        insConf['passiveTimeout'] = instance['passiveTimeout']
        insConf['plugins'] = dict()
        for plg in instance['plugins']:
            if plg['enabled'] == 'enabled':
                insConf['plugins'][plg['name']] = {}
        insConf['colHost'] = central['collector']['host']
        insConf['colPort'] = central['collector']['port']
        insConf['linkID'] = instance['linkID']
        insConf['protocol'] = 'udp' if instance['useTCP'] == 'UDP' else 'tcp'
        config['ipfixprobe_instances'].append(insConf)
    return config


def cfgForCollector(central):
    config = dict()
    config['host'] = central['collector']['host']
    config['port'] = int(central['collector']['port'])
    config['proto'] = central['collector']['proto']
    config['forward_targets'] = []
    for fwdTarget in central['collector']['forwardingTargets']:
        config['forward_targets'].append({
            "host": fwdTarget['host'],
            "port": fwdTarget['port'],
            "proto": fwdTarget['proto'],
        })
    config['adict'] = {
        'enabled': central['collector']['adict'],
        'data_folder': '',
        'protected_ranges': [],
        'users': []
    }
    if central['adict'] is not None:
        config['adict']['data_folder'] = central['adict']['dataFolder']
        config['adict']['protected_ranges'] = [prefix for prefix in central['adict']['protectedPrefixes'].split('\n') if prefix.strip()]
    return config


def read_cfg_from_UI(config):
    ipConfigs = dict()
    for server in config['probeList']:
        ipConfigs[f'{server["host"]}'] = {
            'probe': cfgForProbe(config, server)
        }

    if config['collector']['host'] not in ipConfigs:
        ipConfigs[config['collector']['host']] = {}
    ipConfigs[config['collector']['host']]['collector'] = cfgForCollector(config)

    return ipConfigs
