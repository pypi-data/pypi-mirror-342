# pylint: disable=C0301, disable=W0718, disable=W1510
"""
Module for Instance Utilities
"""
import os
import socket
import urllib.request
import subprocess
import logging
import psutil
from datetime import datetime
from matrice.utils import log_error
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def get_instance_info():
    """Get instance info"""
    try:
        service_provider = os.environ.get("SERVICE_PROVIDER") or "LOCAL"
        instance_id = os.environ.get("INSTANCE_ID") or ""

        # Check for GCP
        try:
            gcp_check = subprocess.run(
                "curl -s -m 1 -H 'Metadata-Flavor: Google' 'http://metadata.google.internal/computeMetadata/v1/instance/id'",
                shell=True,
                capture_output=True
            )
            if gcp_check.returncode == 0:
                service_provider = "GCP"
                instance_id = gcp_check.stdout.decode().strip()
        except subprocess.CalledProcessError:
            pass

        # Check for Azure
        try:
            azure_check = subprocess.run(
                "curl -s -m 1 -H Metadata:true 'http://169.254.169.254/metadata/instance?api-version=2020-09-01'",
                shell=True,
                capture_output=True
            )
            if azure_check.returncode == 0:
                service_provider = "AZURE"
                azure_id = subprocess.run(
                    "curl -s -H Metadata:true 'http://169.254.169.254/metadata/instance/compute/vmId?api-version=2017-08-01&format=text'",
                    shell=True,
                    capture_output=True
                )
                instance_id = azure_id.stdout.decode().strip()
        except subprocess.CalledProcessError:
            pass

        # Check for OCI
        try:
            oci_check = subprocess.run(
                "curl -s -m 1 -H 'Authorization: Bearer OracleCloud' 'http://169.254.169.254/opc/v1/instance/'",
                shell=True,
                capture_output=True
            )
            if oci_check.returncode == 0:
                service_provider = "OCI"
                oci_id = subprocess.run(
                    "curl -s http://169.254.169.254/opc/v1/instance/id",
                    shell=True,
                    capture_output=True
                )
                instance_id = oci_id.stdout.decode().strip()
        except subprocess.CalledProcessError:
            pass

        # Check for AWS
        try:
            aws_check = subprocess.run(
                "curl -s -m 1 http://169.254.169.254/latest/meta-data/",
                shell=True,
                capture_output=True
            )
            if aws_check.returncode == 0:
                service_provider = "AWS"
                aws_id = subprocess.run(
                    "curl -s http://169.254.169.254/latest/meta-data/instance-id",
                    shell=True,
                    capture_output=True
                )
                instance_id = aws_id.stdout.decode().strip()
        except subprocess.CalledProcessError:
            pass

        return str(service_provider), str(instance_id)

    except Exception as e:
        log_error("instance_utils.py", "get_instance_info", str(e))
        return None, None

def calculate_time_difference(start_time_str, finish_time_str):
    """Calculate time difference between start and finish times"""
    try:
        if os.environ["SERVICE_PROVIDER"] in ["AWS", "OCI", "LAMBDA"]:
            start_time = datetime.fromisoformat(start_time_str.split(".")[0] + "+00:00")
            finish_time = datetime.fromisoformat(
                finish_time_str.split(".")[0] + "+00:00"
            )
        else:
            start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            finish_time = datetime.fromisoformat(finish_time_str.replace("Z", "+00:00"))
        return int((finish_time - start_time).total_seconds())
    except Exception as e:
        logging.error(f"Error calculating time difference: {str(e)}")
        return 0

def has_gpu() -> bool:
    """
    Function to check if the system has a GPU
    """
    try:
        subprocess.run('nvidia-smi', check=True)
        return 1
    except Exception:
        return 0

