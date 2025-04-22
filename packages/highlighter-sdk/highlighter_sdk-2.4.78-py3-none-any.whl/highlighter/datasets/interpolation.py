from logging import warning
from os import PathLike
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from shapely.wkt import loads as wkt_loads
from ultralytics import data

from highlighter.agent.capabilities.sources import VideoFrameIterator
from highlighter.core.const import PIXEL_LOCATION_ATTRIBUTE_UUID
from highlighter.datasets.base_models import ImageRecord


def interpolate_pixel_locations_between_frames(
    annotations_df: pd.DataFrame,
    data_files_df: pd.DataFrame,
    frame_frac: Optional[float] = None,
    frame_count: Optional[int] = None,
    frame_save_dir: Optional[PathLike] = None,
    source_video_dir: Optional[PathLike] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    adf = annotations_df
    if "frame_id" not in adf.columns:
        try:
            frame_ids = adf.extra_fields.apply(lambda d: d["frame_id"])
            adf["frame_id"] = frame_ids
        except KeyError as _:
            raise ValueError(
                "Unable to determine frame_id. Expected a frame_id column or extra_fields with a 'frame_id' key"
            )

    adf = adf.merge(data_files_df, on="data_file_id", how="left")
    sorted_adf = adf.sort_values(by="frame_id").set_index("frame_id").copy()

    # Convert WKT strings to Polygon objects only once
    sorted_adf.loc[sorted_adf.attribute_id == PIXEL_LOCATION_ATTRIBUTE_UUID, "value"] = sorted_adf[
        sorted_adf.attribute_id == PIXEL_LOCATION_ATTRIBUTE_UUID
    ].value.apply(lambda p: wkt_loads(p) if isinstance(p, str) else p)

    interpolated_rows = []

    for entity_id, grp in sorted_adf.groupby("entity_id"):
        loc_frames = grp[grp.attribute_id == PIXEL_LOCATION_ATTRIBUTE_UUID].index.to_numpy()
        loc_values = grp[grp.attribute_id == PIXEL_LOCATION_ATTRIBUTE_UUID].value.to_numpy()
        others_adf = grp[~(grp.attribute_id == PIXEL_LOCATION_ATTRIBUTE_UUID)]
        attrs = (
            others_adf.groupby("frame_id")
            .agg({"attribute_name": list, "attribute_id": list, "value": list})
            .iloc[0]
        )

        data_file_id = grp.data_file_id.iloc[0]
        dataset_id = grp.dataset_id.iloc[0]
        # Iterate over consecutive loc_frames
        for i in range(len(loc_frames) - 1):
            current_frame, next_frame = loc_frames[i], loc_frames[i + 1]
            current_bounds, next_bounds = loc_values[i].bounds, loc_values[i + 1].bounds
            frame_diff = next_frame - current_frame

            # Generate interpolated loc_values
            minX_vals = np.linspace(current_bounds[0], next_bounds[0], frame_diff + 1)[1:-1]
            minY_vals = np.linspace(current_bounds[1], next_bounds[1], frame_diff + 1)[1:-1]
            maxX_vals = np.linspace(current_bounds[2], next_bounds[2], frame_diff + 1)[1:-1]
            maxY_vals = np.linspace(current_bounds[3], next_bounds[3], frame_diff + 1)[1:-1]

            # Use itertools.chain to reduce append calls and improve performance
            for f, minX, minY, maxX, maxY in zip(
                range(current_frame + 1, next_frame), minX_vals, minY_vals, maxX_vals, maxY_vals
            ):
                interpolated_rows.append(
                    {
                        "frame_id": f,
                        "entity_id": entity_id,
                        "attribute_name": "pixel_location",
                        "attribute_id": PIXEL_LOCATION_ATTRIBUTE_UUID,
                        "value": Polygon(
                            [(minX, minY), (maxX, minY), (maxX, maxY), (minX, maxY), (minX, minY)]
                        ),
                        "data_file_id": f"{data_file_id}",
                        "dataset_id": int(dataset_id),
                    }
                )
                interpolated_rows.extend(
                    [
                        {
                            "frame_id": f,
                            "entity_id": entity_id,
                            "attribute_name": attribute_name,
                            "attribute_id": attribute_id,
                            "value": value,
                            "data_file_id": f"{data_file_id}",
                            "dataset_id": int(dataset_id),
                        }
                        for attribute_name, attribute_id, value in zip(*attrs.values)
                    ]
                )

    # Create DataFrame with interpolated rows and concatenate with the original DataFrame
    interpolated_adf = pd.concat([adf, pd.DataFrame(interpolated_rows)], ignore_index=True)
    # Keep the original_data_file_id, we'll use it later
    interpolated_adf["original_data_file_id"] = interpolated_adf.data_file_id.copy()
    # Append -{frame_id} to the data_file_id so each frame's data_file_id is unique
    interpolated_adf.loc[:, "data_file_id"] = (
        interpolated_adf["data_file_id"] + "-" + interpolated_adf["frame_id"].astype(str)
    )

    if (frame_frac is not None) or (frame_count is not None):
        interpolated_adf = interpolated_adf.sample(n=frame_count, frac=frame_frac)

    ddf = data_files_df

    def make_frame_data_files(grp, *, split):
        data_file_id = grp.name
        original_data_file_id = data_file_id.split("-")[0]
        original_data_file = ddf[ddf.data_file_id == original_data_file_id].iloc[0].to_dict()

        return pd.Series(
            ImageRecord(
                data_file_id=data_file_id,
                split=split,
                filename=f"{data_file_id}.jpg",
                width=original_data_file.get("width", None),
                height=original_data_file.get("height", None),
                assessment_id=original_data_file.get("assessment_id", None),
            ).model_dump()
        )

    # Preserve the original splits in the interpolated_ddf
    _split_ddfs = []
    for split in ddf.split.unique():
        # get all the data_files pre split for the original ds
        split_data_file_ids = ddf[ddf.split == split].data_file_id

        # filter out all the matching data_files from the interpolated annotations_df
        mask = interpolated_adf.data_file_id.map(lambda d: d.split("-")[0]).isin(split_data_file_ids)

        def fn(grp):
            return make_frame_data_files(grp, split=split)

        _split_ddfs.append(interpolated_adf[mask].groupby("data_file_id").apply(fn))
    interpolated_ddf = pd.concat(_split_ddfs, ignore_index=True)

    if frame_save_dir is not None:
        for original_data_file_id in ddf.data_file_id.unique():
            original_video_filename = ddf[ddf.data_file_id == original_data_file_id].iloc[0].filename
            if not original_video_filename.endswith(".mp4"):
                warning(f"Skipping {original_video_filename}, not a Video")
                continue

            source_video_path = (
                original_video_filename
                if source_video_dir is None
                else Path(source_video_dir) / original_video_filename
            )

            frame_ids = (
                interpolated_adf[interpolated_adf.original_data_file_id == original_data_file_id]
                .frame_id.unique()
                .tolist()
            )
            video_frame_iter = VideoFrameIterator(source_urls=[source_video_path])
            filename = f"{original_data_file_id}" + "-{}.jpg"
            extracted_frame_ids = video_frame_iter.extract_frames_by_id(
                frame_ids,
                frame_save_dir,
                filename,
            )
            interpolated_adf = interpolated_adf[interpolated_adf.frame_id.isin(extracted_frame_ids)]
            interpolated_ddf = interpolated_ddf[
                interpolated_ddf.data_file_id.isin(interpolated_ddf.data_file_id.unique())
            ]

    return interpolated_adf, interpolated_ddf
