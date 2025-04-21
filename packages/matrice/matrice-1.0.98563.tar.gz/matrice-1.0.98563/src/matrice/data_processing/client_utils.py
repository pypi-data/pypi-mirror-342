"""Module providing client_utils functionality."""

import os
import logging
import requests
import zipfile

MAX_PARTITION_SIZE_BYTES = 2 * 1024 * 1024 * 1024
ANNOTATION_EXTENSIONS = [
    ".json",
    ".txt",
    ".xml",
    ".ndjson",
    ".yaml",
    ".csv",
    ".ini",
]
SAMPLES_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".ti",
    ".webp",
    ".mp4",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".mkv",
    ".webm",
]
COMPRESSED_EXTENSIONS = [
    ".zip",
    ".tar",
    ".tar.gz",
    ".tar.bz2",
    ".tar.xz",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
]
ANNOTATION_PARTITION_TYPE = "annotation"
SAMPLES_PARTITION_TYPE = "samples"


def get_size_mb(path):
    """Calculate total size in MB for a file, folder, or list of paths."""
    total_size = 0

    def get_file_size(file_path):
        if os.path.isfile(file_path) and not os.path.islink(file_path):
            return os.path.getsize(file_path)
        return 0

    def get_folder_size(folder_path):
        size = 0
        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                size += get_file_size(os.path.join(dirpath, filename))
        return size

    if isinstance(path, (list, tuple)):
        for p in path:
            total_size += get_file_size(p) if os.path.isfile(p) else get_folder_size(p)
    else:
        total_size += get_file_size(path) if os.path.isfile(path) else get_folder_size(path)
    return -(-total_size // (1024 * 1024))


def rename_mot_file(file_path: str) -> str:
    dir_path, file_name = os.path.split(file_path)
    name, ext = os.path.splitext(file_name)
    parts = file_path.split(os.sep)
    split_folders = {"train", "test", "val"}
    split_index = -1
    video_folder = None
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] in split_folders:
            split_index = i
            break
    if split_index != -1 and split_index + 1 < len(parts):
        video_folder = parts[split_index + 1]
    else:
        raise ValueError("Could not determine video folder from path")
    expected_suffix = f"_train_{video_folder}"
    if not name.endswith(expected_suffix):
        new_name = f"{name}{expected_suffix}{ext}"
    else:
        new_name = file_name
    new_path = os.path.join(dir_path, new_name)
    if new_path != file_path:
        os.rename(file_path, new_path)
    return new_path


def rename_davis_file(file_path: str) -> str:
    dir_path, file_name = os.path.split(file_path)
    name, ext = os.path.splitext(file_name)
    if ext.lower() != ".png":
        return file_path
    file_path.split(os.sep)
    parent_folder = os.path.basename(os.path.dirname(file_path))
    new_name = f"{name}_{parent_folder}{ext}"
    new_path = os.path.join(dir_path, new_name)
    logging.debug("new path constructed: %s", new_path)
    if new_path != file_path:
        os.rename(file_path, new_path)
        logging.debug(
            "Renamed %s to %s",
            file_path,
            new_path,
        )
    return new_path


def scan_folder(folder_path):
    print(f"Scanning folder at {folder_path}")
    file_paths = []
    for root, _, files in os.walk(folder_path):
        if "SegmentationClass" in root or "SegmentationObject" in root:
            continue
        for filename in files:
            file_paths.append(os.path.join(root, filename))
    return file_paths


def scan_dataset(
    base_path,
    rename_annotation_files=False,
    input_type=None,
):
    logging.debug("Scanning dataset at %s", base_path)
    annotation_files = []
    image_files = []
    file_paths = scan_folder(base_path)
    for file_path in file_paths:
        _, ext = os.path.splitext(file_path.lower())
        if input_type == "davis":
            if ".png" not in ANNOTATION_EXTENSIONS:
                ANNOTATION_EXTENSIONS.append(".png")
            if ".png" in SAMPLES_EXTENSIONS:
                SAMPLES_EXTENSIONS.remove(".png")
        if ext in ANNOTATION_EXTENSIONS:
            annotation_files.append(file_path)
        elif ext in SAMPLES_EXTENSIONS:
            image_files.append(file_path)
    logging.debug(
        "Found %s annotation files and %s image files",
        len(annotation_files),
        len(image_files),
    )
    return annotation_files, image_files