def get_gpu_memory_usage():
    """
    Function to get GPU memory usage percentage as a float between 0 and 1
    """
    command = "nvidia-smi --query-gpu=memory.used,memory.total --format=csv,nounits,noheader"
    try:
        output = subprocess.check_output(command.split()).decode('ascii').strip().split('\n')
        memory_percentages = []
        for line in output:
            used, total = map(int, line.split(','))
            usage_percentage = used / total
            memory_percentages.append(usage_percentage)
        return min(memory_percentages)
    except Exception as e:
        logging.error(f"Error getting GPU memory usage: {e}")
        log_error("instance_utils.py", "get_gpu_memory_usage", e)
        return 0


def get_cpu_memory_usage():
    """
    Get CPU memory usage as a float between 0 and 1
    """
    try:
        memory = psutil.virtual_memory()
        return memory.percent / 100
    except Exception as e:
        logging.error(f"Error getting CPU memory usage: {e}")
        log_error("instance_utils.py", "get_cpu_memory_usage", e)
        return 0

def get_mem_usage():
    """
    Function to get memory usage as a float between 0 and 1
    """
    try:
        if has_gpu():
            try:
                mem_usage = get_gpu_memory_usage()
            except Exception as e:
                logging.error(f"Error getting GPU memory usage: {e}")
                log_error("instance_utils.py", "get_mem_usage", e)
                mem_usage = get_cpu_memory_usage()
        else:
            mem_usage = get_cpu_memory_usage()
    except Exception as e:
        logging.error(f"Error getting memory usage: {e}")
        log_error("instance_utils.py", "get_mem_usage", e)
        mem_usage = 0
    return mem_usage


def get_gpu_info():
    """
    Get GPU information.
    """
    with subprocess.Popen(
        [
            "nvidia-smi",
            "--query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu",
            "--format=csv,noheader,nounits",
        ],
        stdout=subprocess.PIPE,
    ) as p:
        stdout, _ = p.communicate()
        output = stdout.decode("UTF-8")
        return output.split("\n")[:-1]


def get_instance_id() -> str:
    """
    Function to get instance ID
    """
    try:
        return os.environ['INSTANCE_ID']
    except KeyError as e:
        logging.error("Environment variable 'INSTANCE_ID' is not set")
        log_error("instance_utils.py", "get_instance_id", e)
        return ""

def is_docker_running():
    """
    Function to check if Docker is running
    """
    try:
        command = "docker ps"
        docker_images = (
            subprocess.check_output(command.split())
            .decode("ascii")
            .split("\n")[:-1][1:]
        )
        return len(docker_images) > 0
    except Exception as e:
        log_error("instance_utils.py", "is_docker_running", e)
        logging.error(f"Error checking Docker status: {e}")
        return False

def prune_docker_images():
    """
    Function to prune Docker images
    """
    try:
        # Execute the Docker prune command with the -a flag
        subprocess.run(["docker", "image", "prune", "-a", "-f"], check=True)
        logging.info("Docker images pruned successfully.")
    except subprocess.CalledProcessError as e:
        log_error("instance_utils.py", "prune_docker_images", e)
        logging.error(f"Error pruning Docker images: {e}")

def _normalize_disk_usage_to_GB(disk_space):
    """
    Function to normalize disk usage information to GB
    """
    try:
        if disk_space.endswith('G'):
            disk_space = float(disk_space[:-1])
        elif disk_space.endswith('T'):
            disk_space = float(disk_space[:-1]) * 1024
        elif disk_space.endswith('M'):
            disk_space = float(disk_space[:-1]) / 1024
        elif disk_space.endswith('K'):
            disk_space = float(disk_space[:-1]) / (1024 * 1024)
        else:
            disk_space = float(disk_space)
        logging.debug(f"Normalized disk space value to {disk_space} GB")
        return disk_space
    except (ValueError, AttributeError) as e:
        logging.error(f"Failed to normalize disk space value: {str(e)}")
        log_error("instance_utils.py", "_normalize_disk_usage_to_GB", e)
        return 0.0

