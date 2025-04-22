import csv
from pathlib import Path

import numpy as np
import pandas as pd
import pendulum
from loguru import logger
from scipy.optimize import curve_fit
from scipy.special import erfc
from pydantic import BaseModel

from .config import Daq
from .daq import (
    get_savef_with_timestamp,
    set_vth_retry,
    time_daq,
    scan_daq,
)


def scan_threshold(args: Daq, fname: str, duration: int) -> pd.DataFrame:
    events = scan_daq(args, fname, duration)
    # logger.debug(events)
    rows = []
    for event in events:
        rows.append(event.model_dump())
    data = pd.DataFrame(rows)
    # logger.debug(data)
    return data


def scan_threshold_by_channel(daq: Daq, duration: int, ch: int, vth: int) -> list:
    """
    Run threshold scan by channel.

    :Args:
    - `daq (Daq)`: Daqオブジェクトを指定する
    - `duration (int)`: 測定時間（秒）を指定する
    - `ch (int)`: 測定するチャンネル番号を指定する
    - `vth (int)`: スレッショルド値を指定する

    :Returns:
    - `data (list)`: [測定時刻, チャンネル番号, スレッショルド値, イベント数, 気温など]のリスト
    """

    # Try to set the threshold
    if not set_vth_retry(daq, ch, vth, 3):
        msg = f"Failed to set threshold: ch{ch} - {vth}"
        logger.error(msg)
        return []

    # Collect data
    try:
        # fidは7ケタまで使える
        fid = f"{ch:02}_{vth:04}"
        fname = get_savef_with_timestamp(daq, fid)
        rows = scan_threshold(daq, fname, duration)
        counts = len(rows)
        tmp = rows["tmp"].mean()
        atm = rows["atm"].mean()
        hmd = rows["hmd"].mean()
        msg = f"Saved data to: {fname}"
        logger.info(msg)
    except Exception as e:
        msg = f"Failed to collect data due to: {str(e)}"
        logger.error(msg)
        counts = 0
        tmp = 0
        atm = 0
        hmd = 0

    # Save Summary
    now = pendulum.now().to_iso8601_string()
    data = [now, duration, ch, vth, counts, tmp, atm, hmd]
    fname = Path(daq.saved) / daq.fname_scan
    with fname.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)
    msg = f"Added data to: {fname}"
    logger.info(msg)

    return data


def scan_thresholds_in_serial(
    daq: Daq, duration: int, ch: int, thresholds: list[int]
) -> list[list]:
    """
    Run threshold scan for all channels by default.

    :Args:
    - daq (Daq): Daqオブジェクト
    - duration (int): 測定時間（秒）
    - ch (int): チャンネル番号（1 - 3)
    - thresholds (list[int])： 測定するスレッショルド値のリスト

    :Returns:
    - rows (list[list]):  [測定時刻、チャンネル番号、スレッショルド値、イベント数]のリスト
    """

    # Estimated time for scan
    msg = f"Number of points: {len(thresholds)}"
    logger.info(msg)
    estimated_time = len(thresholds) * duration
    msg = f"Estimated time: {estimated_time} sec."
    logger.info(msg)

    # すべてのチャンネルの閾値を高くする
    set_vth_retry(daq, 1, 500, 5)
    set_vth_retry(daq, 2, 500, 5)
    set_vth_retry(daq, 3, 500, 5)

    rows = []
    n = len(thresholds)
    for i, vth in enumerate(thresholds):
        msg = "-" * 40 + f"[{i+1:2d}/{n:2d}: {vth}]"
        logger.info(msg)
        row = scan_threshold_by_channel(daq, duration, ch, vth)
        if row:
            rows.append(row)

    return rows


def scan_thresholds_in_parallel(daq: Daq, duration: int, thresholds: list[int]):
    # Estimated time for scan
    msg = f"Number of points: {len(thresholds)}"
    logger.info(msg)
    estimated_time = len(thresholds) * duration
    msg = f"Estimated time: {estimated_time} sec."
    logger.info(msg)

    n = len(thresholds)
    for i, vth in enumerate(thresholds):
        msg = "-" * 40 + f"[{i+1:2d}/{n:2d}: {vth}]"
        logger.info(msg)
        # すべてのチャンネルの閾値を設定
        set_vth_retry(daq, 1, vth, 5)
        set_vth_retry(daq, 2, vth, 5)
        set_vth_retry(daq, 3, vth, 5)

        try:
            rows = time_daq(daq, duration)
            counts = len(rows)
            tmp = rows["tmp"].mean()
            atm = rows["atm"].mean()
            hmd = rows["hmd"].mean()
            fname = get_savef_with_timestamp(daq, ch)
            rows.to_csv(fname, index=False)
            msg = f"Saved data to: {fname}"
            logger.info(msg)
        except Exception as e:
            pass
        # それっぽいものを作ってる途中


