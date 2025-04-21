import logging
import os
import shlex
import subprocess
import threading
import time
import signal
from matrice.compute_manager.instance_utils import (
    get_gpu_with_sufficient_memory_for_action,
    get_decrypted_access_key_pair,
    get_max_file_system,
)
from matrice.compute_manager.task_utils import setup_workspace_and_run_task
from matrice.compute_manager.scaling import Scaling


class ActionInstance:
    """Base class for tasks that run in Action containers."""

    def __init__(self, scaling: Scaling, action_info):
        """Initialize an action instance.

        Args:
            scaling (Scaling): Scaling service instance
            action_info (dict): Action information dictionary
        """
        self.scaling = scaling
        self.process: subprocess.Popen = None
        self.stop_thread = False
        self.log_thread = None
        self.log_path = None

        self.action_info = action_info
        self.action_record_id = action_info["_id"]
        self.action_type = action_info["action"]
        self.action_details = action_info["actionDetails"]
        self.docker_container = self.action_details.get(
            "docker",
            self.action_details.get(
                "docker_container", self.scaling.get_data_processing_image()
            ),
        )

        self.actions_map = {
            "model_train": model_train_execute,
            "model_eval": model_eval_execute,
            "model_export": model_export_execute,
            "deploy_add": model_deploy_execute,
            "data_import": data_processing_execute,
            "data_add": data_processing_execute,
            "data_split": data_split_execute,
            "data_prep": data_preparation_execute,
            "dataset_annotation": dataset_annotation_execute,
            "image_build": image_build_execute,
            "resource_clone": resource_clone_execute,
        }

        if self.action_type not in self.actions_map:
            raise ValueError(f"Unknown action type: {self.action_type}")

        self.task = self.actions_map[self.action_type]

    def _init_credentials(self):
        """Initialize Matrice credentials."""
        self.matrice_access_key_id = self.scaling.session.access_key
        self.matrice_secret_access_key = self.scaling.session.secret_key

        if not all([self.matrice_access_key_id, self.matrice_secret_access_key]):
            raise ValueError(
                "MATRICE_ACCESS_KEY_ID and MATRICE_SECRET_ACCESS_KEY environment variables are required"
            )

        return {
            "matrice_access_key_id": self.matrice_access_key_id,
            "matrice_secret_access_key": self.matrice_secret_access_key,
        }

    def get_log_path(self):
        """Get log directory path, creating if needed."""
        os.makedirs("logs", exist_ok=True)
        return "logs"

    def is_running(self):
        """Check if task process is running."""
        try:
            return self.process and self.process.poll() is None
        except Exception as err:
            logging.error(f"Error checking if task is running: {err}")
            return False

    def get_action_details(self):
        """Get action details from scaling service."""
        resp, error, message = self.scaling.get_action_details(self.action_record_id)
        if error:
            logging.error(f"Error getting action details: {error}")
            return None
        return resp

    def get_gpu_config(self, action_details):
        """Get GPU configuration string based on available GPUs."""
        gpu_indices = get_gpu_with_sufficient_memory_for_action(
            action_details=action_details
        )
        if gpu_indices:
            gpu_str = ",".join(map(str, gpu_indices))
            logging.info(f"Using GPUs: {gpu_str}")
            return f'--gpus "device={gpu_str}"'
        logging.info("No GPUs with sufficient memory found.")
        return ""

    def get_base_docker_cmd(
        self,
        work_fs="",
        use_gpu="",
        mount_docker_sock=False,
        port=None,
        action_id="",
        model_key="",
        internal_api_key="",
        destination_workspace_path="/usr/src/workspace",
        docker_workdir="",
    ):
        """Build base Docker command with common options."""
        if not docker_workdir:
            docker_workdir = f"/usr/src/{action_id}"
        cmd_parts = [
            f"docker run {use_gpu} ",
            (
                f"-v {work_fs}/workspace:{destination_workspace_path}"
                if work_fs not in ["", "/"]
                else " "
            ),
            (
                f"-v {work_fs}/{action_id}:/usr/src/{action_id}"
                if work_fs not in ["", "/"] and action_id
                else " "
            ),
            (
                "-v /var/run/docker.sock:/var/run/docker.sock"
                if mount_docker_sock
                else " "
            ),
            f"-p {port}:80 " if port else " ",
            f"-e ENV={shlex.quote(os.environ['ENV'])} ",
            f"-e MATRICE_SECRET_ACCESS_KEY={shlex.quote(self.matrice_secret_access_key)} ",
            f"-e MATRICE_ACCESS_KEY_ID={shlex.quote(self.matrice_access_key_id)} ",
            (
                f"-e MATRICE_INTERNAL_API_KEY={internal_api_key} "
                if internal_api_key
                else " "
            ),
            (
                f"-e HUGGING_FACE_ACCESS_TOKEN={shlex.quote(self.get_hugging_face_token(model_key))} "
                if model_key
                else ""
            ),
            f"--shm-size=30G --pull=always {shlex.quote(self.docker_container)} "
            f'/bin/bash -c "cd {docker_workdir} && '
            f"if [ -f requirements.txt ]; then pip install -r requirements.txt; fi && "
            f"pip install --upgrade matrice && ",
        ]
        return " ".join(filter(None, cmd_parts))

    def get_hugging_face_token(self, model_key):
        """Get Hugging Face token for specific model keys."""
        hugging_face_token = ""
        if model_key and (
            model_key.startswith("microsoft") or model_key.startswith("timm")
        ):
            secret_name = "hugging_face"
            resp, error, message = self.scaling.get_model_secret_keys(secret_name)
            if error is not None:
                logging.error(f"Error getting Hugging Face token: {message}")
            else:
                hugging_face_token = resp["user_access_token"]
        return hugging_face_token

    def get_internal_api_key(self, action_id):
        """Get internal API key for action."""
        internal_api_key = ""
        resp, error, message = self.scaling.get_internal_api_key(action_id)
        if error is not None:
            logging.error(f"Error getting internal api key: {message}")
        else:
            internal_api_key = resp["internal_api_key"]
        return internal_api_key

    def setup_action_requirements(
        self, action_details, work_fs="", model_family="", action_id=""
    ):
        """Setup action requirements."""
        if model_family:
            model_codebase_url, error, message = self.scaling.get_model_codebase(
                model_family
            )
            model_codebase_requirements_url, error, message = (
                self.scaling.get_model_codebase_requirements(model_family)
            )
            setup_workspace_and_run_task(
                work_fs, action_id, model_codebase_url, model_codebase_requirements_url
            )

        # Docker hub login
        try:
            creds, error, message = self.scaling.get_docker_hub_credentials()
            if error:
                raise Exception(f"Failed to get Docker credentials: {message}")

            username = creds["username"]
            password = creds["password"]
            login_cmd = (
                f"docker login -u {shlex.quote(username)} -p {shlex.quote(password)}"
            )
            subprocess.run(login_cmd, shell=True, check=True)
        except Exception as e:
            logging.error(f"Docker login failed: {str(e)}")
            raise

        # Get user credentials
        try:
            user_access_key_pair, error, message = (
                self.scaling.get_user_access_key_pair(action_details["_idUser"])
            )
            if error:
                raise Exception(f"Failed to get user access key pair: {message}")

            access_key = user_access_key_pair["access_key"]
            secret_key = user_access_key_pair["secret_key"]
            self.matrice_access_key_id, self.matrice_secret_access_key = (
                get_decrypted_access_key_pair(access_key, secret_key)
            )
        except Exception as e:
            logging.error(f"Failed to setup credentials: {str(e)}")
            raise

    def send_logs_continuously(self):
        """Continuously read and send logs from the log file to the scaling service."""
        last_position = 0
        while not self.stop_thread and os.path.exists(self.log_path):
            try:
                with open(self.log_path, "rb") as log_file:
                    log_file.seek(last_position)
                    new_content = log_file.read()

                    if new_content:
                        decoded_content = new_content.decode("utf-8", errors="replace")
                        self._send_logs_to_scaling(decoded_content)
                        self._check_cuda(decoded_content)

                    last_position = log_file.tell()

            except IOError as e:
                logging.error("Error reading log file: %s", e)
            except Exception as e:
                logging.exception("Unexpected error in send_logs_continuously: %s", e)

            time.sleep(30)

    def _send_logs_to_scaling(self, log_content):
        """Send logs to the scaling service."""
        try:
            _, error, message = self.scaling.update_action_docker_logs(
                action_record_id=self.action_record_id, log_content=log_content
            )
            if error:
                logging.error("Error from update_action_docker_logs: %s", error)
        except Exception as e:
            logging.exception("Exception in update_action_docker_logs: %s", e)

    def _check_cuda(self, log_content):
        """Check for CUDA out of memory errors in logs and update action status."""
        try:
            if "CUDA error: out of memory" in log_content:
                action_details = self.get_action_details()
                if not action_details:
                    return

                self.scaling.update_action(
                    id=self.action_record_id,
                    step_code="ERROR",
                    action_type=action_details["action"],
                    status="ERROR",
                    status_description="CUDA error: out of memory",
                    service="bg-job-scheduler",
                    job_params=action_details["jobParams"],
                )
        except Exception as e:
            logging.exception("Error in _check_cuda: %s", e)

    def start_process(self, cmd, log_name):
        """Start the process and initialize logging."""
        self.cmd = cmd
        self.log_path = f"{self.get_log_path()}/{log_name}_{self.action_record_id}.txt"

        try:
            with open(self.log_path, "wb") as out:
                self.process = subprocess.Popen(
                    shlex.split(self.cmd),
                    stdout=out,
                    stderr=out,
                    env={**os.environ},
                    start_new_session=True,
                )
        except Exception as e:
            logging.error(f"Failed to start process: {str(e)}")
            raise

    def start(self, cmd, log_name):
        """Start the process and log monitoring thread."""
        self.start_process(cmd, log_name)
        self.log_thread = threading.Thread(
            target=self.send_logs_continuously, daemon=True
        )
        self.log_thread.start()

    def stop(self):
        """Stop the process and log monitoring thread."""
        try:
            self.stop_thread = True
            if self.process:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.process.wait(timeout=30)
            if self.log_thread and self.log_thread.is_alive():
                self.log_thread.join(timeout=30)
        except Exception as e:
            logging.error(f"Error stopping process: {str(e)}")
            # Force kill if graceful shutdown fails
            if self.process:
                self.process.kill()

    def execute(self):
        """Execute the task."""
        self.task(self)


