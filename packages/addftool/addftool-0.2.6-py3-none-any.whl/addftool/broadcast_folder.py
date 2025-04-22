import os
import time
import fnmatch
import subprocess
import hashlib
from concurrent.futures import ThreadPoolExecutor

from fabric import Connection, ThreadingGroup

try:
    import torch
    import torch.distributed as dist
    from torch.distributed import init_process_group, destroy_process_group
    _torch_is_available = True
except ImportError:
    _torch_is_available = False


def add_broadcast_folder_args(subparsers):
    deploy_parser = subparsers.add_parser('broadcast-folder', help='broadcast folder from master node to other nodes')
    add_args(deploy_parser)


def add_args(parser):
    parser.add_argument("--tool", help="tool name", type=str, default="torch_nccl", choices=["torch_nccl"])
    parser.add_argument("--hostfile", help="host file, broadcast file from node-0 to others", type=str, default="")

    parser.add_argument("--download_timeout", help="download timeout, default is 30 min", type=int, default=60 * 30)

    parser.add_argument("--md5_verify", action='store_true', default=False,
                        help="whether to verify the md5 of the file after broadcast, default is False.")
    parser.add_argument("--port", help="the port for torchrun, default is 29501", type=int, default=29501)
    parser.add_argument("--torchrun_alias", type=str, default="torchrun",
                        help="the alias of torchrun, default is torchrun. If you use torchrun, please set it to torchrun.")
    parser.add_argument("--transfer_ranks_per_node", type=int, default=8,
                        help="the number of ranks per node to transfer the files, default is 8.")

    parser.add_argument("--contain_md5_files", action='store_true', default=False,
                        help="whether to contain the md5 files in the folder, default is False. " \
                        "If True, the md5 files will be transferred to the other nodes and verified. " \
                        "If False, the md5 files will be ignored.")

    parser.add_argument("--include-string", type=str, default="",
                        help="the string to include the files, default is empty. " \
                        "Such as *.py, *.yaml, *.json, \"*.pt;*.pth\" etc. " \
                        "Only node-0 will include the files from the folder, " \
                        "If empty, will transfer all the files from the node-0's local folder.")
    parser.add_argument("--exclude-string", type=str, default="",
                        help="the string to exclude the files, default is empty. " \
                        "Such as *.py, *.yaml, *.json, \"*.pt;*.pth\" etc. " \
                        "Only node-0 will exclude the files from the folder, " \
                        "If empty, will transfer all the files from the node-0's local folder.")

    parser.add_argument("--from_blob_url", type=str, default="",
                        help="the blob url to download from, default is empty. " \
                        "Only node-0 will download the files from the blob url, " \
                        "If empty, will transfer the files from the node-0's local folder.")
    
    # distributed downloader from blob
    parser.add_argument("folder", help="the folder need to broadcast", type=str)


class ConnectionWithCommand(Connection):
    def __init__(self, host, temp_config_dir, puts, command):
        super().__init__(host)
        self.command = command
        self.puts = puts
        self.temp_config_dir = temp_config_dir

    def run(self, command, **kwargs):
        super().run(f"mkdir -p {self.temp_config_dir}", **kwargs)
        for src, dest in self.puts:
            self.put(src, remote=dest)
        print(f"Running command on {self.original_host}: {self.command}")
        super().run(self.command, **kwargs)
        if command:
            super().run(command, **kwargs)