def get_mot_partitions(video_files):
    logging.debug("Creating video partitions")
    video_groups = {}
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith((".jpg", ".png")):
            continue
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        parent_folder = os.path.basename(os.path.dirname(file_path))
        video_id = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
        if not parent_folder.startswith("img"):
            continue
        if video_id not in video_groups:
            video_groups[video_id] = []
        try:
            frame_num = int(os.path.splitext(file_name)[0])
        except ValueError:
            continue
        video_groups[video_id].append((file_path, frame_num, file_size))
    for video_id in video_groups:
        video_groups[video_id].sort(key=lambda x: x[1])
    partitions = []
    current_partition = {}
    current_size = 0
    partition_num = 1

    def create_partition(samples, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(samples),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [samples[vid] for vid in sorted(samples)],
        }

    for video_id, frames in video_groups.items():
        total_video_size = sum(size for _, _, size in frames)
        if total_video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    {video_id: [file_path for file_path, _, _ in frames]},
                    total_video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for video %s with %s frames",
                partition_num,
                video_id,
                len(frames),
            )
        else:
            if current_size + total_video_size > MAX_PARTITION_SIZE_BYTES:
                if current_partition:
                    partitions.append(
                        create_partition(
                            current_partition,
                            current_size,
                            partition_num,
                        )
                    )
                    partition_num += 1
                    logging.debug(
                        "Created partition %s with %s videos",
                        partition_num,
                        len(current_partition),
                    )
                current_partition = {}
                current_size = 0
            current_partition[video_id] = [file_path for file_path, _, _ in frames]
            current_size += total_video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions


def get_davis_partitions(video_files):
    logging.debug("Creating video partitions")
    video_groups = {}
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith((".jpg", ".jpeg")):
            continue
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        parent_folder = os.path.basename(os.path.dirname(file_path))
        video_id = parent_folder
        if video_id not in video_groups:
            video_groups[video_id] = []
        try:
            frame_num = int(os.path.splitext(file_name)[0])
        except ValueError:
            continue
        video_groups[video_id].append((file_path, frame_num, file_size))
    for video_id in video_groups:
        video_groups[video_id].sort(key=lambda x: x[1])
    partitions = []
    current_partition = {}
    current_size = 0
    partition_num = 1

    def create_partition(samples, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(samples),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [samples[vid] for vid in sorted(samples)],
        }

    for video_id, frames in video_groups.items():
        total_video_size = sum(size for _, _, size in frames)
        if total_video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    {video_id: [file_path for file_path, _, _ in frames]},
                    total_video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for video %s with %s frames",
                partition_num,
                video_id,
                len(frames),
            )
        else:
            if current_size + total_video_size > MAX_PARTITION_SIZE_BYTES:
                if current_partition:
                    partitions.append(
                        create_partition(
                            current_partition,
                            current_size,
                            partition_num,
                        )
                    )
                    partition_num += 1
                    logging.debug(
                        "Created partition %s with %s videos",
                        partition_num,
                        len(current_partition),
                    )
                current_partition = {}
                current_size = 0
            current_partition[video_id] = [file_path for file_path, _, _ in frames]
            current_size += total_video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions


def get_video_imagenet_partitions(video_files):
    logging.debug("Creating video partitions")
    video_list = []
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith(
            (".mp4", ".avi", ".mov", ".mkv")
        ):
            continue
        file_size = os.path.getsize(file_path)
        video_list.append((file_path, file_size))
    video_list.sort(key=lambda x: x[1], reverse=True)
    partitions = []
    current_partition = []
    current_size = 0
    partition_num = 1

    def create_partition(videos, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(videos),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [video[0] for video in videos],
        }

    for video_path, video_size in video_list:
        if video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    [(video_path, video_size)],
                    video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for large video %s",
                partition_num,
                video_path,
            )
        else:
            if current_size + video_size > MAX_PARTITION_SIZE_BYTES:
                partitions.append(
                    create_partition(
                        current_partition,
                        current_size,
                        partition_num,
                    )
                )
                partition_num += 1
                logging.debug(
                    "Created partition %s with %s videos",
                    partition_num,
                    len(current_partition),
                )
                current_partition = []
                current_size = 0
            current_partition.append((video_path, video_size))
            current_size += video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions


