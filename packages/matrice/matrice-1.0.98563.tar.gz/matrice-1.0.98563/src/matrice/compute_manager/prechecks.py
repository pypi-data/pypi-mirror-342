import logging
import sys
import subprocess
from typing import Any, Optional
from matrice.compute_manager.scaling import Scaling
from matrice.compute_manager.actions_scaledown_manager import ActionsScaleDownManager
from matrice.compute_manager.resources_tracker import ResourcesTracker, MachineResourcesTracker, ActionsResourcesTracker
from matrice.compute_manager.instance_utils import (
    get_instance_info,
    cleanup_docker_storage,
    get_cpu_memory_usage,
    get_gpu_memory_usage,
    get_mem_usage,
    get_gpu_with_sufficient_memory_for_action,
    get_max_file_system,
    has_gpu
)
from matrice.docker_utils import check_docker


class Prechecks:
    def __init__(self, rpc: Any):
        self.rpc = rpc
        self.instance_id = None
        self.access_key = None 
        self.secret_key = None
        self.scaling = Scaling()
        self.actions_scale_down_manager = ActionsScaleDownManager(self.scaling)
        self.resources_tracker = ResourcesTracker()
        self.machine_resources_tracker = MachineResourcesTracker(self.scaling)
        self.actions_resources_tracker = ActionsResourcesTracker(self.scaling)

    def setup_docker(self):
        """
        Setup docker.
        """
        response, error, message = self.scaling.get_docker_hub_credentials()
        if error is None:
            self.docker_username = response["username"]
            self.docker_password = response["password"]
        else:
            logging.error(f"Error getting docker credentials: {error}")
            return
        try:
            cmd = f"docker login -u {self.docker_username} -p {self.docker_password}"
            subprocess.run(cmd, shell=True, check=True)
            logging.info("Successfully logged into Docker")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to login to Docker: {str(e)}")

    def create_docker_volume(self):
        """
        Create docker volume.
        """
        try:
            subprocess.run(['docker', 'volume', 'create', 'workspace'], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to create docker volume: {str(e)}")

    def get_available_resources(self):
        """Check available system resources are within valid ranges"""
        available_memory, available_cpu, gpu_memory_free, gpu_utilization = self.resources_tracker.get_available_resources()
        
        # Check CPU and memory percentages are valid
        if any(resource > 100 for resource in [available_memory, available_cpu]):
            logging.error(f"Resource usage exceeds 100%: Memory {available_memory}%, CPU {available_cpu}%")
            sys.exit(1)
            
        # Check GPU memory is within reasonable limits
        if gpu_memory_free > 256:
            logging.error(f"GPU memory exceeds 256GB limit: {gpu_memory_free}GB")
            sys.exit(1)
            
        # Check for negative values
        if any(resource < 0 for resource in [available_memory, available_cpu, gpu_memory_free, gpu_utilization]):
            logging.error(f"Resource usage cannot be negative: Memory {available_memory}%, CPU {available_cpu}%, GPU Memory {gpu_memory_free}GB")
            sys.exit(1)
            
        # Check GPU utilization is valid percentage
        if gpu_utilization > 100:
            logging.error(f"GPU utilization exceeds 100%: {gpu_utilization}%")
            sys.exit(1)
            
        logging.info("Resource availability check passed")
        return True
    
    def check_credentials(self, access_key: Optional[str] = None, secret_key: Optional[str] = None) -> bool:
        """Check if access key and secret key are valid"""
        if not access_key or not secret_key:
            logging.error("Missing access key or secret key")
            sys.exit(1)
        logging.info("Credentials check passed")
        return True

    def check_instance_id(self, instance_id: Optional[str] = None) -> bool:
        """Validate instance ID from args or env"""
        if not instance_id:
            logging.error("Missing instance ID")
            sys.exit(1)
            
        # Check instance ID format
        if not isinstance(instance_id, str) or len(instance_id) < 8:
            logging.error("Invalid instance ID format")
            sys.exit(1)
            
        self.instance_id = instance_id
        
        # Verify with scaling service
        instance_info = get_instance_info(self.instance_id)
        if not instance_info:
            logging.error(f"Invalid instance ID {self.instance_id}")
            sys.exit(1)
            
        logging.info(f"Instance ID {self.instance_id} validated")
        return True

    def check_docker(self) -> bool:
        """Check if docker is installed and working"""
        if not check_docker():
            logging.error("Docker not installed or not running")
            sys.exit(1)
            
        # Check docker API version compatibility
        try:
            import docker
            client = docker.from_env()
            client.ping()
        except Exception as e:
            logging.error(f"Docker API check failed: {str(e)}")
            sys.exit(1)
            
        logging.info("Docker check passed")
        return True

    def check_gpu(self) -> bool:
        """Check if machine has GPU and it's functioning"""
        gpu_mem = get_gpu_memory_usage()
        if not gpu_mem:
            logging.error("No GPU detected on this machine")
            sys.exit(1)
            
        # Check minimum GPU memory
        if any(mem < 4 for mem in gpu_mem.values()):
            logging.error("GPU has insufficient memory (min 4GB required)")
            sys.exit(1)
            
        # Check GPU drivers
        try:
            import torch
            if not torch.cuda.is_available():
                logging.error("CUDA not available")
                sys.exit(1)
        except ImportError:
            logging.warning("PyTorch not installed - skipping CUDA check")
            
        logging.info("GPU check passed")
        return True

    def check_resources(self) -> bool:
        """Validate system resource limits and availability"""
        # Check CPU usage
        cpu_usage = get_cpu_memory_usage()
        if cpu_usage > 100:
            logging.error(f"CPU usage exceeds 100%: {cpu_usage}%")
            sys.exit(1)
        elif cpu_usage > 90:
            logging.warning(f"High CPU usage: {cpu_usage}%")

        # Check memory usage
        mem_usage = get_mem_usage()
        if mem_usage > 100:
            logging.error(f"Memory usage exceeds 100%: {mem_usage}%")
            sys.exit(1)
        elif mem_usage > 90:
            logging.warning(f"High memory usage: {mem_usage}%")
            
        # Check GPU memory
        gpu_mem = get_gpu_memory_usage()
        if any(mem > 256 for mem in gpu_mem.values()):
            logging.error("GPU memory exceeds 256GB limit")
            sys.exit(1)
            
        # Check minimum available resources
        if cpu_usage > 95 or mem_usage > 95:
            logging.error("Insufficient available resources")
            sys.exit(1)
            
        logging.info("Resource limits check passed")
        return True

    def cleanup_docker_storage(self) -> bool:
        """Clean up docker storage and verify space freed"""
        try:
            initial_space = get_max_file_system()
            cleanup_docker_storage()
            final_space = get_max_file_system()
            
            if final_space <= initial_space:
                logging.warning("Docker cleanup did not free any space")
                
            return True
        except Exception as e:
            logging.error(f"Docker storage cleanup failed: {str(e)}")
            return False

    def get_shutdown_details(self) -> bool:
        """Get and validate shutdown details from response"""
        try:
            response = self.scaling.get_shutdown_details()
            
            # Validate response fields
            required_fields = ["shutdownThreshold", "launchDuration", "instanceSource"]
            if not all(field in response for field in required_fields):
                logging.error("Invalid shutdown details response")
                return False
                
            self.shutdown_threshold = response["shutdownThreshold"]
            self.launch_duration = response["launchDuration"] 
            self.instance_source = response["instanceSource"]
            
            # Validate values
            if not isinstance(self.shutdown_threshold, (int, float)) or self.shutdown_threshold <= 0:
                logging.error("Invalid shutdown threshold")
                return False
                
            if not isinstance(self.launch_duration, (int, float)) or self.launch_duration <= 0:
                logging.error("Invalid launch duration")
                return False
                
            return True
        except Exception as e:
            logging.error(f"Failed to get shutdown details: {str(e)}")
            return False

    def test_gpu(self) -> bool:
        """Test if GPU is working and has sufficient memory"""
        if has_gpu():   
            gpu_indices = get_gpu_with_sufficient_memory_for_action()
            if not gpu_indices:
                logging.error("No GPU with sufficient memory")
                sys.exit(1)
                
            # Test GPU computation
            try:
                import torch
                test_tensor = torch.cuda.FloatTensor(2, 2).fill_(1.0)
                result = torch.matmul(test_tensor, test_tensor)
                if not torch.all(result == 2.0):
                    logging.error("GPU computation test failed")
                    sys.exit(1)
            except Exception as e:
                logging.error(f"GPU computation test failed: {str(e)}")
                sys.exit(1)
                
        return True

    def check_get_gpu_indices(self) -> bool:
        """Check if get_gpu_indices returns valid indices"""
        gpu_indices = get_gpu_with_sufficient_memory_for_action()
        if not gpu_indices:
            logging.error("Failed to get GPU indices")
            sys.exit(1)
            
        # Validate indices
        if not all(isinstance(idx, int) and idx >= 0 for idx in gpu_indices):
            logging.error("Invalid GPU indices returned")
            sys.exit(1)
            
        # Check for duplicates
        if len(gpu_indices) != len(set(gpu_indices)):
            logging.error("Duplicate GPU indices returned")
            sys.exit(1)
            
        return True

    def check_resources_tracking(self) -> bool:
        """Test resource tracking updates and monitoring"""
        try:
            self.machine_resources_tracker.update_available_resources()
            self.actions_resources_tracker.update_actions_resources()
            
            return True
        except Exception as e:
            logging.error(f"Failed to update resource tracking: {str(e)}")
            sys.exit(1)

    def check_scaling_status(self) -> bool:
        """Test scaling service status"""
        try:
            downscaled_ids = self.scaling.get_downscaled_ids()
            if self.instance_id in downscaled_ids:
                logging.error("Instance is marked for downscaling")
                sys.exit(1)
            return True
        except Exception as e:
            logging.error(f"Failed to check scaling status: {str(e)}")
            sys.exit(1)

    def check_filesystem_space(self) -> bool:
        """Check available filesystem space and usage"""
        max_fs = get_max_file_system()
        if not max_fs:
            logging.error("Failed to get filesystem information")
            sys.exit(1)
        return True

    def test_actions_scale_down(self) -> bool:
        """Test actions scale down"""
        self.actions_scale_down_manager.auto_scaledown_actions()
        return True

    def check_fetch_actions(self) -> bool:
        """Test action fetching and validation"""
        fetched_actions, error, message = self.scaling.assign_jobs(has_gpu())
        if error:
            logging.error("Error assigning jobs: %s", error)
            return False
            
        # Validate fetched actions
        if fetched_actions:
            if not isinstance(fetched_actions, list):
                logging.error("Invalid actions format")
                return False
                
            for action in fetched_actions:
                if not isinstance(action, dict) or '_id' not in action:
                    logging.error("Invalid action format")
                    return False
                    
        return True
    
    def run_all_checks(self, instance_id: Optional[str] = None, 
                      access_key: Optional[str] = None,
                      secret_key: Optional[str] = None) -> bool:
        """Run all prechecks in sequence"""
        checks = [
            lambda: self.check_credentials(access_key, secret_key),
            lambda: self.check_instance_id(instance_id),
            self.check_docker,
            self.setup_docker,
            self.create_docker_volume,
            self.check_gpu,
            self.check_resources,
            self.cleanup_docker_storage,
            self.check_filesystem_space,
            self.check_resources_tracking,
            self.check_scaling_status,
            self.get_shutdown_details,
            self.test_gpu,
            self.check_get_gpu_indices,
            self.test_actions_scale_down,
            self.check_fetch_actions
        ]
        
        for check in checks:
            if not check():
                logging.error(f"Check failed: {check.__name__}")
                return False
                
        logging.info("All prechecks passed successfully")
        return True