def get_ip_via_ssh(hostname):
    if hostname == "localhost":
        return "127.0.0.1"
    try:
        cmd = ["ssh", hostname, "hostname -I | awk '{print $1}'"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            ip = result.stdout.strip()
            return ip
        else:
            print(f"SSH {hostname} failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error executing SSH command on {hostname}: {e}")
        return None


def parallel_check_md5(file_list, expected_md5s):
    """
    Parallel check MD5 checksums for the given files.
    
    Args:
        file_list: List of file paths to check
        md5_dir: Directory containing MD5 files
        
    Returns:
        True if all MD5 checksums match, False otherwise
    """
    def calculate_md5(file_path):
        # Call md5sum and capture output
        result = subprocess.run(["md5sum", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Failed to calculate MD5 for {file_path}: {result.stderr}")
            return file_path, None
        
        # md5sum output format: "<md5_hash>  <file_path>"
        md5_hash = result.stdout.strip().split()[0]
        return file_path, md5_hash
    
    # Calculate MD5 checksums in parallel
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(calculate_md5, file_list))
    
    # Check if all MD5s match
    all_match = True
    for file_path, actual_md5 in results:
        if actual_md5 is None:
            all_match = False
            continue
        
        if file_path not in expected_md5s:
            print(f"No expected MD5 for {file_path}")
            all_match = False
            continue
            
        expected_md5 = expected_md5s[file_path]
        if actual_md5 != expected_md5:
            print(f"MD5 mismatch for {file_path}: expected {expected_md5}, got {actual_md5}")
            all_match = False
    
    return all_match


def broadcast_folder_main(args):
    with open(args.hostfile, "r") as f:
        host_list = []
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                host_list.append(line)
    
    print(f"Find {len(host_list)} hosts in hostfile: {args.hostfile}")
    connection_list = []

    remote_temp_config_dir = "/tmp/broadcast_temp_config_dir"

    master_addr = get_ip_via_ssh(host_list[0])

    for i, host in enumerate(host_list):
        put_commands = []
        put_commands.append((__file__, os.path.join(remote_temp_config_dir, "broadcast.py")))
        commnads = "NCCL_IB_DISABLE=0 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 "
        if os.environ.get("SAS_TOKEN") is not None and i == 0:
            commnads += f"SAS_TOKEN=\"{os.environ['SAS_TOKEN']}\" "
        commnads += f"{args.torchrun_alias} --nproc_per_node={args.transfer_ranks_per_node} --nnodes={len(host_list)} --node_rank={i} --master_addr={master_addr} --master_port={args.port}"
        commnads += f" {remote_temp_config_dir}/broadcast.py {args.folder} --tool {args.tool} --transfer_ranks_per_node {args.transfer_ranks_per_node} "
        if args.contain_md5_files:
            commnads += " --contain_md5_files"
        if args.include_string:
            commnads += f" --include-string \"{args.include_string}\""
        if args.exclude_string:
            commnads += f" --exclude-string \"{args.exclude_string}\""
        if args.from_blob_url and i == 0:
            commnads += f" --from_blob_url {args.from_blob_url}"
        if args.md5_verify:
            commnads += " --md5_verify"
        
        connection_list.append(ConnectionWithCommand(host, remote_temp_config_dir, put_commands, commnads))
    
    group = ThreadingGroup.from_connections(connection_list)
    group.run('echo "Hello"', hide=False)


def download_files_from_blob(queue, blob_url, sas_token, folder, download_files, node_rank):
    if not blob_url.endswith("/"):
        blob_url += "/"
    print(f"Node-{node_rank} start downloading {len(download_files)} files from {blob_url} to {folder}")
    for file_name in download_files:
        file_path = os.path.join(folder, file_name)
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)
        for try_count in range(3):
            try:
                download_status = subprocess.run(
                    ["azcopy", "copy", blob_url + file_name + sas_token, file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if download_status.returncode != 0:
                    raise RuntimeError(f"Failed to download {file_name}: {download_status.stderr}")
                print(f"Rank {node_rank}: Downloaded {file_name} successfully, from {blob_url} to {file_path}")
                queue.put(file_path)
                break
            except Exception as e:
                print(f"Rank {node_rank}: Download failed: {e}")


def broadcast_file_from_rank(rank, file_path, from_rank, device, file_size, max_chunk_size=250 * 1024 * 1024, md5_verify=False, group=None):
    if file_size == 0:
        if rank != from_rank:
            with open(file_path, "wb") as f:
                f.write(b"")
        return

    if group is None:
        group = dist.group.WORLD
    pinned_cpu_tensor = torch.empty(min(max_chunk_size, file_size), dtype=torch.uint8).pin_memory()

    for offset in range(0, file_size, max_chunk_size):
        read_size = min(max_chunk_size, file_size - offset)
        if rank == from_rank:
            with open(file_path, "rb") as f:
                f.seek(offset)
                data = f.read(read_size)
            tensor = torch.frombuffer(data, dtype=torch.uint8).contiguous().pin_memory()
            tensor = tensor.to(device)
            torch.cuda.synchronize()
            dist.broadcast(tensor, src=from_rank, group=group, async_op=True)
        else:
            tensor = torch.empty(read_size, dtype=torch.uint8, device=device)
            dist.broadcast(tensor, src=from_rank, group=group)
            torch.cuda.synchronize()

            file_dir = os.path.dirname(file_path)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)

            with open(file_path, "ab" if offset > 0 else "wb") as f:
                pinned_cpu_tensor[:read_size].copy_(tensor)
                np_array = pinned_cpu_tensor.numpy()[:read_size]
                np_array.tofile(f)
    
    if md5_verify:
        if rank == from_rank:
            with open(file_path, "rb") as f:
                file_md5 = hashlib.md5(f.read()).hexdigest()
            md5_tensor = torch.frombuffer(file_md5.encode('utf-8'), dtype=torch.uint8).to(device)
            dist.broadcast(md5_tensor, src=from_rank, group=group)
        else:
            with open(file_path, "rb") as f:
                file_md5 = hashlib.md5(f.read()).hexdigest()
            src_md5_tensor = torch.empty(32, dtype=torch.uint8, device=device)
            dist.broadcast(src_md5_tensor, src=from_rank, group=group)

            src_md5_str = src_md5_tensor.cpu().numpy().tobytes().decode('utf-8')
            if file_md5 != src_md5_str:
                raise ValueError(f"MD5 verification failed for {file_path}: {file_md5} != {src_md5_str}")


def broadcast_folder_worker(args):
    assert args.tool in ["torch_nccl"], f"tool {args.tool} is not supported"
    if not _torch_is_available:
        raise ImportError("Torch is not available. Please install torch to use this feature.")
    start_time = time.time()

    init_process_group(backend='nccl')
    global_rank = int(os.environ['RANK'])
    local_rank = int(os.environ['LOCAL_RANK'])
    world_size = int(os.environ['WORLD_SIZE'])
    num_nodes = world_size // args.transfer_ranks_per_node
    worker_rank = local_rank

    num_gpus = torch.cuda.device_count()
    torch.cuda.set_device(worker_rank % num_gpus)

    device = torch.device(f"cuda:{worker_rank % num_gpus}")
    
    workers_groups = []
    for i in range(args.transfer_ranks_per_node):
        worker_ranks = []
        for j in range(num_nodes):
            worker_ranks.append(j * args.transfer_ranks_per_node + i)
        
        if global_rank == 0:
            print(f"worker group {i} ranks: {worker_ranks}")
        
        workers_groups.append(dist.new_group(worker_ranks))

    if global_rank == 0:
        print(f"Init {len(workers_groups)} worker groups")

    print(f"rank {global_rank} start broadcast worker, args = {args}, nccl init time: {time.time() - start_time:.2f}s")
    
    file_size_dict = {}
    
    if global_rank == 0:
        # Parse include and exclude patterns
        include_patterns = [p.strip() for p in args.include_string.split(";") if p.strip()]
        exclude_patterns = [p.strip() for p in args.exclude_string.split(";") if p.strip()]
        
        print(f"Include patterns: {include_patterns}")
        print(f"Exclude patterns: {exclude_patterns}")
        
        if not os.path.exists(args.folder):
            raise ValueError(f"Folder {args.folder} does not exist.")
        
        # Gather and filter files in a single pass
        file_size_dict = {}
        for root, dirs, files in os.walk(args.folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                
                # Skip md5 files if not containing them
                if file_name.endswith(".md5") and not args.contain_md5_files:
                    continue
                    
                # Apply include filters first (if any)
                included = not include_patterns  # Include by default if no include patterns
                if include_patterns:
                    for pattern in include_patterns:
                        if fnmatch.fnmatch(file_name, pattern):
                            included = True
                            break
                
                # Then apply exclude filters
                if included and exclude_patterns:
                    for pattern in exclude_patterns:
                        if fnmatch.fnmatch(file_name, pattern):
                            included = False
                            break
                
                # Add to file dict if passes both filters
                if included:
                    file_size_dict[file_path] = os.path.getsize(file_path)
        
        print(f"After filtering: {len(file_size_dict)} files selected for transfer")
        if len(include_patterns) > 0 or len(exclude_patterns) > 0:
            print(f"Files selected for transfer: {file_size_dict.keys()}")
        
        # sort the file list by size
        file_list = sorted(file_size_dict.keys(), key=lambda x: file_size_dict[x], reverse=True)
        file_size_list = [file_size_dict[file] for file in file_list]
        obj_list = [file_list, file_size_list]
        dist.broadcast_object_list(obj_list, src=0)
    else:
        obj_list = [None, None]
        dist.broadcast_object_list(obj_list, src=0)
        file_list, file_size_list = obj_list
    
    print(f"Rank {global_rank}: {len(file_list)} files, total size: {sum(file_size_list) / (1024 * 1024):.2f} MB, time taken: {time.time() - start_time:.2f}s")
    
    worker_g = workers_groups[worker_rank]
    from_rank = global_rank % args.transfer_ranks_per_node
    broadcast_file_list = []
    for i in range(len(file_list)):
        if i % args.transfer_ranks_per_node == worker_rank:
            file_path = file_list[i]
            file_size = file_size_list[i]
            broadcast_file_from_rank(
                global_rank, file_path, from_rank, device,
                file_size, md5_verify=args.md5_verify, group=worker_g,
            )
            if global_rank == from_rank:
                print(f"Group {global_rank} finished broadcasting {file_path}, size: {file_size / (1024 * 1024):.2f} MB, time taken: {time.time() - start_time:.2f}s")
            broadcast_file_list.append(file_path)
    
    dist.barrier()
    for i in range(len(workers_groups)):
        if i != worker_rank:
            dist.destroy_process_group(workers_groups[i])
    destroy_process_group()

    if args.contain_md5_files and global_rank % args.transfer_ranks_per_node == 0:
        to_verify_files = []
        excepted_md5s = {}
        for file_path in file_list:
            if not file_path.endswith(".md5"):
                md5_file_path = file_path + ".md5"
                if os.path.exists(md5_file_path):
                    with open(md5_file_path, "r") as f:
                        md5_hash = f.read().strip()
                    excepted_md5s[file_path] = md5_hash
                    to_verify_files.append(file_path)
                else:
                    print(f"MD5 file {md5_file_path} not found, skipping verification.")
        
        # Verify MD5 checksums
        if not parallel_check_md5(to_verify_files, excepted_md5s):
            print(f"MD5 verification failed for some files, please check the logs.")
            raise ValueError("MD5 verification failed.")
        else:
            print(f"Rank-{global_rank}: MD5 verification passed for all files.")

    print(f"Rank {global_rank} finished broadcasting all files, time taken: {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Addf's tool")
    add_args(parser)
    args = parser.parse_args()
    if args.hostfile:
        broadcast_folder_main(args)
    else:
        broadcast_folder_worker(args)
