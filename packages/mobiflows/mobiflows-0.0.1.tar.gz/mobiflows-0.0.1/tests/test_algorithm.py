from datetime import datetime

import polars as pl

from src.mobiflows.algorithm import Trajectory

TDF = pl.DataFrame(
    dict(
        uid=[
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
        ],
        datetime=[
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
        ],
        lon=[
            0,
            0,
            0,
            1,
            2,
            3,
            3,
            3,
            3,
            0,
            0,
            0,
            0,
            0,
            0,
            6,
            7,
            8,
            0,
            0,
            0,
            3,
            3,
            3,
            80,
            80,
            80,
            60,
            50,
            40,
            30,
            30,
            30,
            30,
            20,
            10,
            0,
            0,
            0,
            5,
            6,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
        ],
        lat=[
            3,
            3,
            3,
            4,
            5,
            6,
            6,
            6,
            6,
            3,
            3,
            3,
            3,
            3,
            3,
            16,
            17,
            18,
            3,
            3,
            3,
            6,
            6,
            6,
            8,
            8,
            8,
            6,
            5,
            4,
            3,
            3,
            3,
            3,
            2,
            1,
            3,
            3,
            3,
            8,
            9,
            6,
            6,
            6,
            6,
            6,
            6,
            6,
        ],
        v_id=[
            1000,
            1000,
            1000,
            1001,
            1002,
            1003,
            1003,
            1003,
            1003,
            1000,
            1000,
            1000,
            1000,
            1000,
            1000,
            1600,
            1700,
            1800,
            1000,
            1000,
            1000,
            1003,
            1003,
            1003,
            8000,
            8000,
            8000,
            7500,
            7000,
            6500,
            6000,
            6000,
            6000,
            6000,
            5500,
            5000,
            1000,
            1000,
            1000,
            1005,
            1006,
            1003,
            1003,
            1003,
            1003,
            1003,
            1003,
            1003,
        ],
    )
)


def test_add_trip_group():
    true_trip_groups = [
        1,
        1,
        1,
        2,
        3,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        1,
        1,
        1,
        2,
        3,
        4,
        5,
        5,
        5,
        6,
        6,
        6,
        1,
        1,
        1,
        2,
        3,
        4,
        5,
        5,
        5,
        5,
        6,
        7,
        1,
        1,
        1,
        2,
        3,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
    ]
    trajectory = Trajectory(TDF)
    tdf = trajectory._add_trip_group()
    trip_groups = tdf["trip_group"].to_list()

    assert true_trip_groups, trip_groups


def test_build_traj_trips():
    true_traj_trips = pl.DataFrame(
        dict(
            uid=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4],
            v_id=[
                1000,
                1001,
                1002,
                1003,
                1000,
                1000,
                1600,
                1700,
                1800,
                1000,
                1003,
                8000,
                7500,
                7000,
                6500,
                6000,
                5500,
                5000,
                1000,
                1005,
                1006,
                1003,
            ],
            trip_group=[
                1,
                2,
                3,
                4,
                5,
                1,
                2,
                3,
                4,
                5,
                6,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                1,
                2,
                3,
                4,
            ],
            first_time_at_origin=[
                1,
                4,
                5,
                6,
                10,
                1,
                4,
                5,
                6,
                7,
                10,
                1,
                4,
                5,
                6,
                7,
                11,
                12,
                1,
                4,
                5,
                6,
            ],
            last_time_at_origin=[
                3,
                4,
                5,
                9,
                12,
                3,
                4,
                5,
                6,
                9,
                12,
                3,
                4,
                5,
                6,
                10,
                11,
                12,
                3,
                4,
                5,
                12,
            ],
        )
    )

    trajectory = Trajectory(TDF)

    assert true_traj_trips.equals(trajectory._build_traj_trips())