def scan_thresholds(daq: Daq, duration: int, ch: int, thresholds: list[int]) -> list[list]:
    return scan_thresholds_in_serial(daq, duration, ch, thresholds)


def erfc_function(x, a, b, c, d):
    """
    誤差補正関数（Error function complement）。

    スレショルドを計算するためのフィット関数です。

    erfc(x) = 1 - erf(x)

    Parameters
    ----------
    x : input value
    a : height
    b : mean
    c : sigma
    d : intercept
    """
    return a * erfc((x - b) / c) + d


def fit_threshold_by_channel(data: pd.DataFrame, ch: int, func, params: list[float]):
    """誤差補正関数を使ってスレッショルド値を決める

    Args:
        data (pd.DataFrame): スレッショルド測定のデータフレーム
        ch (int): スレッショルドを求めるチャンネル番号
        func (_type_): フィット関数

    Returns:
        pd.DataFrame: 閾値の提案値のデータフレーム
        pd.DataFrame: フィットしたデータフレーム
        pd.DataFrame: フィット曲線のデータフレーム
    """

    # 実行した時刻を取得する
    now = pendulum.now()

    # データフレームのカラム名を確認する
    expected_names = ["time", "duration", "ch", "vth", "events", "tmp", "atm", "hmd"]
    names = list(data.columns)
    assert names == expected_names

    # フィットの準備
    # 1. 該当するチャンネル番号のデータを抽出
    # 2. イベントレートの計算
    # 3. numpy配列に変換
    q = f"ch == {ch}"
    # print(f"----- Query: {q} -----")
    data_q = data.query(q).copy()
    data_q["event_rate"] = data_q["events"] / data_q["duration"]
    x_data = data_q["vth"]
    y_data = data_q["event_rate"]

    # フィットの初期パラメータ
    # TODO: 初期パラメータを外から調整できるようにする
    # params = [10.0, 300.0, 1.0, 1.0]

    # フィット：1回目
    popt, pcov = curve_fit(func, x_data, y_data, p0=params)
    # std = np.sqrt(np.diag(pcov))

    # logger.debug("フィット（1回目）")
    # logger.debug(f"Parameter Optimized  (popt) = {popt}")
    # logger.debug(f"Parameter Covariance (pcov) = {pcov}")
    # logger.debug(f"Parameter Std. Dev.  (std) = {std}")

    # フィット：2回目
    popt, pcov = curve_fit(func, x_data, y_data, p0=popt)
    # std = np.sqrt(np.diag(pcov))
    # logger.debug("フィット（2回目）")
    # logger.debug(f"Parameter Optimized  (popt) = {popt}")
    # logger.debug(f"Parameter Covariance (pcov) = {pcov}")
    # logger.debug(f"Parameter Std. Dev.  (std) = {std}")

    # フィット曲線
    # 1. フィットで得られた値を使って関数（numpy.array）を作成する
    # 2. データフレームに変換して返り値にする
    xmin = x_data.min()
    xmax = x_data.max()

    # logger.debug(xmin)
    # logger.debug(xmax)
    x_fit = np.arange(xmin, xmax, 0.1)
    a, b, c, d = popt
    y_fit = func(x_fit, a, b, c, d)
    data_f = pd.DataFrame(
        {
            "vth": x_fit,
            "event_rate": y_fit,
            "ch": f"fit{ch}",
        }
    )

    # フィット結果を使って閾値を計算する
    # 例：1sigma, 3sigma, 5sigma
    # pd.DataFrameに変換する
    mean, sigma = popt[1], popt[2]
    _thresholds = {
        "timestamp": now,
        "ch": ch,
        "0sigma": [round(mean)],
        "1sigma": [round(mean + 1 * sigma)],
        "3sigma": [round(mean + 3 * sigma)],
        "5sigma": [round(mean + 5 * sigma)],
    }
    thresholds = pd.DataFrame(_thresholds)

    return thresholds, data_q, data_f


def fit_thresholds(data: pd.DataFrame, channels: list[int], params: list[float]) -> pd.DataFrame:
    """スレッショルド

    Args:
        data (pd.DataFrame): スレッショルド測定のデータフレーム
        channels (list[int]): スレッショルドを計算するチャンネル番号

    Returns:
        pd.DataFrame: 計算したスレッショルド値のデータフレーム
    """
    threshold = []
    erfc = erfc_function
    for c in channels:
        _threshold, _, _ = fit_threshold_by_channel(data, ch=c, func=erfc, params=params)
        threshold.append(_threshold)

    thresholds = pd.concat(threshold, ignore_index=True)
    return thresholds
