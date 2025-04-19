import numpy as np
import os
import polars as pl
from tqdm import tqdm
import concurrent.futures
import pandas as pd
from .boundary_tile import _get_name_mapping
from scipy.sparse import csr_matrix

def process_coarse_tile(
    trx,
    i,
    j,
    coarse_tile_x_min,
    coarse_tile_x_max,
    coarse_tile_y_min,
    coarse_tile_y_max,
    tile_size,
    path_trx_tiles,
    x_min,
    y_min,
    n_fine_tiles_x,
    n_fine_tiles_y,
    max_workers=1,
):
    # Filter the entire dataset for the current coarse tile
    coarse_tile = trx.filter(
        (pl.col("transformed_x") >= coarse_tile_x_min)
        & (pl.col("transformed_x") < coarse_tile_x_max)
        & (pl.col("transformed_y") >= coarse_tile_y_min)
        & (pl.col("transformed_y") < coarse_tile_y_max)
    )

    if not coarse_tile.is_empty():
        # Now process fine tiles using global fine tile indices
        process_fine_tiles(
            coarse_tile,
            i,
            j,
            coarse_tile_x_min,
            coarse_tile_x_max,
            coarse_tile_y_min,
            coarse_tile_y_max,
            tile_size,
            path_trx_tiles,
            x_min,
            y_min,
            n_fine_tiles_x,
            n_fine_tiles_y,
            max_workers,
        )


def process_fine_tiles(
    coarse_tile,
    coarse_i,
    coarse_j,
    coarse_tile_x_min,
    coarse_tile_x_max,
    coarse_tile_y_min,
    coarse_tile_y_max,
    tile_size,
    path_trx_tiles,
    x_min,
    y_min,
    n_fine_tiles_x,
    n_fine_tiles_y,
    max_workers=1,
):

    # Use ThreadPoolExecutor for parallel processing of fine-grain tiles within the coarse tile
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        # Iterate over fine-grain tiles within the global bounds
        for fine_i in range(n_fine_tiles_x):
            fine_tile_x_min = x_min + fine_i * tile_size
            fine_tile_x_max = fine_tile_x_min + tile_size

            # Process only if the fine tile falls within the current coarse tile's bounds
            if not (
                fine_tile_x_min >= coarse_tile_x_min
                and fine_tile_x_max <= coarse_tile_x_max
            ):
                continue

            for fine_j in range(n_fine_tiles_y):
                fine_tile_y_min = y_min + fine_j * tile_size
                fine_tile_y_max = fine_tile_y_min + tile_size

                # Process only if the fine tile falls within the current coarse tile's bounds
                if not (
                    fine_tile_y_min >= coarse_tile_y_min
                    and fine_tile_y_max <= coarse_tile_y_max
                ):
                    continue

                # Submit the task for each fine tile to process in parallel
                futures.append(
                    executor.submit(
                        filter_and_save_fine_tile,
                        coarse_tile,
                        coarse_i,
                        coarse_j,
                        fine_i,
                        fine_j,
                        fine_tile_x_min,
                        fine_tile_x_max,
                        fine_tile_y_min,
                        fine_tile_y_max,
                        path_trx_tiles,
                    )
                )

        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Raise exceptions if any occurred during execution


def filter_and_save_fine_tile(
    coarse_tile,
    coarse_i,
    coarse_j,
    fine_i,
    fine_j,
    fine_tile_x_min,
    fine_tile_x_max,
    fine_tile_y_min,
    fine_tile_y_max,
    path_trx_tiles,
):

    # Filter the coarse tile for the current fine tile's boundaries
    fine_tile_trx = coarse_tile.filter(
        (pl.col("transformed_x") >= fine_tile_x_min)
        & (pl.col("transformed_x") < fine_tile_x_max)
        & (pl.col("transformed_y") >= fine_tile_y_min)
        & (pl.col("transformed_y") < fine_tile_y_max)
    )

    if not fine_tile_trx.is_empty():
        # Add geometry column as a list of [x, y] pairs
        fine_tile_trx = fine_tile_trx.with_columns(
            pl.concat_list([pl.col("transformed_x"), pl.col("transformed_y")]).alias(
                "geometry"
            )
        ).drop(['transformed_x', 'transformed_y', 'cell_id', 'transcript_id'])

        # Define the filename based on fine tile coordinates
        filename = f"{path_trx_tiles}/transcripts_tile_{fine_i}_{fine_j}.parquet"

        # Save the filtered DataFrame to a Parquet file
        fine_tile_trx.to_pandas().to_parquet(filename, index=False)