def test_build_individual_flows():
    true_individual_trips = pl.DataFrame(
        dict(
            uid=[1, 1, 2, 2, 3, 4],
            origin=[1000, 1003, 1000, 1000, 8000, 1000],
            first_time_at_origin=[1, 6, 1, 7, 1, 1],
            last_time_at_origin=[3, 9, 3, 9, 3, 3],
            duration_at_origin=[2, 3, 2, 2, 2, 2],
            dest=[1003, 1000, 1000, 1003, 6000, 1003],
            first_time_at_dest=[6, 10, 7, 10, 7, 6],
            last_time_at_dest=[9, 12, 9, 12, 10, 12],
            duration_at_dest=[3, 2, 2, 2, 3, 6],
        )
    )

    base_time = datetime(2025, 1, 1, 0, 0, 0)
    us = 60_000_000
    tdf = TDF.with_columns(
        datetime=pl.lit(base_time)
        + pl.col("datetime") * pl.lit(us).cast(pl.Duration("us"))
    )
    trajectory = Trajectory(tdf)
    indiv_trips = trajectory.build_individual_flows(w=2).with_columns(
        first_time_at_origin=(
            (pl.col("first_time_at_origin") - pl.lit(base_time)) / us
        ).cast(pl.Int64),
        last_time_at_origin=(
            (pl.col("last_time_at_origin") - pl.lit(base_time)) / us
        ).cast(pl.Int64),
        duration_at_origin=(pl.col("duration_at_origin") / us).cast(pl.Int64),
        first_time_at_dest=(
            (pl.col("first_time_at_dest") - pl.lit(base_time)) / us
        ).cast(pl.Int64),
        last_time_at_dest=((pl.col("last_time_at_dest") - pl.lit(base_time)) / us).cast(
            pl.Int64
        ),
        duration_at_dest=(pl.col("duration_at_dest") / us).cast(pl.Int64),
    )

    assert true_individual_trips.equals(indiv_trips)


def test_build_voronoi_flows():
    true_voronoi_flows = pl.DataFrame(
        dict(
            origin=[1000, 1000, 8000, 1003, 1000],
            dest=[1003, 1000, 6000, 1000, 1003],
            time=[3, 3, 3, 9, 9],
            count=[2, 1, 1, 1, 1],
        )
    ).sort(by=["time", "origin", "dest"])

    base_time = datetime(2025, 1, 1, 0, 0, 0)
    us = 60_000_000
    tdf = TDF.with_columns(
        datetime=pl.lit(base_time)
        + pl.col("datetime") * pl.lit(us).cast(pl.Duration("us"))
    )
    trajectory = Trajectory(tdf)
    user_trips = trajectory.build_individual_flows(2)
    v_flows = (
        trajectory.build_voronoi_flows(user_trips)
        .with_columns(time=((pl.col("time") - pl.lit(base_time)) / us).cast(pl.Int64))
        .sort(by=["time", "origin", "dest"])
    )

    assert true_voronoi_flows.equals(v_flows)


def test_build_zipcode_flows():
    true_flows = pl.DataFrame(
        dict(
            origin=[1, 1, 2, 1, 1, 2],
            dest=[1, 2, 3, 1, 2, 1],
            time=[3, 3, 3, 9, 9, 9],
            count=[2, 1, 1, 1, 0, 0],
        )
    ).sort(by=["origin", "dest", "time", "count"])
    voronoi_zipcode_intersection_proportions = pl.DataFrame(
        dict(
            plz=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3],
            v_id=[
                1000,
                1001,
                1002,
                1003,
                5500,
                1001,
                1003,
                8000,
                1600,
                1700,
                5000,
                1005,
                1006,
                6000,
                1800,
                6500,
                7000,
                7500,
            ],
            p=[
                1.0,
                1.0,
                0.2,
                0.5,
                0.2,
                0.8,
                0.5,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
            ],
        )
    )

    base_time = datetime(2025, 1, 1, 0, 0, 0)
    us = 60_000_000
    tdf = TDF.with_columns(
        datetime=pl.lit(base_time)
        + pl.col("datetime") * pl.lit(us).cast(pl.Duration("us"))
    )
    trajectory = Trajectory(tdf)
    user_trips = trajectory.build_individual_flows(2)
    v_flows = trajectory.build_voronoi_flows(user_trips)
    flows = (
        trajectory.build_zipcode_flows(
            v_flows, voronoi_zipcode_intersection_proportions
        )
        .with_columns(time=((pl.col("time") - pl.lit(base_time)) / us).cast(pl.Int64))
        .sort(by=["origin", "dest", "time", "count"])
    )

    assert true_flows.equals(flows)
