"""Module providing video_detection_mscoco functionality."""

import os
import json
import logging
import tempfile
from collections import defaultdict
import cv2
import requests
from uuid import uuid4
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid,
)


def get_video_mscoco_annotations(
    annotation_paths,
):
    """Process MSCOCO-style video dataset annotations and return duration-based annotations grouped
    by video and split."""
    complete_videos = {
        "train": {},
        "val": {},
        "test": {},
        "unassigned": {},
    }
    for ann_path in annotation_paths:
        if not os.path.exists(ann_path):
            logging.warning(
                "Annotation file not found: %s",
                ann_path,
            )
            continue
        filename = os.path.basename(ann_path).lower()
        if "train" in filename:
            split = "train"
        elif "val" in filename:
            split = "val"
        elif "test" in filename:
            split = "test"
        elif "metadata" in filename:
            continue
        else:
            split = "unassigned"
        with open(ann_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        categories = {cat["id"]: cat["name"] for cat in data.get("categories", [])}
        video_meta = {video["id"]: video for video in data.get("videos", [])}
        annotations_by_video = defaultdict(list)
        for ann in data.get("annotations", []):
            annotations_by_video[ann["video_id"]].append(ann)
        for (
            video_id,
            annotations,
        ) in annotations_by_video.items():
            if video_id not in video_meta:
                logging.warning(
                    "Video ID %s not found in metadata.",
                    video_id,
                )
                continue
            video_info = video_meta[video_id]
            video_name = os.path.splitext(video_info["file_name"])[0]
            fps = video_info["fps"]
            video_width = video_info["width"]
            video_height = video_info["height"]
            annotations = sorted(
                annotations,
                key=lambda x: x["frame_id"],
            )
            for idx, ann in enumerate(annotations):
                frame_id = ann["frame_id"]
                category_id = ann["category_id"]
                time_start = frame_id / fps
                if idx + 1 < len(annotations):
                    next_frame_id = annotations[idx + 1]["frame_id"]
                else:
                    next_frame_id = video_info["frames"]
                time_end = next_frame_id / fps
                annotation = {
                    "id": str(generate_short_uuid()),
                    "segmentation": ann.get("segmentation", []),
                    "order_id": frame_id,
                    "isCrowd": [
                        (float(item) if isinstance(item, (int, float)) else 0)
                        for item in (
                            ann.get("iscrowd", [0])
                            if isinstance(
                                ann.get("iscrowd"),
                                list,
                            )
                            else [ann.get("iscrowd", 0)]
                        )
                    ],
                    "confidence": 0.0,
                    "bbox": ann.get("bbox", []),
                    "height": ann["bbox"][3],
                    "width": ann["bbox"][2],
                    "center": (
                        [
                            ann["bbox"][0] + ann["bbox"][2] / 2,
                            ann["bbox"][1] + ann["bbox"][3] / 2,
                        ]
                        if ann.get("bbox")
                        else []
                    ),
                    "area": ann.get("area", 0.0),
                    "category": categories.get(category_id, "unknown"),
                    "masks": [],
                    "duration": [
                        round(time_start, 4),
                        round(time_end, 4),
                    ],
                }
                if video_name not in complete_videos[split]:
                    complete_videos[split][video_name] = {
                        "sequence_name": video_name,
                        "video_height": video_height,
                        "video_width": video_width,
                        "fps": fps,
                        "annotations": [],
                    }
                complete_videos[split][video_name]["annotations"].append(annotation)
    return complete_videos


def get_video_metadata(presigned_url):
    """
    Downloads a video from a presigned URL, extracts its dimensions (width, height),
    FPS, and duration, and saves the first frame as an image locally.

    Args:
        presigned_url (str): The presigned URL of the video.

    Returns:
        dict: {
            "width": video_width,
            "height": video_height,
            "fps": rounded_fps,
            "first_frame_path": path_to_saved_image
        }
    """
    try:
        response = requests.get(presigned_url, stream=True, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Failed to download video: {response.status_code}")
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video:
            for chunk in response.iter_content(chunk_size=8192):
                temp_video.write(chunk)
            temp_video.flush()
            cap = cv2.VideoCapture(temp_video.name)
            if not cap.isOpened():
                raise Exception("Failed to open video file")
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            success, frame = cap.read()
            if not success:
                raise Exception("Failed to read first frame")
            frame_filename = f"first_frame_{uuid4().hex}.jpg"
            cv2.imwrite(frame_filename, frame)
            cap.release()
        rounded_fps = int(fps + 0.5)
        return {
            "width": width,
            "height": height,
            "fps": rounded_fps,
            "first_frame_path": os.path.abspath(frame_filename),
        }
    except Exception as e:
        print(f"Error: {e}")
        return None


def add_video_mscoco_dataset_items_details(batch_dataset_items, frames_details):
    """Add details to video MSCOCO dataset items.

    Args:
        batch_dataset_items: Batch of dataset items to process
        frames_details: Details of frames from annotations

    Returns:
        List of processed dataset items
    """
    processed_batch = []
    logging.debug(
        "Batch dataset items: %s",
        batch_dataset_items,
    )
    for dataset_item in batch_dataset_items:
        video_info = dataset_item.get("fileInfoResponse", {}).get("video")
        if not video_info:
            logging.warning(
                "No video info found in dataset item: %s",
                dataset_item,
            )
            continue
        file_location = video_info.get("fileLocation")
        file_name = video_info.get("filename")
        file_name = os.path.splitext(file_name)[0]
        presigned_url = video_info.get("cloudPath")
        if not file_location or not file_name or not presigned_url:
            logging.warning(
                "Missing file location, filename, or presigned URL in video info: %s",
                video_info,
            )
            continue
        video_metadata = get_video_metadata(presigned_url)
        if not video_metadata:
            logging.warning(
                "Failed to extract metadata for video: %s",
                file_name,
            )
            continue
        video_metadata.get("first_frame_path")
        split_dataset_item = get_corresponding_split_type(file_location)
        all_splits_data = frames_details.get(split_dataset_item)
        if not all_splits_data:
            logging.warning(
                "No annotation data found for video file %s",
                file_name,
            )
            continue
        split_video_data = all_splits_data.get(file_name)
        if not split_video_data:
            logging.warning(
                "No annotation data found for split %s in video %s",
                split_dataset_item,
                file_name,
            )
            continue
        split_video_annotation_data = split_video_data.get("annotations", [])
        video_height = split_video_data.get("video_height") or video_metadata.get("height")
        video_width = split_video_data.get("video_width") or video_metadata.get("width")
        fps = split_video_data.get("fps") or video_metadata.get("fps")
        rounded_fps = int(fps + 0.5)
        first_frame_path = video_metadata.get("first_frame_path")
        if first_frame_path:
            new_first_frame_path = first_frame_path.lstrip("/")
        dataset_id = dataset_item.get("_idDataset")
        bucket_upload_first_frame_path = f"{dataset_id}/{new_first_frame_path}"
        logging.debug(f"First frame path: {first_frame_path}")
        logging.debug(f"Bucket upload first frame path: {bucket_upload_first_frame_path}")
        # Update the dataset item
        dataset_item.update(
            {
                "splitType": split_dataset_item,
                "annotations": split_video_annotation_data,
                "video_height": video_height,
                "video_width": video_width,
                "frame_rate": rounded_fps,
                "first_frame_path": first_frame_path,
                "bucket_upload_first_frame_path": bucket_upload_first_frame_path,
            }
        )

        processed_batch.append(
            {
                "sample_details": dataset_item,
                "is_complete": all(
                    dataset_item.get(k) is not None for k in ["video_height", "video_width"]
                ),
            }
        )

    logging.debug(f"Processed batch: {processed_batch}")
    return processed_batch