def data_preparation_execute(self: ActionInstance):
    """Execute data preparation task."""
    work_fs = get_max_file_system()

    action_details = self.get_action_details()
    if not action_details:
        return

    self.setup_action_requirements(action_details, work_fs, model_family="")

    # Update action status
    action = {
        "jobParams": action_details["jobParams"],
    }
    dataset_id_version = (
        action_details["jobParams"]["dataset_id"]
        + action_details["jobParams"]["dataset_version"]
    )

    action["jobParams"].update(
        {
            "dataset_host_path_map": {dataset_id_version: f"{work_fs}/workspace"},
            "dataset_local_path_map": {dataset_id_version: "/usr/src/app/workspace"},
            "host_file_system": work_fs,
        }
    )

    self.scaling.update_action(
        id=self.action_record_id,
        step_code="DCK_LNCH",
        action_type=action_details["action"],
        status=action_details["status"],
        sub_action=action_details["subAction"],
        status_description="Job is assigned to docker",
        service="bg-job-scheduler",
        job_params=action["jobParams"],
    )

    # Pull model training docker if specified
    if action["jobParams"].get("model_train_docker"):
        logging.info("Pulling the docker image")
        pull_cmd = f"docker pull {action['jobParams']['model_train_docker']}"
        process = subprocess.Popen(
            pull_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        logging.info(f"Started pulling Docker image with PID: {process.pid}")

    # Build and execute docker command
    cmd = (
        f"{self.get_base_docker_cmd(work_fs, destination_workspace_path='/usr/src/app/workspace', docker_workdir='/usr/src/app/workspace')} "
        f'python3 /usr/src/app/data_preparation.py {self.action_record_id} "'
    )
    logging.info(f"cmd is: {cmd}")
    self.start(cmd, "data_preparation_log")


def data_processing_execute(self: ActionInstance):
    """Execute data processing task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return

    self.setup_action_requirements(action_details, work_fs, model_family="")

    # Update action status
    action = {"jobParams": action_details["jobParams"]}
    action["jobParams"].update(
        {
            "dp_dv_host_paths": [f"{work_fs}/workspace"],
            "dp_dv_local_paths": ["/usr/src/app/workspace"],
        }
    )

    self.scaling.update_action(
        id=self.action_record_id,
        step_code="DCK_LNCH",
        action_type=action_details["action"],
        status="ACK",
        status_description="Job is assigned to docker",
        service="bg-job-scheduler",
        job_params=action["jobParams"],
    )

    # Build and execute docker command
    cmd = (
        f"{self.get_base_docker_cmd(work_fs)} "
        f'python3 /usr/src/app/main.py {self.action_record_id} "'
    )
    logging.info(f"cmd: {cmd}")
    self.start(cmd, "data_processing_log")


def data_split_execute(self: ActionInstance):
    """Execute data split task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return

    self.setup_action_requirements(action_details, work_fs, model_family="")

    cmd = (
        f"{self.get_base_docker_cmd(work_fs)} "
        f'python3 /usr/src/app/data_split.py {self.action_record_id} "'
    )
    logging.info(f"cmd: {cmd}")
    self.start(cmd, "data_split")


def dataset_annotation_execute(self: ActionInstance):
    """Execute dataset annotation task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return

    self.setup_action_requirements(action_details, work_fs)

    cmd = (
        f"{self.get_base_docker_cmd(work_fs)} "
        f'python3 /usr/src/app/dataset_annotation.py {self.action_record_id} "'
    )
    logging.info(f"cmd: {cmd}")
    self.start(cmd, "dataset_annotation")


def model_deploy_execute(self: ActionInstance):
    """Execute model deployment task."""
    self.port = int(self.scaling.get_open_port())
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return

    action_id = action_details["_id"]
    model_family = action_details["actionDetails"]["modelFamily"]
    self.setup_action_requirements(
        action_details, work_fs, model_family=model_family, action_id=action_id
    )

    use_gpu = self.get_gpu_config(action_details)
    cmd = (
        f"{self.get_base_docker_cmd(work_fs, use_gpu, mount_docker_sock=True, action_id=action_id, port=self.port)} "
        f'python3 deploy.py {self.action_record_id} {self.port}"'
    )
    logging.info(f"cmd is: {cmd}")
    self.start(cmd, "deploy_log")


def model_train_execute(self: ActionInstance):
    """Execute model training task."""
    action_details = self.get_action_details()
    if not action_details:
        return

    action_id = action_details["_id"]
    use_gpu = self.get_gpu_config(action_details)
    work_fs = action_details["jobParams"]["host_file_system"]
    model_key = action_details["actionDetails"]["modelKey"]
    model_family = action_details["actionDetails"]["modelFamily"]

    self.setup_action_requirements(
        action_details, work_fs, model_family=model_family, action_id=action_id
    )

    cmd = (
        f"{self.get_base_docker_cmd(work_fs, use_gpu, action_id=action_id, model_key=model_key)} "
        f'python3 train.py {self.action_record_id} "'
    )
    logging.info(f"cmd is: {cmd}")
    self.start(cmd, "train_log")


def model_eval_execute(self: ActionInstance):
    """Execute model evaluation task."""
    action_details = self.get_action_details()
    if not action_details:
        return

    action_id = action_details["_id"]
    work_fs = action_details["jobParams"]["host_file_system"]
    model_family = action_details["actionDetails"]["modelFamily"]
    use_gpu = self.get_gpu_config(action_details)

    self.setup_action_requirements(
        action_details, work_fs, model_family=model_family, action_id=action_id
    )

    cmd = (
        f"{self.get_base_docker_cmd(work_fs, use_gpu, action_id=action_id)} "
        f'python3 eval.py {self.action_record_id} "'
    )
    logging.info(f"cmd is: {cmd}")
    self.start(cmd, "eval_log")


def model_export_execute(self: ActionInstance):
    """Execute model export task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return

    action_id = action_details["_id"]
    if "host_file_system" in action_details["jobParams"]:
        work_fs = action_details["jobParams"]["host_file_system"]
        logging.info("host_file_system: %s", work_fs)

    use_gpu = self.get_gpu_config(action_details)
    model_family = action_details["actionDetails"]["modelFamily"]
    self.setup_action_requirements(
        action_details, work_fs, model_family=model_family, action_id=action_id
    )

    cmd = (
        f"{self.get_base_docker_cmd(work_fs, use_gpu, action_id=action_id)} "
        f'python3 export.py {self.action_record_id} "'
    )
    logging.info(f"cmd is: {cmd}")
    self.start(cmd, "export_log")


def image_build_execute(self: ActionInstance):
    """Execute image building task."""
    action_details = self.get_action_details()
    if not action_details:
        return

    self.setup_action_requirements(action_details)

    model_family_id = action_details["_idService"]
    action_id = action_details["_id"]
    internal_api_key = self.get_internal_api_key(action_id)

    cmd = (
        f"{self.get_base_docker_cmd(mount_docker_sock=True, internal_api_key=internal_api_key)} "
        f'python3 main.py {model_family_id} {action_id}"'
    )
    logging.info(f"cmd is: {cmd}")
    self.start(cmd, "image_build_log")


def resource_clone_execute(self: ActionInstance):
    """Execute resource clone task."""
    action_details = self.get_action_details()
    if not action_details:
        return

    self.setup_action_requirements(action_details)

    cmd = (
        f"{self.get_base_docker_cmd()} "
        f'python3 main.py {self.action_record_id} "'
    )
    logging.info(f"cmd is: {cmd}")
    self.start(cmd, "resource_clone")
