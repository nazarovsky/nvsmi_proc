🖥️ GPU Process Monitor for Docker Containers

This Python script leverages nvidia-smi to monitor GPU usage and identify processes running inside Docker containers. It provides detailed information about GPU memory usage, utilization, temperature, and associated container information.

📌 Overview

The script queries GPU metrics using nvidia-smi and displays:

* Memory usage (free, used, total)
* GPU and memory utilization percentages
* Temperature
* Running process details (PID, user, command)
* Container ID and name (if applicable)
* This is especially useful in multi-user or multi-container environments where you need to track GPU resource consumption and which container is using which GPU.

🧰 Requirements

* NVIDIA GPU with drivers installed
* nvidia-smi command-line tool
* Docker installed (to inspect containers)
* Python 3.x

📦 Installation

No special installation is required beyond having the tools listed above. Just save the script as nvsmi_proc.py and run it.

▶️ Usage

```
python3 nvsmi_proc.py
```

Example Output

```
user@machine:~$ python3 nvsmi_proc.py
================================================================================
GPU PROCESSES inside containers:
================================================================================
GPU#0 : MEM [23858/  388] 24564 MB | GPU:  74% MEM:  49% TEMP  82C
2179498 63514792 root   root     python          python train.py -c configs/config.yml --use-amp --seed=0
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
904a9cf55bdf9c7b619e87181c284c401421d35afabfb4a6a85f8e7f82c9f1b9 /user_container
================================================================================
```
