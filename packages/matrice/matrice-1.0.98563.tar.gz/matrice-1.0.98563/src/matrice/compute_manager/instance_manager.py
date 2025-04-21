import os
import time
import json
import logging
import threading

from matrice.session import Session
from matrice.compute_manager.scaling import Scaling

from matrice.compute_manager.actions_manager import ActionsManager
from matrice.compute_manager.shutdown_manager import ShutdownManager
from matrice.compute_manager.actions_scaledown_manager import ActionsScaleDownManager
from matrice.compute_manager.resources_tracker import (
    MachineResourcesTracker,
    ActionsResourcesTracker,
)
from matrice.compute_manager.instance_utils import (
    get_instance_info,
    get_decrypted_access_key_pair,
)


class InstanceManager:
    """
    Class for managing actions.
    """

    def __init__(
        self,
        matrice_access_key_id="",
        matrice_secret_access_key="",
        encryption_key="",
        instance_id="",
        service_provider="",
        env="",
        gpus="",
        workspace_dir="matrice_workspace",
    ):
        """Initialize a instance manager.

        Args:
            matrice_access_key_id (str, optional): Access key ID for Matrice authentication. Defaults to "".
            matrice_secret_access_key (str, optional): Secret access key for Matrice authentication. Defaults to "".
            encryption_key (str, optional): Key used for encrypting sensitive data. Defaults to "".
            instance_id (str, optional): Unique identifier for this compute instance. Defaults to "".
            service_provider (str, optional): Cloud service provider being used. Defaults to "".
            env (str, optional): Environment name (e.g. dev, prod). Defaults to "".
            gpus (str, optional): GPU configuration string (e.g. "0,1"). Defaults to "".
            workspace_dir (str, optional): Directory for workspace files. Defaults to "matrice_workspace".
        """
        self.session = self.setup_env_credentials(
            env,
            service_provider,
            instance_id,
            encryption_key,
            matrice_access_key_id,
            matrice_secret_access_key,
        )
        os.environ["WORKSPACE_DIR"] = str(workspace_dir)
        os.environ["GPUS"] = json.dumps(gpus)
        self.scaling = Scaling(self.session, os.environ.get("INSTANCE_ID"))
        logging.info("InstanceManager initialized with scaling")
        self.current_actions = {}
        self.actions_manager = ActionsManager(self.scaling)
        logging.info("InstanceManager initialized with actions manager")
        self.scale_down_manager = ActionsScaleDownManager(self.scaling)
        logging.info("InstanceManager initialized with scale down manager")
        self.shutdown_manager = ShutdownManager(self.scaling)
        logging.info("InstanceManager initialized with shutdown manager")
        self.machine_resources_tracker = MachineResourcesTracker(self.scaling)
        logging.info("InstanceManager initialized with machine resources tracker")
        self.actions_resources_tracker = ActionsResourcesTracker(self.scaling)
        logging.info("InstanceManager initialized with actions resources tracker")
        self.poll_interval = 10
        logging.info("InstanceManager initialized.")

    def setup_env_credentials(
        self,
        env,
        service_provider,
        instance_id,
        encryption_key,
        matrice_access_key_id,
        matrice_secret_access_key,
    ):
        """
        Setup environment credentials
        """
        try:
            auto_service_provider, auto_instance_id = get_instance_info()
        except Exception as e:
            logging.error(f"Error getting instance info: {str(e)}")

        manual_instance_info = {
            "ENV": env or os.environ.get("ENV"),
            "SERVICE_PROVIDER": service_provider
            or os.environ.get("SERVICE_PROVIDER")
            or auto_service_provider,
            "INSTANCE_ID": instance_id
            or os.environ.get("INSTANCE_ID")
            or auto_instance_id,
            "MATRICE_ENCRYPTION_KEY": encryption_key
            or os.environ.get("MATRICE_ENCRYPTION_KEY"),
            "MATRICE_ACCESS_KEY_ID": matrice_access_key_id
            or os.environ.get("MATRICE_ACCESS_KEY_ID"),
            "MATRICE_SECRET_ACCESS_KEY": matrice_secret_access_key
            or os.environ.get("MATRICE_SECRET_ACCESS_KEY"),
        }
        for key, value in manual_instance_info.items():
            os.environ[key] = value

        if not (os.environ.get("SERVICE_PROVIDER") and os.environ.get("INSTANCE_ID")):
            raise Exception(
                "SERVICE_PROVIDER and INSTANCE_ID must be set as environment variables or passed as arguments"
            )

        self.encryption_key = manual_instance_info["MATRICE_ENCRYPTION_KEY"]
        access_key, secret_key = self.decrypt_access_key_pair(
            manual_instance_info["MATRICE_ACCESS_KEY_ID"],
            manual_instance_info["MATRICE_SECRET_ACCESS_KEY"],
            self.encryption_key,
        )
        os.environ["MATRICE_SECRET_ACCESS_KEY"] = secret_key
        os.environ["MATRICE_ACCESS_KEY_ID"] = access_key
        os.environ["MATRICE_ENCRYPTION_KEY"] = self.encryption_key

        return Session(
            account_number="",
            secret_key=secret_key,
            access_key=access_key,
        )

    def decrypt_access_key_pair(
        self, enc_access_key, enc_secret_key, encryption_key=""
    ):
        """
        Decrypt the access key pair
        """
        return get_decrypted_access_key_pair(
            enc_access_key, enc_secret_key, encryption_key
        )

    def start_instance_manager(self):
        """
        Instance manager loop.
        """
        while True:
            try:
                self.shutdown_manager.handle_shutdown(
                    bool(self.actions_manager.get_current_actions())
                )
                self.scale_down_manager.auto_scaledown_actions()
                self.machine_resources_tracker.update_available_resources()
                self.actions_resources_tracker.update_actions_resources()
            except Exception as e:
                logging.error(f"Error in actions manager loop: {str(e)}")
            time.sleep(self.poll_interval)

    def start(self):
        """
        Start the instance manager.
        """
        instance_manager_thread = threading.Thread(
            target=self.start_instance_manager
        ).start()
        actions_manager_thread = threading.Thread(
            target=self.actions_manager.start_actions_manager
        ).start()
        return instance_manager_thread, actions_manager_thread