def _parse_disk_usage_info(line):
    """
    Function to parse disk usage information
    """
    try:
        parts = line.split()
        parsed_info = {
            "filesystem": parts[0],
            "size": float(_normalize_disk_usage_to_GB(parts[1])),
            "used": float(_normalize_disk_usage_to_GB(parts[2])),
            "available": float(_normalize_disk_usage_to_GB(parts[3])),
            "use_percentage": float(parts[4].rstrip('%')),
            "mounted_on": parts[5]
        }
        logging.debug(f"Successfully parsed disk usage info: {parsed_info}")
        return parsed_info
    except Exception as e:
        logging.error(f"Failed to parse disk usage info: {str(e)}")
        log_error("instance_utils.py", "_parse_disk_usage_info", e)
        return None

def get_disk_space_usage():
    """
    Function to get disk space usage information for all filesystems
    """
    try:
        logging.info("Getting disk space usage information")
        result = subprocess.run(['df', '-h'], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')[1:]
        disk_usage = []

        for line in lines:
            disk = _parse_disk_usage_info(line)
            if disk:
                disk_usage.append(disk)
        logging.info(f"Found disk usage info for {len(disk_usage)} filesystems")
        return disk_usage
    except Exception as e:
        logging.error(f"Failed to get disk space usage: {str(e)}")
        log_error("instance_utils.py", "get_disk_space_usage", e)
        return None

def get_max_file_system():
    """
    Function to get filesystem with maximum available space.
    Excludes special filesystems and returns the one with most available space.
    If root or empty filesystem is found, creates and returns workspace directory.
    
    Returns:
        str|None: Path to filesystem with most space, workspace dir, or None on error
    """
    try:
        logging.info("Finding filesystem with maximum available space")
        disk_usage = get_disk_space_usage()
        if not disk_usage:
            logging.warning("No disk usage information available")
            return None

        # Filter out special filesystems and those with no available space
        filtered_disks = [
            disk for disk in disk_usage 
            if (disk["mounted_on"] != '/boot/efi' 
                and "overlay" not in disk["filesystem"]
                and disk["available"] > 0)
        ]
        
        if not filtered_disks:
            logging.warning("No suitable filesystems found after filtering")
            max_available_filesystem = ""
        else:
            max_disk = max(filtered_disks, key=lambda x: x["available"]) 
            max_available_filesystem = max_disk["mounted_on"]
            logging.info(f"Found filesystem with maximum space: {max_available_filesystem} "
                        f"({max_disk['available']:.2f} GB available)")

        # For root or empty filesystem, create workspace in home directory
        if max_available_filesystem in ['/', '']:
            home_dir = os.path.expanduser("~")
            if not os.environ.get("WORKSPACE_DIR"):
                logging.error("WORKSPACE_DIR environment variable not set")
                return None
            workspace_dir = os.path.join(home_dir, os.environ["WORKSPACE_DIR"])
            os.makedirs(workspace_dir, exist_ok=True)
            logging.info(f"Created workspace directory at: {workspace_dir}")
            return workspace_dir

        return max_available_filesystem

    except Exception as e:
        logging.error(f"Failed to get max filesystem: {str(e)}")
        log_error("instance_utils.py", "get_max_file_system", e)
        return None

def get_docker_disk_space_usage():
    """
    Function to get disk space usage information for Docker storage.
    """
    try:
        # Get the Docker root directory from docker info
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True, check=True)
        docker_info = result.stdout
        
        # Extract the Docker root directory (e.g., /var/lib/docker)
        docker_root_dir = None
        for line in docker_info.split('\n'):
            if line.strip().startswith('Docker Root Dir'):
                docker_root_dir = line.split(':')[1].strip()
                break

        if docker_root_dir is None:
            logging.error("Unable to find Docker root directory")
            raise Exception("Unable to find Docker root directory")

        logging.debug(f"Found Docker root directory: {docker_root_dir}")

        # Run df to get disk usage for Docker's root directory
        result = subprocess.run(['df', '-h', docker_root_dir], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        
        if not lines:
            logging.error("No disk usage information found for Docker root directory")
            raise Exception("No disk usage information found for Docker root directory")

        # Parse the disk usage output
        docker_disk_usage = _parse_disk_usage_info(lines[0])
        if docker_disk_usage is None:
            logging.error("Failed to parse Docker disk usage information")
            raise Exception("Failed to parse Docker disk usage information")

        logging.info(f"Successfully retrieved Docker disk usage: {docker_disk_usage}")
        return docker_disk_usage
    except Exception as e:
        logging.error(f"Failed to get Docker disk space usage: {str(e)}")
        log_error("instance_utils.py", "get_docker_disk_space_usage", e)
        return None

def cleanup_docker_storage():
    """
    Function to clean up Docker storage
    """
    docker_disk_usage = get_docker_disk_space_usage()
    if docker_disk_usage is None:
        logging.error("Failed to get Docker disk space usage, skipping cleanup")
        return

    if docker_disk_usage["use_percentage"] >= 90 or docker_disk_usage["available"] <= 30:
        logging.info(f"Pruning Docker images. Disk space is low: {docker_disk_usage}")
        try:
            prune_docker_images()
        except Exception as e:
            logging.error(f"Failed to clean up Docker storage: {str(e)}")
            log_error("instance_utils.py", "cleanup_docker_storage", e)

def get_required_gpu_memory(action_details):
    """
    Function to get required GPU memory
    """
    try:
        required_gpu_memory = action_details["actionDetails"]["expectedResources"][
            "gpuMemory"
        ]
    except KeyError:
        required_gpu_memory = 0
    return required_gpu_memory

def is_allowed_gpu_device(gpu_index):
    """
    Check if a GPU device is allowed based on GPUS environment variable.
    
    Args:
        gpu_index (int): Index of the GPU device to check
        
    Returns:
        bool: True if the GPU is allowed, False otherwise
    """
    try:
        gpus = os.environ.get("GPUS")
        if not gpus:
            return True
        allowed_gpus = [int(x) for x in gpus.split(",") if x.strip()]
        return int(gpu_index) in allowed_gpus
    except Exception as e:
        logging.warning(f"Error checking allowed GPU device: {e}")
        return True

def get_gpu_with_sufficient_memory_for_action(action_details):
    """
    Get list of GPUs with sufficient total memory for the action.
    
    Args:
        action_details (dict): Action details containing memory requirements
        
    Returns:
        list[int]: List of GPU indices that can be used
        
    Raises:
        ValueError: If insufficient GPU memory is available
    """
    required_gpu_memory = get_required_gpu_memory(action_details)
    command = "nvidia-smi --query-gpu=memory.free --format=csv"

    try:
        memory_free_info = subprocess.check_output(command.split()).decode("ascii").split("\n")
        if len(memory_free_info) < 2:
            raise ValueError("No GPU information available from nvidia-smi")
            
        # Skip header row and empty last line
        memory_free_values = [int(x.split()[0]) for x in memory_free_info[1:-1]]
        
        # Try single GPU first for smaller memory requirements
        if required_gpu_memory < 80000:
            try:
                return get_single_gpu_with_sufficient_memory_for_action(action_details)
            except ValueError:
                pass

        # Otherwise try multiple GPUs
        selected_gpus = []
        total_memory = 0
        
        for i, mem in enumerate(memory_free_values):
            if not is_allowed_gpu_device(i):
                continue
            if total_memory >= required_gpu_memory:
                break
            selected_gpus.append(i)
            total_memory += mem

        if total_memory >= required_gpu_memory:
            return selected_gpus
            
        raise ValueError(f"Insufficient GPU memory available. Required: {required_gpu_memory}, Available: {total_memory}")
            
    except Exception as e:
        logging.error(f"Error getting GPU memory info: {e}")
        raise ValueError(f"Failed to get GPU memory information: {str(e)}")

def get_single_gpu_with_sufficient_memory_for_action(action_details):
    """
    Get single GPU with sufficient memory using best-fit approach.
    
    Args:
        action_details (dict): Action details containing memory requirements
        
    Returns:
        list[int]: List containing single GPU index
        
    Raises:
        ValueError: If no single GPU has sufficient memory
    """
    required_gpu_memory = get_required_gpu_memory(action_details)
    command = "nvidia-smi --query-gpu=memory.free --format=csv"

    try:
        memory_free_info = subprocess.check_output(command.split()).decode("ascii").split("\n")
        if len(memory_free_info) < 2:
            raise ValueError("No GPU information available from nvidia-smi")
            
        # Skip header row and empty last line
        memory_free_values = [int(x.split()[0]) for x in memory_free_info[1:-1]]

        # Find best fit GPU (smallest GPU with sufficient memory)
        best_fit_gpu = None
        best_fit_memory = float('inf')
        
        for i, mem in enumerate(memory_free_values):
            if not is_allowed_gpu_device(i):
                continue
            if mem >= required_gpu_memory and mem < best_fit_memory:
                best_fit_gpu = i
                best_fit_memory = mem

        if best_fit_gpu is not None:
            return [best_fit_gpu]
            
        raise ValueError(f"No single GPU with sufficient memory ({required_gpu_memory}MB) available")
            
    except Exception as e:
        logging.error(f"Error getting GPU memory info: {e}")
        raise ValueError(f"Failed to get GPU memory information: {str(e)}")

def get_decrypted_access_key_pair(enc_access_key, enc_secret_key, encryption_key=""):
    """
    Function to get decrypted access key pair
    """
    encryption_key = encryption_key or os.environ.get("MATRICE_ENCRYPTION_KEY")
    if not encryption_key:
        logging.warning("Encryption key is not set, Will assume that the keys are not encrypted")
        return enc_access_key, enc_secret_key

    # Decode the base64 encoded keys
    encrypted_access_key = base64.b64decode(enc_access_key)
    encrypted_secret_key = base64.b64decode(enc_secret_key)

    # Extract nonce and tag from encrypted data
    nonce = encrypted_access_key[:12]
    tag = encrypted_access_key[-16:]
    ciphertext = encrypted_access_key[12:-16]

    # Create cipher with authentication tag
    cipher = Cipher(algorithms.AES(encryption_key.encode()), 
                   modes.GCM(nonce, tag),
                   backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the access key
    decrypted_access_key = decryptor.update(ciphertext) + decryptor.finalize()

    # Repeat for secret key
    nonce = encrypted_secret_key[:12]
    tag = encrypted_secret_key[-16:]
    ciphertext = encrypted_secret_key[12:-16]

    cipher = Cipher(algorithms.AES(encryption_key.encode()),
                   modes.GCM(nonce, tag), 
                   backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_secret_key = decryptor.update(ciphertext) + decryptor.finalize()

    # Convert the decrypted keys to strings
    access_key = decrypted_access_key.decode('utf-8',errors='replace')
    secret_key = decrypted_secret_key.decode('utf-8',errors='replace')

    return access_key, secret_key


def check_public_port_exposure(port):
    """
    Check if a given port is publicly accessible and locally available.
    
    Args:
        port (int): The port number to check
        
    Returns:
        bool: True if port is both publicly accessible and locally available, False otherwise
    """
    is_public_exposed = False
    is_locally_available = False

    # Public Exposure Check
    try:
        public_ip = (
            urllib.request.urlopen("https://ident.me", timeout=10).read().decode("utf8")
        )

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn_sock:
            conn_sock.settimeout(3)
            result = conn_sock.connect_ex((public_ip, port))
            is_public_exposed = result == 0
    except (urllib.error.URLError, socket.timeout) as e:
        logging.error(f"Failed to get public IP or connect to port: {str(e)}")
    except Exception as e:
        logging.error(
            f"Unexpected error during public exposure check for port {port}: {str(e)}"
        )

    # Local Availability Check
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bind_sock:
            bind_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            bind_sock.bind(("", port))
            bind_sock.listen(1)
            is_locally_available = True
    except socket.error as e:
        if hasattr(e, "errno") and e.errno == socket.EADDRINUSE:
            logging.debug(f"Port {port} is already in use locally")
        else:
            logging.error(f"Socket error checking local port {port}: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error checking local port {port}: {str(e)}")

    # Return False if either check fails
    if not is_public_exposed:
        logging.debug(f"Port {port} is not publicly exposed")
        return False
    if not is_locally_available:
        logging.debug(f"Port {port} is not locally available")
        return False
        
    return True