def get_kinetics_partitions(video_files):
    logging.debug("Creating video partitions")
    video_list = []
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith(
            (".mp4", ".avi", ".mov", ".mkv")
        ):
            continue
        file_size = os.path.getsize(file_path)
        video_list.append((file_path, file_size))
    video_list.sort(key=lambda x: x[1], reverse=True)
    partitions = []
    current_partition = []
    current_size = 0
    partition_num = 1

    def create_partition(videos, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(videos),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [video[0] for video in videos],
        }

    for video_path, video_size in video_list:
        if video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    [(video_path, video_size)],
                    video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for large video %s",
                partition_num,
                video_path,
            )
        else:
            if current_size + video_size > MAX_PARTITION_SIZE_BYTES:
                partitions.append(
                    create_partition(
                        current_partition,
                        current_size,
                        partition_num,
                    )
                )
                partition_num += 1
                logging.debug(
                    "Created partition %s with %s videos",
                    partition_num,
                    len(current_partition),
                )
                current_partition = []
                current_size = 0
            current_partition.append((video_path, video_size))
            current_size += video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions


def get_video_mscoco_partitions(video_files):
    logging.debug("Creating video partitions")
    video_list = []
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith(
            (".mp4", ".avi", ".mov", ".mkv")
        ):
            continue
        file_size = os.path.getsize(file_path)
        video_list.append((file_path, file_size))
    video_list.sort(key=lambda x: x[1], reverse=True)
    partitions = []
    current_partition = []
    current_size = 0
    partition_num = 1

    def create_partition(videos, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(videos),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [video[0] for video in videos],
        }

    for video_path, video_size in video_list:
        if video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    [(video_path, video_size)],
                    video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for large video %s",
                partition_num,
                video_path,
            )
        else:
            if current_size + video_size > MAX_PARTITION_SIZE_BYTES:
                partitions.append(
                    create_partition(
                        current_partition,
                        current_size,
                        partition_num,
                    )
                )
                partition_num += 1
                logging.debug(
                    "Created partition %s with %s videos",
                    partition_num,
                    len(current_partition),
                )
                current_partition = []
                current_size = 0
            current_partition.append((video_path, video_size))
            current_size += video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions


def get_youtube_bb_partitions(video_files):
    logging.debug("Creating video partitions")
    video_groups = {}
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith((".jpg", ".png")):
            continue
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        if "_" not in file_name:
            continue
        file_name = os.path.splitext(file_name)[0]
        video_id, frame_num = file_name.rsplit("_", 1)
        if not frame_num.isdigit():
            continue
        if video_id not in video_groups:
            video_groups[video_id] = []
        video_groups[video_id].append((file_path, int(frame_num), file_size))
    for video_id in video_groups:
        video_groups[video_id].sort(key=lambda x: x[1])
    partitions = []
    current_partition = {}
    current_size = 0
    partition_num = 1

    def create_partition(samples, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(samples),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [samples[vid] for vid in sorted(samples)],
        }

    for video_id, frames in video_groups.items():
        total_video_size = sum(size for _, _, size in frames)
        if current_size + total_video_size > MAX_PARTITION_SIZE_BYTES:
            if current_partition:
                partitions.append(
                    create_partition(
                        current_partition,
                        current_size,
                        partition_num,
                    )
                )
                partition_num += 1
                logging.debug(
                    "Created partition %s with %s videos",
                    partition_num,
                    len(current_partition),
                )
                current_partition = {}
                current_size = 0
        current_partition[video_id] = [file_path for file_path, _, _ in frames]
        current_size += total_video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    logging.debug(
        "Final Partitions from get_youtube_bb_partitions: %s",
        partitions,
    )
    return partitions


def get_youtube_bb_relative_path(abs_path):
    """
    Extract the relative path starting from the folder containing train/test/val directories.

    Args:
        abs_path (str): Absolute path to the file

    Returns:
        str: Relative path starting from the folder containing the parent directory of
            train/test/val
    """
    abs_path = os.path.normpath(abs_path)
    path_parts = abs_path.split(os.sep)
    try:
        split_index = next(
            i for i, part in enumerate(path_parts) if part in ["train", "test", "val"]
        )
        if split_index > 0:
            split_index -= 1
    except StopIteration:
        return None
    return os.path.join(*path_parts[split_index:])


def get_davis_relative_path(abs_path: str) -> str:
    """
    Extract the relative path starting from the grand-grandparent directory.

    Args:
        abs_path (str): Absolute path to the file

    Returns:
        str: Relative path starting from the grand-grandparent directory
    """
    abs_path = os.path.normpath(abs_path)
    path_parts = abs_path.split(os.sep)
    if len(path_parts) > 3:
        split_index = len(path_parts) - 4
    else:
        return None
    return os.path.join(*path_parts[split_index:])


