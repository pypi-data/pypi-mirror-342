import logging
import docker
from matrice.compute_manager.scaling import Scaling

class ActionsScaleDownManager:
    """
    Class for managing scale down.
    """
    def __init__(self, scaling: Scaling):
        self.docker_client = docker.from_env()
        self.scaling = scaling

    def auto_scaledown_actions(self):
        """
        Start polling for containers that need to be scaled down and stop them.
        """
        down_scaled_jobs, error, message = self.scaling.get_downscaled_ids()
        if error is not None:
            logging.error(f"Error getting downscaled ids: {error}")
            return
        containers = self.docker_client.containers.list(
            filters={"status": "running"}, all=True
        )
        if down_scaled_jobs:
            for container in containers:
                container_id = container.id
                inspect_data = self.docker_client.api.inspect_container(container_id)
                action_record_id = next(
                    (arg for arg in inspect_data["Args"] if len(arg) == 24), None
                )
                if action_record_id in down_scaled_jobs:
                    try:
                        container.stop()
                        logging.info(f"Container {container_id} stopped.")
                    except docker.errors.APIError as e:
                        logging.error(f"Failed to stop container {container_id}: {str(e)}")
