import shlex
import subprocess
import os

def setup_workspace_and_run_task(work_fs, action_id, model_codebase_url, model_codebase_requirements_url):

    # Define the paths
    workspace_dir = f"{work_fs}/{action_id}"
    codebase_zip_path = f"{workspace_dir}/file.zip"
    requirements_txt_path = f"{workspace_dir}/requirements.txt"

    # if workspace directory already exists do not anything
    if os.path.exists(workspace_dir):
        return

    # Ensure the workspace directory exists
    os.makedirs(workspace_dir, exist_ok=True)

    # Download the codebase
    download_codebase_cmd = (
        f'curl -L -o {shlex.quote(codebase_zip_path)} {shlex.quote(model_codebase_url)}'
    )
    subprocess.run(download_codebase_cmd, shell=True, check=True)

    # Unzip the codebase
    unzip_codebase_cmd = (
        f'unzip -o {shlex.quote(codebase_zip_path)} -d {shlex.quote(workspace_dir)}'
    )
    subprocess.run(unzip_codebase_cmd, shell=True, check=True)

    # Move files from the unzipped folder to the workspace directory
    move_files_cmd = (
        f'rsync -av {shlex.quote(workspace_dir)}/*/ {shlex.quote(workspace_dir)}/ '
    )
    subprocess.run(move_files_cmd, shell=True, check=True)

    # Download the requirements if the URL is provided
    if model_codebase_requirements_url:
        download_requirements_cmd = (
            f'curl -L -o {shlex.quote(requirements_txt_path)} {shlex.quote(model_codebase_requirements_url)}'
        )
        subprocess.run(download_requirements_cmd, shell=True, check=True)