def get_images_partitions(image_files):
    """Split image files into partitions and return partition stats."""
    logging.debug("Creating image partitions")
    partitions = []
    current_partition = []
    current_size = 0
    partition_num = 1

    def create_partition(files, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(files),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": files,
        }

    for image_file in image_files:
        file_size = os.path.getsize(image_file)
        if current_size + file_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    current_partition,
                    current_size,
                    partition_num,
                )
            )
            partition_num += 1
            current_partition = [image_file]
            current_size = file_size
        else:
            current_partition.append(image_file)
            current_size += file_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s image partitions",
        len(partitions),
    )
    return partitions


def get_annotations_partition(annotation_files):
    logging.debug("Creating annotations partition")
    return {
        "partitionNum": 0,
        "sampleCount": len(annotation_files),
        "diskSizeMB": get_size_mb(annotation_files),
        "type": ANNOTATION_PARTITION_TYPE,
        "files": annotation_files,
    }


def get_video_mot_cloud_file_path(
    dataset_id,
    dataset_version,
    base_dataset_path,
    file_path,
    include_version_in_cloud_path=False,
):
    abs_file_path = os.path.abspath(file_path)
    abs_base_path = os.path.abspath(base_dataset_path)
    if abs_file_path.startswith(abs_base_path):
        rel_path = os.path.relpath(abs_file_path, abs_base_path)
    else:
        rel_path = os.path.basename(abs_file_path)
    if include_version_in_cloud_path:
        final_path = os.path.join(dataset_id, dataset_version, rel_path).replace(os.sep, "/")
        logging.debug(
            "constructed cloud file path: %s",
            final_path,
        )
        return final_path
    else:
        final_path = os.path.join(dataset_id, rel_path).replace(os.sep, "/")
        logging.debug(
            "constructed cloud file path: %s",
            final_path,
        )
        return final_path


def get_cloud_file_path(dataset_id, dataset_version, base_dataset_path, file_path, include_version_in_cloud_path=False):
    if include_version_in_cloud_path:
        return os.path.join(dataset_id, dataset_version, os.path.relpath(file_path, base_dataset_path)).replace(os.sep, "/")
    else:
        return os.path.join(dataset_id, os.path.relpath(file_path, base_dataset_path)).replace(os.sep, "/")

def get_batch_pre_signed_upload_urls(
    cloud_file_paths,
    rpc,
    type,
    bucket_alias="",
    account_number="",
):
    logging.debug(
        "Getting presigned URLs for %s files",
        len(cloud_file_paths),
    )
    payload_get_presigned_url = {
        "fileNames": cloud_file_paths,
        "type": type,
        "isPrivateBucket": (True if bucket_alias else False),
        "bucketAlias": bucket_alias,
        "accountNumber": account_number,
    }
    resp = rpc.post(
        "/v2/dataset/get_batch_pre_signed_upload_urls",
        payload={
            "fileNames": cloud_file_paths,
            "type": type,
            "isPrivateBucket": (True if bucket_alias else False),
            "bucketAlias": bucket_alias,
            "accountNumber": account_number,
        },
    )
    logging.debug(
        "payload for getting the presigned urls: %s",
        payload_get_presigned_url,
    )
    if resp["success"]:
        return resp["data"]
    else:
        logging.error(
            "Failed to get presigned URLs: %s",
            resp["message"],
        )
        return resp["message"]


def upload_file(local_path, presigned_url, max_attempts=5):
    if not presigned_url:
        logging.error(
            "Missing presigned URL for %s",
            local_path,
        )
        return False
    for attempt in range(max_attempts):
        try:
            with open(local_path, "rb") as f:
                response = requests.put(
                    presigned_url,
                    data=f,
                    allow_redirects=True,
                    timeout=30,
                )
                if response.status_code == 200:
                    logging.debug(
                        "Successfully uploaded %s to %s",
                        local_path,
                        presigned_url,
                    )
                    return True
                else:
                    logging.warning(
                        "Failed to upload %s (status: %s), attempt %s/%s",
                        local_path,
                        response.status_code,
                        attempt + 1,
                        max_attempts,
                    )
                    response.raise_for_status()
        except Exception as e:
            if attempt == max_attempts - 1:
                logging.error(
                    "Failed to upload %s after %s attempts. Error: %s",
                    local_path,
                    max_attempts,
                    e,
                )
                return False
            else:
                logging.warning(
                    "Attempt %s/%s failed for %s. Retrying... Error: %s",
                    attempt + 1,
                    max_attempts,
                    local_path,
                    e,
                )


