import os
import logging
from matrice.compute_manager.instance_utils import check_public_port_exposure


class Scaling:
    """This is a private class used internally."""

    def __init__(self, session, instance_id=None):
        if not instance_id:
            logging.error(
                "Instance id not set for this instance. Cannot perform the operation for job-scheduler without instance id"
            )
            raise Exception(
                "Instance id not set for this instance. Cannot perform the operation for job-scheduler without instance id"
            )
        self.instance_id = instance_id
        self.session = session
        self.rpc = session.rpc
        self.USED_PORTS = set()
        logging.info(f"Initialized Scaling with instance_id: {instance_id}")

    def handle_response(self, resp, success_message, error_message):
        """Helper function to handle API response"""
        if resp.get("success"):
            data = resp.get("data", None)
            error = None
            message = success_message
            logging.info(message)
        else:
            data = resp.get("data", None)
            error = resp.get("message", None)
            message = error_message
            logging.error(f"{message}: {error}")

        return data, error, message

    def get_downscaled_ids(self):
        logging.info(f"Getting downscaled ids for instance {self.instance_id}")
        path = f"/v1/scaling/down_scaled_ids/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Downscaled ids info fetched successfully",
            "Could not fetch the Downscaled ids info",
        )

    def stop_instance(self):
        logging.info(f"Stopping instance {self.instance_id}")
        path = "/v1/scaling/compute_instance/stop"
        resp = self.rpc.put(
            path=path, payload={"_idInstance": self.instance_id, "isForcedStop": False}
        )
        return self.handle_response(
            resp, "Instance stopped successfully", "Could not stop the instance"
        )

    def update_action_status(
        self,
        service_provider="",
        action_record_id="",
        isRunning=True,
        status="",
        docker_start_time=None,
        action_duration=0,
        cpuUtilisation=0.0,
        gpuUtilisation=0.0,
        memoryUtilisation=0.0,
        gpuMemoryUsed=0,
        createdAt=None,
        updatedAt=None,
    ):
        logging.info(f"Updating action status for action {action_record_id}")
        path = "/v1/scaling/update_action_status"
        payload_scaling = {
            "instanceID": self.instance_id,
            "serviceProvider": service_provider,
            "actionRecordId": action_record_id,
            "isRunning": isRunning,
            "status": status,
            "dockerContainerStartTime": docker_start_time,
            "cpuUtilisation": cpuUtilisation,
            "gpuUtilisation": gpuUtilisation,
            "memoryUtilisation": memoryUtilisation,
            "gpuMemoryUsed": gpuMemoryUsed,
            "actionDuration": action_duration,
            "createdAt": createdAt,
            "updatedAt": updatedAt,
        }
        resp = self.rpc.put(path=path, payload=payload_scaling)
        return self.handle_response(
            resp,
            "Action status details updated successfully",
            "Could not update the action status details ",
        )

    def update_status(
        self,
        action_record_id,
        action_type,
        service_name,
        stepCode,
        status,
        status_description,
    ):
        logging.info(f"Updating status for action {action_record_id}")
        url = "/v1/project/action"

        payload = {
            "_id": action_record_id,
            "action": action_type,
            "serviceName": service_name,
            "stepCode": stepCode,
            "status": status,
            "statusDescription": status_description,
        }

        self.rpc.put(path=url, payload=payload)

    def get_shutdown_details(self):
        logging.info(f"Getting shutdown details for instance {self.instance_id}")
        path = f"/v1/scaling/get_shutdown_details/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Shutdown info fetched successfully",
            "Could not fetch the shutdown details",
        )

    def get_tasks_details(self):
        logging.info(f"Getting tasks details for instance {self.instance_id}")
        path = f"/v1/project/action/instance/{self.instance_id}/action_details"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Task details fetched successfully",
            "Could not fetch the task details",
        )

    def get_action_details(self, action_status_id):
        logging.info(f"Getting action details for action {action_status_id}")
        path = f"/v1/project/action/{action_status_id}/details"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Task details fetched successfully",
            "Could not fetch the task details",
        )

    def update_action(
        self,
        id="",
        step_code="",
        action_type="",
        status="",
        sub_action="",
        status_description="",
        service="",
        job_params={},
    ):
        logging.info(f"Updating action {id}")
        path = "/v1/project/action"
        payload = {
            "_id": id,
            "stepCode": step_code,
            "action": action_type,
            "status": status,
            "subAction": sub_action,
            "statusDescription": status_description,
            "serviceName": service,
            "jobParams": job_params,
        }
        resp = self.rpc.put(path=path, payload=payload)
        return self.handle_response(
            resp, "Error logged successfully", "Could not log the errors"
        )

    def assign_jobs(self, is_gpu):
        logging.info(f"Assigning jobs for instance {self.instance_id} (GPU: {is_gpu})")
        path = f"/v1/scaling/assign_jobs/{str(is_gpu)}/{self.instance_id}"

        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp, "Pinged successfully", "Could not ping the scaling jobs"
        )

    def update_available_resources(
        self,
        availableCPU=0,
        availableGPU=0,
        availableMemory=0,
        availableGPUMemory=0,
    ):
        logging.info(f"Updating available resources for instance {self.instance_id}")
        path = f"/v1/scaling/update_available_resources/{self.instance_id}"
        payload = {
            "availableMemory": availableMemory,
            "availableCPU": availableCPU,
            "availableGPUMemory": availableGPUMemory,
            "availableGPU": availableGPU,
        }
        resp = self.rpc.put(path=path, payload=payload)
        return self.handle_response(
            resp, "Resources updated successfully", "Could not update the resources"
        )

    def update_action_docker_logs(self, action_record_id, log_content):
        logging.info(f"Updating docker logs for action {action_record_id}")
        path = "/v1/project/update_action_docker_logs"
        payload = {"actionRecordId": action_record_id, "logContent": log_content}
        resp = self.rpc.put(path=path, payload=payload)
        return self.handle_response(
            resp, "Docker logs updated successfully", "Could not update the docker logs"
        )

    def get_docker_hub_credentials(self):
        logging.info("Getting docker credentials")
        path = "/v1/scaling/get_docker_hub_credentials"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Docker credentials fetched successfully",
            "Could not fetch the docker credentials",
        )

    def get_open_ports_config(self):
        path = f"/v1/scaling/get_open_ports/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Open ports config fetched successfully", 
            "Could not fetch the open ports config"
        )

    def get_open_port(self):
        port_range = {"from": 8200, "to": 9000}  # Default fallback range
        try:
            resp, err, msg = self.get_open_ports_config()
            if not err and resp and resp[0]:
                port_range = resp[0]
            else:
                logging.warning(
                    "Using default port range 8200-9000 due to config fetch error"
                )
        except Exception as e:
            logging.warning(
                f"Using default port range 8200-9000. Config fetch failed: {str(e)}"
            )

        min_port = port_range["from"]
        max_port = port_range["to"]

        for port in range(min_port, max_port):
            if port in self.USED_PORTS:
                continue
            # if not check_public_port_exposure(port):
            #     logging.warning(f"Port {port} is not publicly accessible")
            #     continue
            self.USED_PORTS.add(port)
            logging.info(f"Found available port: {port}")
            return port
        logging.error(f"No available ports found in range {min_port}-{max_port}")
        return None

    def get_data_processing_image(self):
        logging.info("Getting data processing image")
        return f"285699223019.dkr.ecr.us-west-2.amazonaws.com/{os.environ.get('ENV')}-data-processing:latest"  # TODO: Get from API

    def get_model_secret_keys(self, secret_name):
        path = f"/v1/scaling/get_models_secret_keys?secret_name={secret_name}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Secret keys fetched successfully",
            "Could not fetch the secret keys",
        )

    def get_model_codebase(self, model_family_id):
        path = f"/v1/model_store/get_user_code_download_path/{model_family_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Codebase fetched successfully",
            "Could not fetch the codebase",
        )

    def get_model_codebase_requirements(self, model_family_id):
        path = f"/v1/model_store/get_user_requirements_download_path/{model_family_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Codebase requirements fetched successfully",
            "Could not fetch the codebase requirements",
        )

    def get_model_codebase_script(self, model_family_id):
        path = f"/v1/model_store/get_user_script_download_path/:{model_family_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Codebase script fetched successfully",
            "Could not fetch the codebase script",
        )

    def add_account_compute_instance(
        self,
        account_number,
        alias,
        service_provider,
        instance_type,
        shut_down_time,
        lease_type,
        launch_duration,
    ):
        path = "/v1/scaling/add_account_compute_instance"
        payload = {
            "accountNumber": account_number,
            "alias": alias,
            "serviceProvider": service_provider,
            "instanceType": instance_type,
            "shutDownTime": shut_down_time,
            "leaseType": lease_type,
            "launchDuration": launch_duration,
        }
        resp = self.rpc.post(path=path, payload=payload)
        return self.handle_response(
            resp,
            "Compute instance added successfully",
            "Could not add the compute instance",
        )

    def stop_account_compute(self, account_number, alias):
        path = f"/v1/scaling/stop_account_compute/{account_number}/{alias}"
        resp = self.rpc.put(path=path)
        return self.handle_response(
            resp,
            "Compute instance stopped successfully",
            "Could not stop the compute instance",
        )

    def restart_account_compute(self, account_number, alias):
        path = f"/v1/scaling/restart_account_compute/{account_number}/{alias}"
        resp = self.rpc.put(path=path)
        return self.handle_response(
            resp,
            "Compute instance restarted successfully",
            "Could not restart the compute instance",
        )

    def delete_account_compute(self, account_number, alias):
        path = f"/v1/scaling/delete_account_compute/{account_number}/{alias}"
        resp = self.rpc.delete(path=path)
        return self.handle_response(
            resp,
            "Compute instance deleted successfully",
            "Could not delete the compute instance",
        )

    def get_all_instances_type(self):
        path = "/v1/scaling/get_all_instances_type"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "All instance types fetched successfully",
            "Could not fetch the instance types",
        )

    def get_compute_details(self):
        path = f"/v1/scaling/get_compute_details/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Compute details fetched successfully",
            "Could not fetch the compute details",
        )

    def get_user_access_key_pair(self, user_id):
        path = f"/v1/scaling/get_user_access_key_pair/{user_id}/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "User access key pair fetched successfully",
            "Could not fetch the user access key pair",
        )

    def get_internal_api_key(self, action_id):
        path = f"/v1/scaling/get_internal_api_key/{action_id}/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "internal keys fetched successfully",
            "Could not fetch internal keys",
        )