def transform_transcript_coordinates(
    technology, path_trx, chunk_size, transformation_matrix, image_scale=1, gene_str_to_int_mapping={},
):

    # Load the transcript data based on the technology using Polars
    if technology == "MERSCOPE":
        trx_ini = pl.read_csv(path_trx, columns=["gene", "global_x", "global_y"])
        trx_ini = trx_ini.with_columns(
            [
                pl.col("cell_id"),
                pl.col("transcript_id"),
                pl.col("global_x").alias("x"),
                pl.col("global_y").alias("y"),
                pl.col("gene").alias("name"),
            ]
        ).select(["name", "x", "y"])

    elif technology == "Xenium":
        trx_ini = pl.read_parquet(path_trx).select(
            [
                pl.col("cell_id"),
                pl.col("transcript_id"),
                pl.col("feature_name").alias("name"),
                pl.col("x_location").alias("x"),
                pl.col("y_location").alias("y"),
            ]
        )

    # Create a list with the mapped names; if a name isn't in gene_map, keep the original.
    mapped_names = [gene_str_to_int_mapping.get(name, name) for name in trx_ini["name"]]

    # Replace the "name" column using with_columns.
    trx_ini = trx_ini.with_columns([pl.Series("name", mapped_names)])


    # Process the data in chunks and apply transformations
    all_chunks = []

    for start_row in tqdm(
        range(0, trx_ini.height, chunk_size), desc="Processing chunks"
    ):
        chunk = trx_ini.slice(start_row, chunk_size)

        points = np.hstack([chunk.select(["x", "y"]).to_numpy(), np.ones((chunk.height, 1))])
        sparse_matrix = csr_matrix(transformation_matrix)
        transformed_points = sparse_matrix.dot(points.T).T[:, :2]

        # # Apply transformation matrix to the coordinates
        # points = np.hstack(
        #     [chunk.select(["x", "y"]).to_numpy(), np.ones((chunk.height, 1))]
        # )
        # transformed_points = np.dot(points, transformation_matrix.T)[:, :2]

        # Create new transformed columns and drop original x, y columns
        transformed_chunk = chunk.with_columns(
            [
                (pl.Series(transformed_points[:, 0]) * image_scale)
                .round(2)
                .alias("transformed_x"),
                (pl.Series(transformed_points[:, 1]) * image_scale)
                .round(2)
                .alias("transformed_y"),
            ]
        ).drop(["x", "y"])
        all_chunks.append(transformed_chunk)

    # Concatenate all chunks after processing
    trx = pl.concat(all_chunks)

    return trx


