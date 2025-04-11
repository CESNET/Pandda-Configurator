#!/bin/bash

export LC_ALL=C

# Prepare directory
TARGET_DIR=/tmp/pandda_machine_info
mkdir -p $TARGET_DIR

# Output used working directory
echo $TARGET_DIR

# Run commands
dpdk-devbind.py -s > $TARGET_DIR/dpdk_devbind_output.txt
lspci | grep -Ei 'eth|network|ethernet|wireless|wifi' > $TARGET_DIR/lspci_output.txt
ls -1 /sys/class/net > $TARGET_DIR/sys_class_net.txt
lscpu > $TARGET_DIR/lscpu_output.txt
cat /proc/meminfo > $TARGET_DIR/meminfo_output.txt

# Tar
cd /tmp && tar czf machine_info.tar.gz pandda_machine_info

exit 0
