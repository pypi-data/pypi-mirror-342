"""Module providing video_mscoco_detection functionality."""

import json
import logging
import os
import traceback
from matrice.data_processing.server_utils import (
    get_corresponding_split_type,
    generate_short_uuid,
)


def calculate_bbox_properties(bbox):
    """Calculate properties for a bounding box.

    Args:
        bbox: Bounding box in format [x_min, y_min, width, height]

    Returns:
        Dictionary containing height, width, center coordinates, and area

    Raises:
        ValueError: If bbox doesn't have exactly 4 elements
    """
    if len(bbox) != 4:
        raise ValueError("Bounding box must be in the format [x_min, y_min, width, height].")
    x_min, y_min, width, height = bbox
    center_x = x_min + width / 2
    center_y = y_min + height / 2
    area = width * height
    return {
        "height": float(height),
        "width": float(width),
        "center": [
            float(center_x),
            float(center_y),
        ],
        "area": float(area),
    }


def get_msococo_videos_details(annotation_files):
    """Process MSCOCO video annotation files and extract video details.

    Args:
        annotation_files: List of paths to MSCOCO video annotation JSON files

    Returns:
        Tuple containing:
        - Dictionary of video details indexed by file location
        - List of video IDs missing annotations
        - Dictionary of class-wise split counts
    """
    complete_videos = {}
    missing_annotations = []
    missing_metadata = {}
    classwise_splits = {}
    logging.info(
        "Processing %d video annotation files",
        len(annotation_files),
    )
    if not annotation_files:
        logging.error("No annotation files provided")
        return (
            complete_videos,
            missing_annotations,
            classwise_splits,
        )
    for file_index, file_path in enumerate(annotation_files, 1):
        logging.debug(
            "\nProcessing file %d/%d: %s",
            file_index,
            len(annotation_files),
            file_path,
        )
        if not os.path.exists(file_path):
            logging.error("File not found: %s", file_path)
            continue
        try:
            with open(file_path, encoding="utf-8") as file_obj:
                try:
                    data = json.load(file_obj)
                except json.JSONDecodeError as err:
                    logging.error(
                        "Invalid JSON in %s: %s",
                        file_path,
                        err,
                    )
                    continue
                videos = data.get("videos", [])
                categories = data.get("categories", [])
                annotations = data.get("annotations", [])
            if not videos or not annotations:
                logging.error(
                    "Missing videos or annotations in %s",
                    file_path,
                )
                continue
            video_info = {
                vid["id"]: vid for vid in videos if isinstance(vid, dict) and "id" in vid
            }
            category_map = {
                cat["id"]: cat["name"]
                for cat in categories
                if isinstance(cat, dict) and "id" in cat
            }
            for category_name in category_map.values():
                if category_name not in classwise_splits:
                    classwise_splits[str(category_name)] = {
                        "train": 0,
                        "test": 0,
                        "val": 0,
                        "unassigned": 0,
                    }
            video_annotations = {}
            for annotation in annotations:
                if not isinstance(annotation, dict):
                    continue
                video_id = annotation.get("video_id")
                frame_id = annotation.get("frame_id")
                if video_id is None or frame_id is None:
                    continue
                if video_id not in video_annotations:
                    video_annotations[video_id] = {}
                if frame_id not in video_annotations[video_id]:
                    video_annotations[video_id][frame_id] = []
                video_annotations[video_id][frame_id].append(annotation)
            processed = 0
            skipped = 0
            for (
                video_id,
                frame_annotations,
            ) in video_annotations.items():
                video = video_info.get(video_id)
                if not video:
                    skipped += 1
                    continue
                try:
                    processed_annotations = []
                    for (
                        frame_id,
                        frame_anns,
                    ) in frame_annotations.items():
                        for annotation in frame_anns:
                            bbox = [float(coord) for coord in annotation.get("bbox", [])]
                            if not bbox or len(bbox) != 4:
                                continue
                            bbox_properties = calculate_bbox_properties(bbox)
                            annotation_json = {
                                "id": str(generate_short_uuid()),
                                "frame_id": int(frame_id),
                                "segmentation": [
                                    [float(coord) for coord in segment]
                                    for segment in annotation.get(
                                        "segmentation",
                                        [],
                                    )
                                    if isinstance(
                                        segment,
                                        list,
                                    )
                                ],
                                "isCrowd": [
                                    (
                                        float(item)
                                        if isinstance(
                                            item,
                                            (
                                                int,
                                                float,
                                            ),
                                        )
                                        else 0
                                    )
                                    for item in (
                                        annotation.get(
                                            "iscrowd",
                                            [0],
                                        )
                                        if isinstance(
                                            annotation.get("iscrowd"),
                                            list,
                                        )
                                        else [
                                            annotation.get(
                                                "iscrowd",
                                                0,
                                            )
                                        ]
                                    )
                                ],
                                "confidence": float(
                                    annotation.get(
                                        "confidence",
                                        0.0,
                                    )
                                ),
                                "bbox": bbox,
                                "height": bbox_properties["height"],
                                "width": bbox_properties["width"],
                                "center": bbox_properties["center"],
                                "area": float(
                                    annotation.get(
                                        "area",
                                        bbox_properties["area"],
                                    )
                                ),
                                "category": str(
                                    category_map.get(
                                        annotation.get("category_id"),
                                        "Unknown",
                                    )
                                ),
                                "masks": annotation.get(
                                    "segmentation",
                                    [],
                                ),
                            }
                            processed_annotations.append(annotation_json)
                    details = {
                        "splitType": get_corresponding_split_type(
                            file_path,
                            include_year=False,
                        ),
                        "file_name": video.get("file_name", "unknown"),
                        "fps": float(video.get("fps", None)),
                        "total_frames": int(video.get("frames", None)),
                        "duration_seconds": float(video.get("duration", None)),
                        "annotations": processed_annotations,
                    }
                    key = f"{details['splitType']}/{details['file_name']}"
                    if "height" in video and "width" in video:
                        details.update(
                            {
                                "video_height": int(video["height"]),
                                "video_width": int(video["width"]),
                            }
                        )
                    else:
                        missing_metadata[key] = details
                    if key in complete_videos:
                        complete_videos[key]["annotations"].extend(details["annotations"])
                    else:
                        complete_videos[key] = details
                    for ann in processed_annotations:
                        classwise_splits[ann["category"]][details["splitType"]] += 1
                    processed += 1
                except Exception as err:
                    logging.error(
                        "Error processing video annotation: %s",
                        err,
                    )
                    skipped += 1
                    continue
            if not annotations:
                missing_annotations.extend(
                    vid["id"] for vid in videos if isinstance(vid, dict) and "id" in vid
                )
        except Exception as err:
            logging.error(
                "Error processing file %s: %s",
                file_path,
                err,
            )
            traceback.print_exc()
    logging.info("\nFinal summary:")
    logging.info(
        "Complete videos: %d",
        len(complete_videos),
    )
    logging.info(
        "Missing annotations: %d",
        len(missing_annotations),
    )
    logging.info(
        "Missing metadata: %d",
        len(missing_metadata),
    )
    for (
        category,
        counts,
    ) in classwise_splits.items():
        counts["total"] = sum(counts.values())
    return (
        {**complete_videos, **missing_metadata},
        missing_annotations,
        classwise_splits,
    )


def add_mscoco_video_dataset_items_details(batch_dataset_items, videos_details):
    """Add video details to batch dataset items.

    Args:
        batch_dataset_items: List of dataset items containing video information
        videos_details: Dictionary of video details indexed by split type and filename

    Returns:
        List of processed dataset items with video details and completion status
    """
    processed_batch = []
    for dataset_item in batch_dataset_items:
        video_key = f"{get_corresponding_split_type(dataset_item.get('fileLocation'))}/{dataset_item.get('filename')}"
        if video_key not in videos_details:
            logging.warning(
                "'%s' not found in videos_details",
                video_key,
            )
            continue
        dataset_item.update(videos_details[video_key])
        processed_batch.append(
            {
                "sample_details": dataset_item,
                "is_complete": all(
                    dataset_item.get(k) is not None
                    for k in [
                        "video_height",
                        "video_width",
                        "fps",
                        "total_frames",
                        "duration_seconds",
                    ]
                ),
            }
        )
    return processed_batch
