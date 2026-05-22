import subprocess as sp
DECODE = 'utf-8'

def query_gpu():
    print('='*80)
    print('GPU PROCESSES inside containers:')
    print('='*80)
    command = "nvidia-smi --query-gpu=memory.free --format=csv"
    memory_free_info = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:]
    memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
    gpus = [int(i) for i, x in enumerate(memory_free_info)]
    command = "nvidia-smi --query-gpu=memory.used --format=csv"
    memory_used_info = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:]
    memory_used_values = [int(x.split()[0]) for i, x in enumerate(memory_used_info)]

    command = "nvidia-smi --query-gpu=memory.total --format=csv"
    memory_total_info = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:]
    memory_total_values = [int(x.split()[0]) for i, x in enumerate(memory_total_info)]

    command = "nvidia-smi --query-gpu=temperature.gpu --format=csv"
    temperature_gpu_info = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:]
    temperature_gpu_values = [int(x.split()[0]) for i, x in enumerate(temperature_gpu_info)]

    command = "nvidia-smi --query-gpu=utilization.gpu --format=csv"
    utilization_gpu_info = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:]
    utilization_gpu_values = [int(x.split()[0]) for i, x in enumerate(utilization_gpu_info)]

    command = "nvidia-smi --query-gpu=utilization.memory --format=csv"
    utilization_memory_info = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:]
    utilization_memory_values = [int(x.split()[0]) for i, x in enumerate(utilization_memory_info)]

    pid_values = []
    for i, gpu in enumerate(gpus):
        command = "nvidia-smi --query-compute-apps=pid --id={0:} --format=csv".format(gpu)
        pid_info = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:]
        if len(pid_info)==0:
            pid = 0
        else:
            pid = int(pid_info[0])
        pid_values.append(pid)

    D = {}
    D['pid'] = pid_values
    D['memory_free']  = memory_free_values
    D['memory_used']  = memory_used_values
    D['memory_total'] = memory_total_values
    D['temperature_gpu']    = temperature_gpu_values
    D['utilization_gpu']    = utilization_gpu_values
    D['utilization_memory'] = utilization_memory_values
    ps_info = []
    RED    = "\033[31m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    BLUE   = "\033[34m"
    CYAN   = "\033[36m"
    ORANGE = "\033[38;2;255;165;0m"
    OFF    = "\033[0m"

    for i, gpu in enumerate(gpus):
        pid = pid_values[i]
        if pid ==0:
            S = GREEN + 'GPU#{0:01d} '.format(i) + OFF
            S = S + ': '+ RED+ 'MEM [{0:5d}/{1:5d}] {2:5d} MB '.format(memory_used_values[i], memory_free_values[i],memory_total_values[i]) + OFF+ ' | '
            S = S + YELLOW + 'GPU: {0:3d}% MEM: {1:3d}% TEMP {2:3d}C '.format(utilization_gpu_values[i], utilization_memory_values[i], temperature_gpu_values[i]) + OFF
            print(S)
            print('='*80)
        else:
            command = 'ps -p {0:} -o pid,pcpu,pmem,vsz=MEMORY -o user,group=GROUP -o comm=PROGRAM'.format(pid)
            ps_info_head = sp.check_output(command.split()).decode(DECODE).split('\n')[:][:][0]
            ps_info_str = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:][0]
            ps_info.append(ps_info_str)
            command_args_only = 'ps -p {0:} -o args=ARGS'.format(pid)
            ps_info_command_args_only = sp.check_output(command_args_only.split()).decode(DECODE).split('\n')[:-1][1:][0]
            S = GREEN + 'GPU#{0:01d} '.format(i) + OFF
            S = S + ': '+ RED+ 'MEM [{0:5d}/{1:5d}] {2:5d} MB '.format(memory_used_values[i], memory_free_values[i],memory_total_values[i]) + OFF+ ' | '
            S = S + YELLOW + 'GPU: {0:3d}% MEM: {1:3d}% TEMP {2:3d}C '.format(utilization_gpu_values[i], utilization_memory_values[i], temperature_gpu_values[i]) + OFF
            print(S)
            print(ORANGE + ps_info_head + OFF)
            print(ORANGE + ps_info_str + OFF)
            print(ORANGE + ps_info_command_args_only + OFF)
#            print('- '*40)
            # get container by pid
            command = 'cat /proc/{0:}/cgroup'.format(pid)
            container_id_str = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][1:]

            if len(container_id_str)>0:
                if container_id_str[-1] == '0::/system.slice/containerd.service':
                    container_id_str = container_id_str[-2].replace('1:name=systemd:/docker/','')
                else:
                    container_id_str = container_id_str[-1].replace('0::/docker/','')
                # inspect
                command = "docker inspect --format '{{.Name}}' " + container_id_str
#                docker inspect --format '{{.Name}}' a7f943010262b4071d851a0c00edc683be291129210e5ff643c05269d942fd71
                container_name_str = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][0]
                container_name_str = container_name_str.strip("\'")
                print(CYAN + container_id_str + OFF+ ' ' + container_name_str)  

                command = "docker logs --tail 1 " + container_id_str
#                docker inspect --format '{{.Name}}' a7f943010262b4071d851a0c00edc683be291129210e5ff643c05269d942fd71
                container_output_str = sp.check_output(command.split()).decode(DECODE).split('\n')[:-1][-1]
                container_output_str = container_output_str.strip("\'")
                print(YELLOW + container_output_str + OFF)   
                
                print('='*80)

    D['ps_info'] = ps_info
    return D


query_gpu()
