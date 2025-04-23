import torch
import os
def hello():
	print("hello")


def update_12_4():
	print("colab_dc333.update_12_4 downgrades colab from cuda12.5 to cuda12.4 to make nvcc and nvidia-smi match")
	print("this takes 5minutes, please wait ...")
	os.environ['DEBIAN_FRONTEND'] = "noninteractive"
	os.system('apt-get update && apt-get install -y git')
	os.system('apt-get install -y emacs')
	os.system('apt-get install net-tools')
	os.system('apt-get install -y mlocate')
	os.system('apt-get install -y keyboard-configuration')
	os.system('wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb')
	os.system('dpkg -i cuda-keyring_1.1-1_all.deb')
	os.system('apt-get update')
	os.system('apt-get -y install cuda-toolkit-12-4')
	os.system('rm /etc/alternatives/cuda')
	os.system('ln -s  /usr/local/cuda-12.4 /etc/alternatives/cuda')
	os.system('nvcc --version')

def install_nemo():
	os.system('pip install nemo_toolkit["all"]')
	os.system('pip install git+https://github.com/NVIDIA/NeMo-Run.git')
	os.system('pip install megatron-core')
	os.system('pip install megatron-core')
	os.system('pip install transformer-engine[pytorch]')
	print("run from nemo.collections import llm and verify this works")

def device():
	device = torch.device('cpu')
	if torch.cuda.is_available():
		device = torch.device('cuda')
		gpu_stats = torch.cuda.get_device_properties(0)
		start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
		max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
		print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
		print(f"{start_gpu_memory} GB of memory reserved.")
	torch.set_default_device(device)
	print(f"Using device = {torch.get_default_device()}")

def gpu_memory():
	gpu_stats = torch.cuda.get_device_properties(0)
	start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
	max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
	print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
	print(f"{start_gpu_memory} GB of memory reserved.")