def update_annotation_bucket_url(
    rpc,
    dataset_id,
    partition_number,
    annotation_bucket_url,
):
    payload = {
        "partitionNumber": partition_number,
        "path": annotation_bucket_url,
    }
    logging.debug(
        "Updating annotation bucket URL for partition %s with URL: %s",
        partition_number,
        annotation_bucket_url,
    )
    url = f"/v2/dataset/update_annotation_path/{dataset_id}"
    response = rpc.post(url, payload=payload)
    return response


def upload_compressed_dataset(
    rpc,
    dataset_path,
    bucket_alias="",
    account_number="",
):
    file_name = os.path.basename(dataset_path)
    presigned_urls = get_batch_pre_signed_upload_urls(
        [file_name],
        rpc,
        "compressed",
        bucket_alias,
        account_number,
    )
    upload_url = presigned_urls[file_name]
    upload_file(dataset_path, upload_url)
    return upload_url.split("?")[0]


def compress_annotation_files(file_paths, base_dataset_path):
    zip_file_path = os.path.join(base_dataset_path, "annotations.zip")
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            zipf.write(
                file_path,
                arcname=os.path.relpath(file_path, base_dataset_path).replace(os.sep, "/"),
            )
    logging.info(
        "Files zipped successfully into %s",
        zip_file_path,
    )
    return zip_file_path


def is_file_compressed(file_path):
    _, ext = os.path.splitext(file_path.lower())
    return ext in COMPRESSED_EXTENSIONS


def update_partitions_numbers(
    rpc,
    dataset_id,
    items,
    partition_key="partitionNum",
):
    try:
        logging.info(
            "Updating partition numbers for dataset %s",
            dataset_id,
        )
        dataset_info = rpc.get(f"/v2/dataset/{dataset_id}").get("data")
        if dataset_info:
            dataset_partition_stats = dataset_info.get("partitionStats")
            if dataset_partition_stats:
                max_partition_num = max([p["partitionNum"] for p in dataset_partition_stats])
                for item in items:
                    item[partition_key] = max_partition_num + item[partition_key]
    except Exception as e:
        logging.error(
            "Error updating partition numbers: %s",
            e,
        )
    return items


def complete_dataset_items_upload(
    rpc,
    dataset_id,
    partition_stats,
    target_version="v1.0",
    source_version="",
    action_type="data_import",
):
    logging.debug(
        "partition_stats for complete_dataset_items_upload: %s",
        partition_stats,
    )
    logging.info(
        "Completing dataset items upload for dataset %s",
        dataset_id,
    )
    url = "/v2/dataset/complete_dataset_items_upload"
    payload = {
        "action": action_type,
        "_id": dataset_id,
        "sourceVersion": source_version,
        "targetVersion": target_version,
        "totalSample": sum(
            [p["sampleCount"] for p in partition_stats if p["type"] == SAMPLES_PARTITION_TYPE]
        ),
        "partitionInfo": [
            {
                "partitionNum": p["partitionNum"],
                "sampleCount": p["sampleCount"],
                "diskSizeMB": p["diskSizeMB"],
                "type": p["type"],
            }
            for p in (
                [partition_stats[0]] + partition_stats[1]
                if isinstance(partition_stats, tuple)
                else (partition_stats if isinstance(partition_stats, list) else [partition_stats])
            )
            if p["type"] == SAMPLES_PARTITION_TYPE
        ],
    }
    logging.info("Payload: %s", payload)
    response = rpc.post(url, payload=payload)
    logging.info("Response: %s", response)
    return response


def create_partition_stats(
    rpc,
    partition_stats,
    dataset_id,
    target_version,
    source_version="",
):
    logging.info(
        "Creating partition stats for dataset %s",
        dataset_id,
    )
    new_partition_stats = [stat for stat in partition_stats if stat is not None]
    payload = {
        "datasetId": dataset_id,
        "sourceVersion": source_version,
        "targetVersion": target_version,
        "partitionStats": new_partition_stats,
    }
    url = "/v2/dataset/create-partition"
    logging.debug(
        "Making request to %s with payload: %s",
        url,
        payload,
    )
    response = rpc.post(url, payload=payload)
    logging.debug(
        "response after calling create-partition API: %s",
        response,
    )
    return response
