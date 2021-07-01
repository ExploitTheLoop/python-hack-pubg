#! /usr/bin/env python
import os
import sys
import re
#getting pids

def get_pid(pkg):
    try:
        pid_id = os.popen("sudo pidof {}".format(pkg))
    except:
        print("Give root permissions please")

    pid_decode = pid_id.read()
    if pid_decode is not None:
        pid = pid_decode.replace("\n", "")
        return pid



#finding mapping
def mappings(pid):
    try:
        map_file = open(f"/proc/{pid}/maps", "r")
    except:
        print("Maps not opened permissions denied")
        sys.exit()
    #names

    '''
    O->others:others -> --p, anon, system/framework, etc
    Jh->:rw-p, anon:dalvik-main space
    Xs->system: --xp, lib, .so, system
    J->Java: 
    ch -> c++heap: 
    ca -> c++ alloc: anon, key -> anon:libc_malloc, rw-p, rwxp
    cd -> c++ data:
    cb -> c++ bss:
    PS -> PPSSPP: 
    A -> Anonymous: just rw-p
    S -> Stack:
    As -> Ashmem:
    V -> Video:
    B -> Bad(dang):
    Xa -> code app:r-xp, lib, .so, .jar
    '''
    
    #order
    '''
                0               1           2           3       4           5           6
    ['76a01ae000-76a01af000', 'r--p', '00000000', '00:00', '26', '[anon:atexit', 'handler]']

    A -> 4[]
    '''
    details_all = {"address": [], "permissions": [], "allocated": []}
    details_ca = {"address": [], "permissions": [], "allocated": []}
    details_xa = {"address": [], "permissions": [], "allocated": []}
    details_a = {"address": [], "permissions": [], "allocated": []}
    for line in map_file.readlines():
        temp_details = line.split()
        region = temp_details[len(temp_details)-1]
        re_region = temp_details[len(temp_details)-2]
        perm = temp_details[1]

        details_all["address"].append(temp_details[0])
        details_all["permissions"].append(temp_details[1])
        details_all["allocated"].append(region)

        #ca anon, key -> anon:libc_malloc, rw-p, rwxp
        if ("anon" in region or "anon" in re_region) and ("r" in perm or "w" in perm) and ("libc_malloc" in region or "libc_malloc" in re_region):
            details_ca["address"].append(temp_details[0])
            details_ca["permissions"].append(temp_details[1])
            details_ca["allocated"].append(region)

        #A -> Anonymous: just rw-p
        elif ("0" in region or ":" in re_region) and ("r" in perm or "w" in perm):
            details_a["address"].append(temp_details[0])
            details_a["permissions"].append(temp_details[1])
            details_a["allocated"].append(region)


        #Xa -> code app:r-xp, lib, .so, .jar
        elif ("lib" in region or "lib" in re_region) and ("r" in perm or "w" in perm) and (".so" in region or ".so" in re_region) and ("system" in region or "system" in re_region):
            details_xa["address"].append(temp_details[0])
            details_xa["permissions"].append(temp_details[1])
            details_xa["allocated"].append(region)

        else:
            pass
    map_file.close()
    return details_ca, details_a, details_xa, details_all


#memory reading

def ReadProcessMemory(d_ca, d_a, d_xa, d_all, pid, value):

    try:
        mem_file = open(f"/proc/{pid}/mem", "rb", 0)
    except:
        print("Mem not opened permissions denied")
        sys.exit()

    da = d_xa["address"]
    da_search = []
    total_results_da = 0
    for addr in range(0, len(da)):
        partitions = da[addr].split("-")
        startAddr = int(partitions[0], 16)
        endAddr = int(partitions[1], 16)
        mem_file.seek(startAddr)
        read_addr = mem_file.read(endAddr - startAddr)
        search = bytes(value, "ASCII")
        #mem_file.seek(startAddr + number_offset)
        for search_number in re.finditer(search, read_addr):
            da_search.append(search_number.start())
    for results in da_search:
        total_results_da += len(da_search)
    print(f"Found {total_results_ca} in ca region")
    mem_file.close()


def WriteProcessMemory(d_ca, d_a, d_xa, d_all, pid, value, v_write):
    try:
        mem_file = open(f"/proc/{pid}/mem", "rb+", 0)
    except:
        print("Mem not opened permissions denied")
        sys.exit()

    da = d_xa["address"]
    added=0
    for addr in range(0, len(da)):
        da_search = []
        partitions = da[addr].split("-")
        startAddr = int(partitions[0], 16)
        endAddr = int(partitions[1], 16)
        mem_file.seek(startAddr)
        try:
            read_addr = mem_file.read(endAddr - startAddr)
            search = bytes(value, "ASCII")
            #mem_file.seek(startAddr + number_offset)
            for search_number in re.finditer(search, read_addr):
                da_search.append(search_number.start())

            for num in range(0,len(da_search)):
                mem_file.seek(startAddr + da_search[num])
                try:
                    mem_file.write(bytes(v_write, "ASCII"))
                    added+=1
                except:
                    print("I/O Error while writing memory")
                    continue
        except:
            pass
        
    print(f"{added} values added")



def writer(pkg, read, write):
    pid = get_pid(pkg)
    
    details_ca, details_a, details_xa, details_all = mappings(pid)


    WriteProcessMemory(details_ca, details_a, details_xa, details_all, pid, read, write)

