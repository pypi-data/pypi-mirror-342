import logging
import time
import os
import sys
from matrice.utils import log_error
from matrice.compute_manager.scaling import Scaling

class ShutdownManager:
    """
    Class for managing shutdown.
    """
    def __init__(self, scaling: Scaling):
        self.scaling = scaling
        self._load_shutdown_configuration()
        self.last_no_queued_time = None

    def _load_shutdown_configuration(self):
        """
        Load configuration from AWS secrets and initialize parameters.
        """
        response, error, message = self.scaling.get_shutdown_details()
        if error is None:
            self.shutdown_threshold = response["shutdownThreshold"]
            self.launch_duration = response["launchDuration"]
            self.instance_source = response["instanceSource"]
            self.encryption_key = response.get("encryptionKey", None)
        else:
            self.shutdown_threshold = 500
            self.instance_source = "auto"
            self.launch_duration = 1
            self.source_stop_instance = True
            logging.error("Failed to get shutdown details: %s", message)

        self.reserved_instance = self.instance_source == "reserved"

    def do_cleanup_and_shutdown(self):
        """
        Function to clean up and shut down
        """
        try:
            self.scaling.stop_instance()
        except Exception as err:
            log_error("instance_utils.py", "do_cleanup_and_shutdown", err)
        try:
            if os.environ["SERVICE_PROVIDER"] != "":
                os.system("shutdown now")
                sys.exit(0)
        except Exception as err:
            log_error("instance_utils.py", "do_cleanup_and_shutdown", err)
        sys.exit(1)

    def handle_shutdown(self, tasks_running):
        """
        Check idle time and trigger shutdown if threshold is exceeded.
        """
        if tasks_running:
            self.last_no_queued_time = None
        elif self.last_no_queued_time is None:
            self.last_no_queued_time = time.time()

        if self.last_no_queued_time is not None:
            elapsed_time = time.time() - self.last_no_queued_time
            if elapsed_time > self.shutdown_threshold and not self.reserved_instance:
                logging.info(
                    f"Idle time {elapsed_time} exceeded threshold {self.shutdown_threshold}. Shutting down."
                )
                self.do_cleanup_and_shutdown()
            else:
                logging.info(
                    f"Time since last action: {elapsed_time}. Time left to shutdown: {self.shutdown_threshold - elapsed_time}."
                )