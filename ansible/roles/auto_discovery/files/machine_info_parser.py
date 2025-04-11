import json
import os
import re
import sys


# DPDK PATTERNS
PATTERN_DPDK_NO_DEVS = re.compile(r'^No .* devices')
PATTERN_DPDK_SECTION_NAME = re.compile(r'(Network|Baseband|Crypto|DMA|Eventdev|Mempool|Compress|Misc \(rawdev\)|Regex|ML) devices')
PATTERN_DPDK_IFC_NAME = re.compile(r'if=([a-zA-Z0-9]*) ')
PATTERN_DPDK_DRV_NAME = re.compile(r'drv=([a-zA-Z0-9_\-]*) ')

# LSCPU PATTERNS
PATTERN_CPU_COUNT = re.compile(r'^CPU\(s\):\s*([0-9]+)$')
PATTERN_CPU_LIST = re.compile(r'On-line CPU\(s\) list:\s*([0-9\-]+)$')
PATTERN_CPU_NUMA = re.compile(r'NUMA node\(s\):\s*([0-9]+$)')
PATTERN_CPU_NUMA_LIST = re.compile(r'NUMA node([0-9]?) CPU\(s\):\s*([0-9\-]+)$')

# MEMINFO PATTERNS
PATTERN_MEM_TOTAL = re.compile(r'^MemTotal:\s*([0-9]+) kB$')


def load_file_content(file):
    with open(file, 'rt') as src:
        lines = src.readlines()
    return lines


def read_key(input_data, pattern):
    result = pattern.search(input_data)
    return result.group(1) if result else ''


def read_net_interfaces(sys_class_net_output):
    return [e.strip() for e in sys_class_net_output if e.strip()]


def read_dpdk_devices(dpdk_output):
    devices = list()

    current_section = None
    for line in dpdk_output:
        section_match = PATTERN_DPDK_SECTION_NAME.match(line)
        if section_match:
            current_section = section_match.group(1)
            continue

        if current_section != 'Network' or PATTERN_DPDK_NO_DEVS.match(line):
            continue

        if line.strip() and '====' not in line:
            line = line.strip()
            device = line.split(' ')[0]
            name = line.split("'")[1]
            ifc_name = read_key(line, PATTERN_DPDK_IFC_NAME)
            drv_name = read_key(line, PATTERN_DPDK_DRV_NAME)
            devices.append({
                'device': device,
                'name': name,
                'ifc': ifc_name,
                'drv': drv_name
            })

    return devices


def match_cpu_key(input_data, pattern, group_idx=1):
    result = pattern.match(input_data)
    return result.group(group_idx) if result else None


def match_numa_list(input_data, pattern):
    result = pattern.match(input_data)
    return (result.group(1), result.group(2)) if result else None


def read_cpu_info(lscpu_output):
    cpu_info = dict()
    cpu_info['numa_list'] = list()

    for line in lscpu_output:
        cpu_count = match_cpu_key(line, PATTERN_CPU_COUNT)
        if cpu_count:
            cpu_info['cpu_count'] = cpu_count

        cpu_list = match_cpu_key(line, PATTERN_CPU_LIST)
        if cpu_list:
            cpu_info['online_cpus'] = cpu_list

        numa_count = match_cpu_key(line, PATTERN_CPU_NUMA)
        if numa_count:
            cpu_info['numa_count'] = numa_count

        numa_info = match_numa_list(line, PATTERN_CPU_NUMA_LIST)
        if numa_info:
            numa_idx = numa_info[0]
            numa_list = numa_info[1]
            cpu_info['numa_list'].append({
                'numa_idx': numa_idx,
                'numa_cpus': numa_list
            })

    return cpu_info


def read_meminfo(meminfo_output):
    mem_info = dict()

    for line in meminfo_output:
        result = PATTERN_MEM_TOTAL.match(line)
        if result:
            mem_info['memory_in_kB'] = result.group(1)

    return mem_info


if __name__ == '__main__':
    root = os.path.dirname(sys.argv[0])
    tar_root = f'{root}/pandda_machine_info'

    net_interfaces = read_net_interfaces(
        load_file_content(f'{tar_root}/sys_class_net.txt')
    )

    dpdk_devices = read_dpdk_devices(
        load_file_content(f'{tar_root}/dpdk_devbind_output.txt')
    )

    cpu_info = read_cpu_info(
        load_file_content(f'{tar_root}/lscpu_output.txt')
    )

    mem_info = read_meminfo(
        load_file_content(f'{tar_root}/meminfo_output.txt')
    )

    machine_info = dict()
    machine_info['net_interfaces'] = net_interfaces
    machine_info['dpdk_devices'] = dpdk_devices
    machine_info['cpu_info'] = cpu_info
    machine_info['mem_info'] = mem_info

    with open(f'{root}/extracted_machine_info.json', 'wt') as dst:
        dst.write(json.dumps(machine_info, indent=4))
