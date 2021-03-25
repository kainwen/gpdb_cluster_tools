#!/usr/bin/env python3

import sys
import subprocess
from jinja2 import Template

SYSCTL_CONF ="""
# kernel.shmall = _PHYS_PAGES / 2 # See Shared Memory Pages
# kernel.shmall = 197951838
# kernel.shmmax = kernel.shmall * PAGE_SIZE 
# kernel.shmmax = 810810728448
kernel.shmall = {{ kernel.shmall }}
kernel.shmmax = {{ kernel.shmmax }}
kernel.shmmni = 4096
vm.overcommit_memory = 2 # See Segment Host Memory
vm.overcommit_ratio = 95 # See Segment Host Memory

net.ipv4.ip_local_port_range = 10000 65535 # See Port Settings
kernel.sem = 500 2048000 200 4096
kernel.sysrq = 1
kernel.core_uses_pid = 1
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.msgmni = 2048
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.conf.all.arp_filter = 1
net.core.netdev_max_backlog = 10000
net.core.rmem_max = 2097152
net.core.wmem_max = 2097152
vm.swappiness = 10
vm.zone_reclaim_mode = 0
vm.dirty_expire_centisecs = 500
vm.dirty_writeback_centisecs = 100
vm.dirty_background_ratio = 0 # See System Memory
vm.dirty_ratio = 0
vm.dirty_background_bytes = 1610612736
vm.dirty_bytes = 4294967296
vm.min_free_kbytes = {{ vm.min_free_kbytes }}
"""


class Kernel:

    def __init__(self):
        pass

    @property
    def shmall(self):
        return self.get_mem_page_conf("_PHYS_PAGES") // 2

    @property
    def shmmax(self):
        page_size = self.get_mem_page_conf("PAGE_SIZE")
        return self.shmall * page_size

    def get_mem_page_conf(self, control):
        cmd = ["getconf", control]
        return int(subprocess.check_output(cmd))

"""
awk 'BEGIN {OFMT = "%.0f";} /MemTotal/ {print "vm.min_free_kbytes =", $2 * .03;}'
               /proc/meminfo >> /etc/sysctl.conf 
"""
class Vm:

    def __init__(self):
        pass

    @property
    def min_free_kbytes(self):
        code = "BEGIN {OFMT = \"%.0f\";} /MemTotal/ {print \"\", $2 * .03;}"
        cmd = ["awk", code, "/proc/meminfo"]
        return int(subprocess.check_output(cmd).strip())

   
if __name__ == "__main__":
    template = Template(SYSCTL_CONF)
    with open("/etc/sysctl.conf", "w") as g:
        print(template.render(kernel=Kernel(), vm=Vm()), file=g)
    print(subprocess.check_output(["sysctl", "-p"]).decode("utf-8"))
