import geopandas as gpd
import pandas as pd
import polars as pl


class Trajectory(pl.DataFrame):
    def __init__(
        self,
        tdf: pl.DataFrame,
        v_id_col: str = "v_id",
        time_col: str = "datetime",
        uid_col: str = "uid",
    ) -> None:
        """
        Parameters
        ----------
        tdf : pandas.DataFrame
            Trajectory data with columns [uid, datetime, lon, lat]
                with regular observations for every users (interval τ)
        v_id_col : str, optional
            Column identifying tile IDs in the tessellation dataframe
            (default is "v_id")
        time_col : str, optional
            Time column name (default "time")
        uid_col : str, optional
            User ID column name (default "uid")
        """

        super().__init__()
        self.tdf = tdf.sort(by=[uid_col, time_col])
        self.v_id = v_id_col
        self.time = time_col
        self.uid = uid_col

    def mapping(self, tessellation) -> pl.DataFrame:
        """Map (pseudo-)locations to coverage cells

        Parameters
        ----------
        tdf : pandas.DataFrame
            Trajectory data with columns [uid, datetime, lon, lat]
        tessellation : gpd.GeoDataFrame
            Tessellation, e.g., Voronoi tesselation and any coverage tessellation

        Returns
        -------
        pandas.DataFrame
            Pandas dataframe with the columns [uid, datetime, lon, lat, v_id]
        """

        gdf = gpd.GeoDataFrame(
            self.tdf.to_pandas(),
            geometry=gpd.points_from_xy(self.tdf["lon"], self.tdf["lat"]),
            crs=tessellation.crs,
        )
        joined = gpd.sjoin(
            gdf, tessellation[[self.v_id, "geometry"]], how="left", predicate="within"
        )
        gdf[self.v_id] = joined[self.v_id]

        matched = gdf[~gdf[self.v_id].isna()]
        unmatched = gdf[gdf[self.v_id].isna()]

        if not unmatched.empty:
            # build a lookup of future assigned regions per user
            tessellation = tessellation.copy()
            tessellation["rep"] = gpd.points_from_xy(
                tessellation["lon"], tessellation["lat"]
            )

            matched_sorted = matched.sort_values(by=[self.uid, self.time])
            future_region_lookup = matched_sorted.groupby(self.uid).apply(
                lambda df: df.set_index(self.time)[self.v_id]
            )

            # find candidate cells for all unmatched points (intersection test)
            unmatched["candidates"] = unmatched.geometry.apply(
                lambda geom: tessellation[tessellation.geometry.intersects(geom)][
                    [self.v_id, "rep"]
                ]
            )

            fallback_ids = []
            for _, row in unmatched.iterrows():
                uid = row[self.uid]
                time = row[self.time]

                # candidate cells at current time
                candidates = row["candidates"]
                if candidates.empty:
                    raise ValueError(
                        f"""tdf not proper: trajectory point for user {uid} at time
                            {time} intersects no tessellation cell."""
                    )

                # find user's next assigned cell
                if uid not in future_region_lookup:
                    raise ValueError(
                        f"""tdf not proper: uid {uid} does not have any point
                            assigned to a cell to a cell."""
                    )

                user_future = future_region_lookup[uid]
                future_times = user_future[user_future.index > time]

                if future_times.empty:
                    raise ValueError(
                        f"""tdf not proper: no future point for uid {uid} at time
                            {time}."""
                    )

                future_id = future_times.iloc[0]
                future_geom = tessellation.loc[
                    tessellation[self.v_id] == future_id, "rep"
                ].values[0]

                # choose closest candidate cell to the future one
                candidates["dist"] = candidates["rep"].distance(future_geom)
                fallback_id = candidates.sort_values(by="dist").iloc[0][self.v_id]
                fallback_ids.append(fallback_id)

            unmatched[self.v_id] = fallback_ids

            gdf = pd.concat(
                [matched, unmatched.drop(columns=["candidates"])], ignore_index=True
            )

        gdf.drop(columns=["geometry"], inplace=True)

        return pl.DataFrame(gdf.sort_values(by=[self.uid, self.time]))

    def _add_trip_group(self) -> pl.DataFrame:
        """Add trip group to individual trajectories.

        Returns
        -------
        polars.DataFrame
            Polars dataframe with the columns [uid, datetime, lon, lat, trip_group]
        """

        tdfs = []
        for d in self.tdf.partition_by(self.uid):
            group = 0
            prev_origin = None
            new_row = []

            for r in d.iter_rows(named=True):
                current_origin = r[self.v_id]
                if current_origin != prev_origin:
                    group = group + 1

                r["trip_group"] = group
                prev_origin = current_origin
                new_row.append(r)

            new_tdf = pl.DataFrame(new_row)
            tdfs.append(new_tdf)

        return pl.concat(tdfs).sort(by=[self.uid, self.time])

    def _build_traj_trips(self) -> pl.DataFrame:
        """Build trajectory trips

        Returns
        -------
        polars.DataFrame
            Polars dataframe with the columns
            [uid, v_id, trip_group, first_time_at_origin, last_time_at_origin]
        """

        tdf = self._add_trip_group()

        tdf = (
            tdf.group_by([self.uid, self.v_id, "trip_group"])
            .agg(
                first_time_at_origin=pl.col(self.time).first(),
                last_time_at_origin=pl.col(self.time).last(),
            )
            .sort(by=[self.uid, "first_time_at_origin"])
        )

        return tdf

    def build_individual_flows(
        self,
        w: int = 60,
    ) -> pl.DataFrame:
        """Build individual flows

        Parameters
        ----------
        w : int
            Duration at a location used to define a trip

        Returns
        -------
        polars.DataFrame
            Polars dataframe with the columns
                [uid, origin, first_time_at_origin, last_time_at_origin,
                duration_at_origin, dest, first_time_at_dest, last_time_at_dest,
                duration_at_dest]
        """

        tdf = self._build_traj_trips()

        flows = tdf.with_columns(
            dest=pl.col(self.v_id).shift(-1),
            next_uid=pl.col(self.uid).shift(-1),
            first_time_at_dest=pl.col("first_time_at_origin").shift(-1),
            last_time_at_dest=pl.col("last_time_at_origin").shift(-1),
        )

        flows = flows.rename({self.v_id: "origin"})

        flows = flows.filter(pl.col("uid") == pl.col("next_uid"))

        flows = flows.with_columns(
            duration_at_origin=pl.col("last_time_at_origin")
            - pl.col("first_time_at_origin"),
            duration_at_dest=pl.col("last_time_at_dest") - pl.col("first_time_at_dest"),
        )

        # where you spent at least `w` minutes.
        flows_relevant = flows.filter(
            (pl.col("duration_at_origin") >= pl.duration(minutes=w))
            | (pl.col("duration_at_dest") >= pl.duration(minutes=w))
        )
        flows_relevant = flows_relevant.with_columns(index=pl.col("uid").cum_count())

        # index of the start flow where a user spent less than `w` minutes
        bad_start_flows_index = (
            flows_relevant.filter(
                (
                    (pl.col("duration_at_origin") < pl.duration(minutes=w))
                    & (pl.col("uid").is_first_distinct().over("uid"))
                )
            )
            .select(pl.col("index"))
            .to_series()
            .to_list()
        )
        bad_stop_flows_index = (
            flows_relevant.reverse()
            .filter(
                (
                    (pl.col("duration_at_dest") < pl.duration(minutes=w))
                    & (pl.col("uid").is_first_distinct().over("uid"))
                )
            )
            .select(pl.col("index"))
            .to_series()
            .to_list()
        )

        to_remove = bad_start_flows_index + bad_stop_flows_index
        flows_relevant = flows_relevant.filter(
            ~pl.col("index").is_in(to_remove)
        )  # removes flows with bad global origins and destinations

        flows_of_interest_origins = flows_relevant.filter(
            (pl.col("duration_at_origin") >= pl.duration(minutes=w))
        ).select(
            [
                "uid",
                "origin",
                "first_time_at_origin",
                "last_time_at_origin",
                "duration_at_origin",
            ]
        )
        flows_of_interest_dests = flows_relevant.filter(
            (pl.col("duration_at_dest") >= pl.duration(minutes=w))
        ).select(
            [
                "dest",
                "first_time_at_dest",
                "last_time_at_dest",
                "duration_at_dest",
            ]
        )

        assert len(flows_of_interest_origins) == len(flows_of_interest_dests)

        flows_of_interest = pl.concat(
            [flows_of_interest_origins, flows_of_interest_dests], how="horizontal"
        )

        # TODO: self-loops
        # we do not remove self-loops as they count trips where an individual doesn't spend much time  e.g., <30 min, when that is our `w` outside
        # flows_of_interest = flows_of_interest.filter(pl.col("origin") != pl.col("dest"))

        flows_of_interest.sort(by=["uid", "first_time_at_dest"])

        return flows_of_interest

    def build_voronoi_flows(self, user_trips: pl.DataFrame) -> pl.DataFrame:
        """build voronoi flows

        Parameters
        ----------
        user_trips : polars.DataFrame
            Polars dataframe with the columns
                [uid, origin, first_time_at_origin, last_time_at_origin,
                duration_at_origin, dest, first_time_at_dest, last_time_at_dest,
                duration_at_dest]
                gotten from build_individual_flows(), for example.

        Returns
        -------
        polars.DataFrame
            Polars dataframe with the columns
                [origin, dest, time]
        """

        # the time column is the time at which an individual leaves his origin location
        individual_flows = user_trips.with_columns(time=pl.col("last_time_at_origin"))

        flows = (
            individual_flows.group_by(["origin", "dest", "time"])
            .agg(count=pl.len())
            .sort(by="time")
        )

        return flows

    def build_zipcode_flows(
        self,
        cell_flows: pl.DataFrame,
        voronoi_zipcode_intersection_proportions: pl.DataFrame,
    ) -> pl.DataFrame:
        """build zipcode flows"""

        flows = (
            (
                cell_flows.join(
                    voronoi_zipcode_intersection_proportions,
                    left_on="origin",
                    right_on="v_id",
                    suffix="_origin",
                    how="left",
                )
                .join(
                    voronoi_zipcode_intersection_proportions,
                    left_on="dest",
                    right_on="v_id",
                    suffix="_dest",
                    how="left",
                )
                .rename({"p": "p_origin", "plz": "plz_origin"})
                .with_columns(p=pl.col("p_origin") * pl.col("p_dest"))
                .with_columns(count_avg=pl.col("p") * pl.col("count"))
                .select(
                    origin=pl.col("plz_origin"),
                    dest=pl.col("plz_dest"),
                    time=pl.col("time"),
                    p=pl.col("p"),
                    count_avg=pl.col("count_avg"),
                )
            )
            .group_by(["origin", "dest", "time"])
            .agg(count_avg=pl.sum("count_avg"))
            .with_columns(count=pl.col("count_avg").floor().cast(pl.Int64))
            .select(["origin", "dest", "time", "count"])
        )

        return flows
