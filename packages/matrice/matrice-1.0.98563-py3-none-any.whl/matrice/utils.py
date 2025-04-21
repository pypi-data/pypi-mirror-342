"""Utility functions for the Matrice package."""

import os
import traceback
import subprocess
import logging
from matrice.rpc import RPC


def log_error(
    filename,
    function_name,
    error_message,
    action_record_id="",
):
    """Log error to the BE system.

    Args:
        filename (str): Name of the file where error occurred
        function_name (str): Name of the function where error occurred
        error_message (str): Error message to log
        action_record_id (str, optional): ID of the action record. Defaults to "".
    """
    traceback_str = traceback.format_exc().rstrip()
    log_err = {
        "serviceName": "Python-Sdk",
        "stackTrace": traceback_str,
        "errorType": "Internal",
        "description": error_message,
        "fileName": filename,
        "functionName": function_name,
        "moreInfo": {},
    }
    if action_record_id:
        log_err["actionRecordID"] = action_record_id
    error_logging_route = "/v1/system/log_error"
    try:
        rpc_client = RPC(
            secret_key=os.environ.get("MATRICE_SECRET_ACCESS_KEY"),
            access_key=os.environ.get("MATRICE_ACCESS_KEY_ID"),
        )
        rpc_client.post(
            path=error_logging_route,
            payload=log_err,
        )
    except Exception as exc:
        print(f"Failed to log error: {exc}")
    print(f"An exception occurred. Logging the exception information: {log_err}")


def handle_response(response, success_message, failure_message):
    """Handle API response and return appropriate result.

    Args:
        response (dict): API response
        success_message (str): Message to return on success
        failure_message (str): Message to return on failure

    Returns:
        tuple: (result, error, message)
    """
    if response.get("success"):
        result = response.get("data")
        error = None
        message = success_message
    else:
        result = None
        error = response.get("message")
        message = failure_message
    return result, error, message


def check_for_duplicate(session, service, name):
    """Check if an item with the given name already exists for the specified service.

    Args:
        session: Session object containing RPC client
        service (str): The name of the service to check (e.g., 'dataset', 'annotation')
        name (str): The name of the item to check for duplication

    Returns:
        tuple: (API response, error_message, status_message)

    Example:
        >>> resp, err, msg = check_for_duplicate('dataset', 'MyDataset')
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Duplicate check result: {resp}")
    """
    service_config = {
        "dataset": {
            "path": f"/v1/dataset/check_for_duplicate?datasetName={name}",
            "item_name": "Dataset",
        },
        "annotation": {
            "path": f"/v1/annotations/check_for_duplicate?annotationName={name}",
            "item_name": "Annotation",
        },
        "model_export": {
            "path": f"/v1/model/model_export/check_for_duplicate?modelExportName={name}",
            "item_name": "Model export",
        },
        "model": {
            "path": f"/v1/model/model_train/check_for_duplicate?modelTrainName={name}",
            "item_name": "Model Train",
        },
        "projects": {
            "path": f"/v1/project/check_for_duplicate?name={name}",
            "item_name": "Project",
        },
        "deployment": {
            "path": f"/v1/deployment/check_for_duplicate?deploymentName={name}",
            "item_name": "Deployment",
        },
    }
    if service not in service_config:
        return (
            None,
            f"Invalid service: {service}",
            "Service not supported",
        )
    config = service_config[service]
    resp = session.rpc.get(path=config["path"])
    if resp.get("success"):
        if resp.get("data") == "true":
            return handle_response(
                resp,
                f"{config['item_name']} with this name already exists",
                f"Could not check for this {service} name",
            )
        return handle_response(
            resp,
            f"{config['item_name']} with this name does not exist",
            f"Could not check for this {service} name",
        )
    return handle_response(
        resp,
        "",
        f"Could not check for this {service} name",
    )


def get_summary(session, project_id, service_name):
    """Fetch a summary of the specified service in the project.

    Args:
        session: Session object containing RPC client
        project_id (str): The project ID
        service_name (str): Service to fetch summary for ('annotations', 'models', etc)

    Returns:
        tuple: (summary_data, error_message)

    Example:
        >>> summary, error = get_summary(rpc, project_id, 'models')
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Summary: {summary}")
    """
    service_paths = {
        "annotations": "/v1/annotations/summary",
        "models": "/v1/model/summary",
        "exports": "/v1/model/summaryExported",
        "deployments": "/v1/deployment/summary",
    }
    success_messages = {
        "annotations": "Annotation summary fetched successfully",
        "models": "Model summary fetched successfully",
        "exports": "Model Export Summary fetched successfully",
        "deployments": "Deployment summary fetched successfully",
    }
    error_messages = {
        "annotations": "Could not fetch annotation summary",
        "models": "Could not fetch models summary",
        "exports": "Could not fetch models export summary",
        "deployments": "An error occurred while trying to fetch deployment summary.",
    }
    if service_name not in service_paths:
        return (
            None,
            f"Invalid service name: {service_name}",
        )
    path = f"{service_paths[service_name]}?projectId={project_id}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        error_messages[service_name],
        success_messages[service_name],
    )


def dependencies_check(package_names):
    """Check and install required dependencies.

    Args:
        package_names (str or list): Package name(s) to check/install

    Raises:
        Exception: If package installation fails
    """
    if not isinstance(package_names, list):
        package_names = [package_names]
    for package_name in package_names:
        try:
            subprocess.run(
                ["pip", "install", package_name],
                check=True,
            )
            logging.info(
                "Successfully installed %s",
                package_name,
            )
        except subprocess.CalledProcessError as exc:
            logging.error(
                "Failed to install %s: %s",
                package_name,
                exc,
            )
            raise Exception(f"Failed to install {package_name}") from exc