def make_trx_tiles(
    technology,
    path_trx,
    path_transformation_matrix=None,
    path_trx_tiles=None,
    coarse_tile_factor=10,
    tile_size=250,
    chunk_size=1000000,
    verbose=False,
    image_scale=1,
    max_workers=1,
):
    """
    Processes transcript data by dividing it into coarse-grain and fine-grain tiles,
    applying transformations, and saving the results in a parallelized manner.

    Parameters
    ----------
    technology : str
        The technology used for generating the transcript data (e.g., "MERSCOPE" or "Xenium").
    path_trx : str
        Path to the file containing the transcript data.
    path_transformation_matrix : str
        Path to the file containing the transformation matrix (CSV file).
    path_trx_tiles : str
        Directory path where the output files (Parquet files) for each tile will be saved.
    coarse_tile_factor : int, optional
        Scaling factor of each coarse-grain tile comparing to the fine tile size.
    tile_size : int, optional
        Size of each fine-grain tile in microns (default is 250).
    chunk_size : int, optional
        Number of rows to process per chunk for memory efficiency (default is 1000000).
    verbose : bool, optional
        Flag to enable verbose output (default is False).
    image_scale : float, optional
        Scale factor to apply to the transcript coordinates (default is 0.5).
    max_workers : int, optional
        Maximum number of parallel workers for processing tiles (default is 1).

    Returns
    -------
    dict
        A dictionary containing the bounds of the processed data in both x and y directions.
    """

    if technology == 'custom':

        x_min, y_min = 0, 0
        x_max, y_max = pl.read_parquet(path_trx).select(
            [
                pl.col("x_image_coords").max().alias("x_max"),
                pl.col("y_image_coords").max().alias("y_max"),
            ]
        ).row(0)

    else:

        if not os.path.exists(path_trx_tiles):
            os.makedirs(path_trx_tiles)

        transformation_matrix = np.loadtxt(path_transformation_matrix)

        # transformed_points = np.dot(points, transformation_matrix.T)[:, :2]
        # sparse_matrix = csr_matrix(transformation_matrix)
        # transformed_points = sparse_matrix.dot(points.T).T[:, :2]

        gene_str_to_int_mapping = _get_name_mapping(
            path_transformation_matrix.replace('/micron_to_image_transform.csv',''),
            layer='transcript',
            )

        trx = transform_transcript_coordinates(
            technology, path_trx, chunk_size, transformation_matrix, image_scale, gene_str_to_int_mapping=gene_str_to_int_mapping,
        )

        # Get min and max x, y values
        x_min, y_min = 0, 0
        x_max, y_max = trx.select(
            [
                pl.col("transformed_x").max().alias("x_max"),
                pl.col("transformed_y").max().alias("y_max"),
            ]
        ).row(0)

        # Calculate the number of fine-grain tiles globally
        n_fine_tiles_x = int(np.ceil((x_max - x_min) / tile_size))
        n_fine_tiles_y = int(np.ceil((y_max - y_min) / tile_size))

        # Calculate the number of coarse-grain tiles
        n_coarse_tiles_x = int(np.ceil((x_max - x_min) / (coarse_tile_factor * tile_size)))
        n_coarse_tiles_y = int(np.ceil((y_max - y_min) / (coarse_tile_factor * tile_size)))

        # Use ThreadPoolExecutor for parallel processing of coarse-grain tiles
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for i in range(n_coarse_tiles_x):
                coarse_tile_x_min = x_min + i * (coarse_tile_factor * tile_size)
                coarse_tile_x_max = coarse_tile_x_min + (coarse_tile_factor * tile_size)

                for j in range(n_coarse_tiles_y):
                    coarse_tile_y_min = y_min + j * (coarse_tile_factor * tile_size)
                    coarse_tile_y_max = coarse_tile_y_min + (coarse_tile_factor * tile_size)

                    # Submit each coarse tile for parallel processing
                    futures.append(
                        executor.submit(
                            process_coarse_tile,
                            trx,
                            i,
                            j,
                            coarse_tile_x_min,
                            coarse_tile_x_max,
                            coarse_tile_y_min,
                            coarse_tile_y_max,
                            tile_size,
                            path_trx_tiles,
                            x_min,
                            y_min,
                            n_fine_tiles_x,
                            n_fine_tiles_y,
                            max_workers,
                        )
                    )

            # Wait for all coarse tiles to complete
            for future in tqdm(
                concurrent.futures.as_completed(futures),
                desc="Processing coarse tiles",
                unit="tile",
            ):
                future.result()  # Raise exceptions if any occurred during execution

    # Return the tile bounds
    tile_bounds = {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
    }

    return tile_bounds