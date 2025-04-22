import time
from pathlib import Path

import eikon as ek
import pandas as pd


def get_series(
    api_key: str,
    series_id_list: list[str],
    start_date: str,
    end_date: str,
    freq: str = "B",
    fields: list[str] | None = None,
    cooldown: int = 60,
    datapoint_limit: int = 2_000,
    cache_path: Path | None = None,
) -> pd.DataFrame:
    """Downloads data from eikon given that tou have a valid API key"""
    ek.set_app_key(api_key)
    fields = (
        ["TIMESTAMP", "CLOSE", "CF_LAST", "CF_YIELD"]
        if fields is None
        else fields
    )

    dates_list: list[str] = list(
        pd.date_range(start=start_date, end=end_date, freq=freq).astype("str")
    )
    partial_data: list[pd.DataFrame] = []
    download_step: int = datapoint_limit // (
        len(series_id_list) * (len(fields) - 1)
    )
    downloaded_dates: int = 0
    while downloaded_dates < len(dates_list):
        dates_to_download = dates_list[
            downloaded_dates : downloaded_dates + download_step
        ]
        start = dates_to_download[0]
        end = dates_to_download[-1]
        cache_file_path: Path = (
            cache_path / f"from_{start}_to_{end}.csv"
            if cache_path is not None
            else None
        )
        if (cache_file_path is None) or (not cache_file_path.exists()):
            data: pd.DataFrame = block_download(
                series_id_list,
                start_date=start,
                end_date=end,
                freq=freq,
                fields=fields,
                cooldown=cooldown,
                file_path=cache_file_path,
                debug=True,
            )
            if cache_file_path is None:
                partial_data.append(data)
            if downloaded_dates + download_step < len(dates_list):
                print(f"Waiting {cooldown} seconds for Eikon to cool down...")
                time.sleep(cooldown)
        downloaded_dates += download_step
    data = concat_partial_data(cache_path, partial_data)
    return data


def block_download(
    series_id_list: list[str],
    start_date: str,
    end_date: str,
    freq: str = "B",
    fields: list[str] | None = None,
    cooldown: int = 60,
    file_path: Path | None = None,
    debug: bool = False,
):
    interval = "daily" if freq == "B" else freq

    while True:
        try:
            data: pd.DataFrame | None = ek.get_timeseries(
                rics=series_id_list,
                start_date=start_date,
                end_date=end_date,
                fields=fields,
                interval=interval,
                debug=debug,
            )
            if data is None:
                raise ek.EikonError(
                    code=404, message="Service temporarily unavailable"
                )
            data = data.drop_duplicates()
            data = data.sort_index()
            if len(data.columns) == 1:
                data.columns = series_id_list
            if file_path is not None:
                data.to_csv(file_path)
            break
        except ek.EikonError as e:
            print(f"Eikon error: {e}")
            print("This is probably not our fault")
        print(f"Waiting {cooldown} seconds for Eikon to cool down...")
        time.sleep(cooldown)
    return data


def concat_partial_data(
    cache_path: Path, partial_data: list[pd.DataFrame]
) -> pd.DataFrame:
    dfs = partial_data
    if cache_path is not None:
        for chunk in cache_path.iterdir():
            df = pd.read_csv(chunk, index_col="Date")
            dfs.append(df)
    full = pd.concat(dfs)
    return full
