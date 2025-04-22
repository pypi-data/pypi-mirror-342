import platform
import sys
import webbrowser
from pathlib import Path

import pandas as pd
import pendulum
import typer
from loguru import logger
from platformdirs import PlatformDirs
from typing_extensions import Annotated

from . import __version__

DOCS = {
    "home": "https://qumasan.gitlab.io/haniwers/docs/",
    "version": "https://qumasan.gitlab.io/haniwers/docs/command/version/",
    "scan": "https://qumasan.gitlab.io/haniwers/docs/command/scan/",
    "fit": "https://qumasan.gitlab.io/haniwers/docs/command/fit/",
    "vth": "https://qumasan.gitlab.io/haniwers/docs/command/vth/",
    "daq": "https://qumasan.gitlab.io/haniwers/docs/command/daq/",
    "raw2tmp": "https://qumasan.gitlab.io/haniwers/docs/command/raw2tmp/",
    "run2csv": "https://qumasan.gitlab.io/haniwers/docs/command/run2csv/",
}
"""URLs of online documents"""


def _setup_logger(level="INFO") -> Path:
    """ロガーの設定"""

    format_short = (" | ").join(
        ["{time:YYYY-MM-DDTHH:mm:ss}", "<level>{level:8}</level>", "<level>{message}</level>"]
    )
    format_long = (" | ").join(
        [
            "{time:YYYY-MM-DDTHH:mm:ss}",
            "<level>{level:8}</level>",
            "<cyan>{name}.{function}:{line}</cyan>",
            "<level>{message}</level>",
        ]
    )

    # ロガーをリセット
    logger.remove()

    # stderr用
    if level in ["DEBUG"]:
        logger.add(
            sys.stderr,
            format=format_long,
            level=level,
        )
    else:
        logger.add(
            sys.stderr,
            format=format_short,
            level=level,
        )

    # ファイル出力用
    p = PlatformDirs(appname="haniwers", version=__version__)
    fname = p.user_log_path / "haniwers_log.json"
    logger.add(
        sink=fname,
        format=format_long,
        level="DEBUG",
        serialize=True,
        retention="10 days",
        rotation="1 MB",
    )
    return fname


def _open_docs(value: bool, url: str) -> None:
    """Open document with browser.

    コマンドの使い方をのドキュメントをブラウザで開く

    :Args:
        - `value (bool)`: boolean
        - `url (str)`: document URL

    :Example:

    既存コマンドに追加した``--docs``オプションのcallback関数として利用

    ```python
    typer.Option(
        "--docs",
        help=f"Open online document. ({DOCS['version']})",
        callback=lambda v: _open_docs(v, DOCS["version"]),
    )
    ```
    """
    if value:
        msg = f"Open docs with browser: {url}"
        logger.info(msg)
        webbrowser.open(url)
        raise typer.Exit()


app = typer.Typer()


@app.command()
def version(
    env: Annotated[bool, typer.Option(help="Show environment.")] = False,
    log_level: Annotated[str, typer.Option(help="Change log level.")] = "INFO",
    docs: Annotated[
        bool,
        typer.Option(
            "--docs",
            help=f"Open online document. ({DOCS['version']})",
            callback=lambda v: _open_docs(v, DOCS["version"]),
        ),
    ] = False,
):
    """Show haniwers version.

    :Args:
    - env (bool, optional): Show with environment details. Defaults to False.
    - log_level (str, optional): Log level. Defaults to "INFO".

    :Example:

    ```console
    $ haniwers version
    haniwers 0.19.1
    ```

    :Example:

    ```
    $ haniwers version --env
    haniwers 0.19.2

    Environments:

    Logs: ~/Library/Logs/haniwers/0.19.2/haniwers_log.json
    Executable: ~/.local/pipx/venvs/haniwers/bin/python
    Python: 3.12.5
    Implementation: CPython
    Compiler: Clang 15.0.0 (clang-1500.3.9.4)
    OS: macOS-14.6.1-arm64-arm-64bit
    System: darwin
    Platform: Darwin
    Kernel: 23.6.0
    Arch: arm64
    ```

    """

    fname = _setup_logger(level=log_level)

    msg = f"haniwers {__version__}"
    print(msg)
    logger.debug(msg)

    if env:
        _envs = {
            "Logs": fname,
            "Executable": sys.executable,
            "Python": platform.python_version(),
            "Implementation": platform.python_implementation(),
            "Compiler": platform.python_compiler(),
            "OS": platform.platform(),
            "System": sys.platform,
            "Platform": platform.system(),
            "Kernel": platform.release(),
            "Arch": platform.machine(),
        }

        print("\nEnvironments:\n")

        for k, v in _envs.items():
            msg = f"  {k}: {v}"
            print(msg)
            logger.debug(msg)

        print("\n")

    return


@app.command()
def docs(
    page: Annotated[
        str,
        typer.Option(
            help="Set page name.",
        ),
    ] = "home",
):
    """Open online document.

    オンラインドキュメントを開きます。

    :VersionAdded: 0.19.0

    :Example:

    ```console
    $ haniwers docs
    $ haniwers docs --page version
    $ haniwers docs --page scan
    $ haniwers docs --page fit
    $ haniwers docs --page vth
    $ haniwers docs --page daq
    $ haniwers docs --page raw2tmp
    $ haniwers docs --page run2csv
    ```

    """
    url = DOCS[page]
    _open_docs(True, url)


@app.command()
def ports(log_level: Annotated[str, typer.Option(help="Change log level")] = "INFO") -> None:
    """Search available ports and show device names.

    接続可能なポート名の一覧を表示します。
    OSECHIが接続されたポート名は、OSごとに以下のように変化します。

    - Linuxの場合: `/dev/ttyUSB0`
    - macOSの場合: `/dev/cu.usbserial-*` （CP2102N USB to UART Bridge Controller）
    - Windowsの場合: `COM3`

    :Args:
        log_level (str, optional): Log level. Defaults to "INFO".

    :Example:

    ```console
    $ haniwers ports
    | INFO     | Found 2 ports
    | INFO     | Port0: /dev/cu.Bluetooth-Incoming-Port - n/a
    | INFO     | Port1: /dev/cu.usbserial-140 - USB Serial
    ```

    """

    _setup_logger(level=log_level)

    from serial.tools import list_ports

    ports = list_ports.comports()
    n = len(ports)

    if n == 0:
        logger.warning("No ports found")
        return

    logger.info(f"Found {n} ports")

    for i, port in enumerate(ports):
        logger.info(f"Port{i}: {port}")

        logger.debug(f"{port.device=}")
        logger.debug(f"{port.name=}")
        logger.debug(f"{port.description=}")
        logger.debug(f"{port.usb_description()=}")
        logger.debug(f"{port.hwid=}")
        logger.debug(f"{port.usb_info()=}")
        logger.debug(f"{port.pid=}")
        logger.debug(f"{port.vid=}")
        logger.debug(f"{port.interface=}")
        logger.debug(f"{port.manufacturer=}")
        logger.debug(f"{port.product=}")
        logger.debug(f"{port.serial_number=}")

    for port in ports:
        if "UART" in port.description:
            logger.info(f"Please use '{port.device}' as your device path")


@app.command()
def scan(
    ch: Annotated[int, typer.Option(help="Set channel ID.")] = 0,
    duration: Annotated[int, typer.Option(help="Set duration. Unit: [sec]")] = 10,
    step: Annotated[int, typer.Option(help="Set step interval. Unit: [step]")] = 1,
    vmin: Annotated[int, typer.Option(help="Set start point. Unit: [step]")] = 250,
    vmax: Annotated[int, typer.Option(help="Set end point. Unit: [step]")] = 311,
    vstarts: Annotated[
        str, typer.Option(help="Comma-separated start thresholds per channel.")
    ] = "250,250,250",
    nsteps: Annotated[int, typer.Option(help="Number of threshold steps.")] = 50,
    quiet: Annotated[bool, typer.Option(help="Quiet mode.")] = False,
    load_from: Annotated[str, typer.Option(help="Set filename.")] = "scan.toml",
    log_level: Annotated[str, typer.Option(help="Change log level.")] = "INFO",
    docs: Annotated[
        bool,
        typer.Option(
            "--docs",
            help=f"Open online document. ({DOCS['scan']})",
            callback=lambda v: _open_docs(v, DOCS["scan"]),
        ),
    ] = False,
) -> None:
    """スレッショルド測定

    :Args:
        - `ch (int, optional)`: チャンネル番号. Defaults to 0.
        - `duration (int, optional)`: 1点あたりの測定時間（秒）. Defaults to 10.
        - `step (int, optional)`: 測定間隔. Defaults to 1.
        - `vmin (int, optional)`: 測定範囲（最小値）. Defaults to 250. -> deprecated.
        - `vmax (int, optional)`: 測定範囲（最大値）. Defaults to 311. -> deprecated.
        - `nsteps (int, optional`): 測定するステップ数. Defaults to 50.
        - `vstarts (str, optional`): 測定開始する値3つ. Defaults to "250,250,250"
        - `quiet (bool, optional)`: _description_. Defaults to False.
        - `load_from (str, optional)`: 設定ファイル. Defaults to "scan.toml".

    :Example:

    ```console
    $ haniwers scan
    $ haniwers scan --ch 1
    $ haniwers scan --duration=30
    $ haniwers scan --step=5
    $ haniwers scan --step=10 --vmin=200 --vmin=400

    """
    from .config import Daq
    from .threshold import scan_thresholds

    _setup_logger(level=log_level)

    # オプション解析

    # vminとvmaxが設定（＝初期値以外）の場合はエラーにする
    if vmin != 250 or vmax != 311:
        msg = "--vmin and --vmax are deprecated. Use --vstarts, --step, and --nsteps instead."
        logger.error(msg)
        raise typer.BadParameter(msg)

    if ch == 0:
        channels = [1, 2, 3]
    else:
        channels = [ch]

    # 開始点を取得
    try:
        vmins = [int(v.strip()) for v in vstarts.split(",")]
    except Exception:
        logger.error(f"Invalid format for --vstarts: {vstarts}")
        raise typer.BadParameter("Invalid format for --vstarts. Use comma-separated numbers.")

    # 開始点の数とチャンネル数が一致していない場合はエラーにする
    if (len(vmins)) != len(channels):
        logger.error("Number of vstart values must match the number of channels")
        raise typer.Exit(code=1)

    daq = Daq()
    daq.load_toml(load_from)
    daq.quiet = quiet

    now = pendulum.now().format("YYYYMMDD")
    daq.saved = str(Path(daq.saved) / now)

    for i, ch in enumerate(channels):
        start = vmins[i]
        stop = start + nsteps * step
        thresholds = list(range(start, stop, step))
        msg = f"Running threshold scan on ch{ch}."
        logger.info(msg)
        scan_thresholds(daq, duration, ch, thresholds)

    return


@app.command()
def fit(
    read_from: Annotated[str, typer.Argument(help="Set directory.")],
    params: Annotated[
        str, typer.Option(help="Set initial fit parameters (commma separated string).")
    ] = "10,300,1,1",
    search_pattern: Annotated[str, typer.Option(help="Set filename.")] = "threshold_scan.csv",
    ch: Annotated[int, typer.Option(help="Set channel ID")] = 0,
    log_level: Annotated[str, typer.Option(help="Change log level")] = "INFO",
    docs: Annotated[
        bool,
        typer.Option(
            "--docs",
            help=f"Open online document. ({DOCS['fit']})",
            callback=lambda v: _open_docs(v, DOCS["fit"]),
        ),
    ] = False,
):
    """スレッショルド計算

    スレッショルドを測定したデータから、誤差関数を使って閾値の推定値を計算します。
    チャンネル番号を指定できます。
    デフォルトはすべてのチャンネルの推定値を計算します。
    計算するたびにその結果は``thresholds_history.csv``に追記されます。
    また、最新のフィット結果は``thresholds_latest.csv``に保存されます。
    このファイルを使ってスレッショルドを設定できるようになっています。

    :Args:
        - `read_from (str)`: スレッショルド測定データがあるディレクトリ名を指定してください
        - `search_pattern (str, optional)`: スレッショルド測定データのファイル名を変更できます。Defaults to "threshold_scan.csv".
        - `ch (int, optional)`: チャンネル番号を変更できます。Defaults to 0.
        - `params (str, optional)`: フィット関数の初期パラメーターです。Defaults to "10, 300, 1,1"

    :Example:

    ```console
    $ haniwers fit ディレクトリ名
    ```
    """
    import pandas as pd

    from .preprocess import get_fnames
    from .threshold import fit_thresholds

    _setup_logger(level=log_level)

    try:
        p0 = [float(x.strip()) for x in params.split(",")]
    except Exception:
        logger.error(f"Invalid format for --params: {params}")
        raise typer.BadParameter("Invalid format for --params. Use comma-separated numbers.")

    logger.info(f"Read data from {read_from}")
    fnames = get_fnames(
        read_from,
        search_pattern,
    )

    # ファイルが見つからない時は、なにもしない
    if len(fnames) == 0:
        logger.error("No files found.")
        return

    logger.debug(fnames)

    # チャンネル番号が範囲外のときは、なにもしない
    if ch > 3:
        logger.error(f"Out of range!: {ch}")
        return

    channels = [ch]
    if ch == 0:
        channels = [1, 2, 3]

    names = ["time", "duration", "ch", "vth", "events", "tmp", "atm", "hmd"]
    data = pd.read_csv(fnames[0], names=names, parse_dates=["time"])
    thresholds = fit_thresholds(data, channels, p0)

    # 実行した時刻を上書きする
    now = pendulum.now()
    thresholds["timestamp"] = now
    print(thresholds)

    fname = "thresholds_history.csv"
    thresholds.to_csv(fname, index=False, mode="a", header=None)
    logger.info(f"Saved to {fname}")
    fname = "thresholds_latest.csv"
    thresholds.to_csv(fname, index=False)
    logger.info(f"Saved to {fname}")

    return


@app.command()
def vth(
    ch: Annotated[int, typer.Option(help="Set channel ID")] = 0,
    vth: Annotated[int, typer.Option(help="Set threshold value.")] = 0,
    max_retry: Annotated[int, typer.Option(help="Set numbers to retry.")] = 3,
    load_from: Annotated[str, typer.Option(help="Set filename.")] = "daq.toml",
    log_level: Annotated[str, typer.Option(help="Change log level.")] = "INFO",
    docs: Annotated[
        bool,
        typer.Option(
            "--docs",
            help=f"Open online document. ({DOCS['vth']})",
            callback=lambda v: _open_docs(v, DOCS["vth"]),
        ),
    ] = False,
) -> None:
    """スレッショルド設定

    各チャンネルにスレッショルドを設定します。
    カレントディレクトリにある ``thresholds_latest.csv`` を参考に、
    スレッショルド値の最良推定値を設定します。
    1step = 4mVに相当します。

    原因がまだわかってないですが、スレッショルドの書き込みに失敗することがあります。
    その場合は、書き込みに成功するまで``max_retry``回リトライします。デフォルトは3回です。

    :Args:
        - `ch (int, optional)`: チャンネル番号. Defaults to 0 (=all).
        - `vth (int, optional)`: スレッショルド値. Defaults to 0 (=all).
        - `max_retry (int, optional)`: スレッショルドの書き込みに失敗したときにリトライする回数. Defaults to 3.
        - `load_from (str, optional)`: 設定ファイル. Defaults to "daq.toml".

    :Example:

    すべてのチャンネルをまとめて設定

    ```console
    $ haniwers vth
    ```

    :Example:

    チャンネルごとに個別に設定

    ```console
    $ haniwers vth --ch 1 --vth 278
    $ haniwers vth --ch 2 --vth 268
    $ haniwers vth --ch 3 --vth 300
    ```

    """

    from .config import Daq
    from .daq import set_vth_retry

    _setup_logger(level=log_level)

    daq = Daq()
    daq.load_toml(load_from)

    now = pendulum.now().format("YYYYMMDD")
    daq.saved = str(Path(daq.saved) / now)

    # 個別のチャンネルにスレッショルドを設定する
    if ch in range(1, 4) and vth > 0:
        logger.debug(f"Set threshold to each channel: {ch} -> {vth}")
        set_vth_retry(daq, ch, vth, max_retry)
        return

    # 引数を指定しない場合は
    # すべてのチャンネルに規定のスレッショルドを設定する
    if ch == 0 and vth == 0:
        # スレッショルド値をファイルから読み込む
        fname = Path("thresholds_latest.csv")
        if not fname.exists():
            logger.error(f"No file found. Please create {fname}")
            return

        names = ["ch", "3sigma"]
        thresholds = pd.read_csv(fname)[names]

        for _, row in thresholds.iterrows():
            ch = int(row["ch"])
            vth = int(row["3sigma"])
            logger.debug(f"Set threshold to channels: {ch} -> {vth}")
            set_vth_retry(daq, ch, vth, max_retry)
        return

    # オプション指定が間違っている
    logger.error("Invalid arguments")
    return


@app.command()
def daq(
    quiet: Annotated[bool, typer.Option(help="Quiet mode.")] = False,
    load_from: Annotated[str, typer.Option(help="Set filename.")] = "daq.toml",
    log_level: Annotated[str, typer.Option(help="Change log level")] = "INFO",
    docs: Annotated[
        bool,
        typer.Option(
            "--docs",
            help=f"Open online document. ({DOCS['daq']})",
            callback=lambda v: _open_docs(v, DOCS["daq"]),
        ),
    ] = False,
) -> None:
    """Start DAQ. Set up with daq.toml.

    :Args:
        - `quiet (bool, optional)`: quiet mode. Defaults to False.
        - `load_from (str, optional)`: 設定ファイル. Defaults to "daq.toml".

    :Example:

    ```console
    $ haniwers daq
    ```
    """
    from .config import Daq
    from .daq import open_serial_connection, run

    # ログレベルを設定
    _setup_logger(level=log_level)

    # DAQの初期設定
    args = Daq()
    args.load_toml(load_from)
    args.quiet = quiet

    # データの保存先をymdに変更
    now = pendulum.now().format("YYYYMMDD")
    args.saved = str(Path(args.saved) / now)

    with open_serial_connection(args) as port:
        run(port, args)

    return


@app.command()
def raw2tmp(
    read_from: Annotated[str, typer.Argument(help="Set directory.")],
    search_pattern: Annotated[str, typer.Option(help="Set search pattern.")] = "*.csv",
    interval: Annotated[int, typer.Option(help="Set resample interval. Unit: [sec]")] = 600,
    offset: Annotated[int, typer.Option(help="Set datetime offset. Unit: [sec]")] = 0,
    tz: Annotated[str, typer.Option(help="Set time-zone.")] = "UTC+09:00",
    log_level: Annotated[str, typer.Option(help="Change log level.")] = "INFO",
    docs: Annotated[
        bool,
        typer.Option(
            "--docs",
            help=f"Open online document. ({DOCS['raw2tmp']})",
            callback=lambda v: _open_docs(v, DOCS["raw2tmp"]),
        ),
    ] = False,
) -> None:
    """Parse raw_data into CSV format. Should be used temporarily for quick analysis.

    宇宙線を測定したデータをその場で確認するために、生データを変換するための簡易コマンドです。
    必要最低限のオプションしか変更できないようになっています。
    出力ファイル名（``tmp_raw2tmp.csv``）は固定で、変更できません。
    きちんとしたデータ解析には ``haniwers run2csv`` を使って変換してください。

    :Args:
        - `read_from (str)`: 測定データがあるディレクトリ名
        - `search_pattern (str, optional)`: 検索パターン. Defaults to "*.csv".
        - `interval (int, optional)`: リサンプル間隔. Defaults to 600.
        - `offset (int, optional)`: 測定時刻のオフセット. Defaults to 0.
        - `tz (str, optional)`: 測定時刻のタイムゾーン. Defaults to "UTC+09:00".

    :Example:

    ```console
    $ haniwers raw2tmp ディレクトリ名
    $ haniwers raw2tmp ディレクトリ名 --search-pattern="*.dat"
    $ haniwers raw2tmp ディレクトリ名 --interval=10
    $ haniwers raw2tmp ディレクトリ名 --offset=36480
    $ haniwers raw2tmp ディレクトリ名 --tz="UTC+09:00"
    ```
    """
    from .preprocess import get_fnames, raw2csv

    _setup_logger(level=log_level)

    logger.info(f"Read data from {read_from}")
    fnames = get_fnames(read_from, search_pattern)
    gzip, csv = raw2csv(fnames, interval, offset, tz)
    logger.debug(f"raw2gz = {len(gzip)}")
    logger.debug(f"raw2csv = {len(csv)}")

    fname = "tmp_raw2tmp.csv.gz"
    gzip.to_csv(fname, index=False, compression="gzip")
    logger.info(f"Save data to: {fname} ({len(gzip)} rows).")

    fname = "tmp_raw2tmp.csv"
    csv.to_csv(fname, index=False)
    logger.info(f"Save data to: {fname} ({len(csv)} rows).")


@app.command()
def run2csv(
    run_id: Annotated[int, typer.Argument(help="Run ID")],
    save: Annotated[bool, typer.Option(help="Set True to save dataframes.")] = False,
    load_from: Annotated[str, typer.Option(help="Set filename.")] = "runs.csv",
    drive: Annotated[str, typer.Option(help="Set directory.")] = "../data",
    log_level: Annotated[str, typer.Option(help="Change log level")] = "INFO",
    docs: Annotated[
        bool,
        typer.Option(
            "--docs",
            help=f"Open online document. ({DOCS['run2csv']})",
            callback=lambda v: _open_docs(v, DOCS["run2csv"]),
        ),
    ] = False,
) -> None:
    """Parse raw_data into CSV format. Specify RunID.

    :Args:
        - `run_id (int)`: ラン番号
        - `save (bool, optional)`: 保存ファイル名（CSV形式）. Defaults to False.
        - `load_from (str, optional)`: RunDataの設定ファイル. Defaults to `"runs.csv"`.
        - `drive (str, optional)`: 設定ファイルがあるディレクトリ. Defaults to `"../data"`.

    :Example:

    ```console
    $ haniwers run2csv 98
    $ haniwers run2csv 98 --save
    $ haniwers run2csv 98 --drive="../data" --load_from="runs.csv"
    ```

    :Example:

    無効なラン番号を指定した場合は、処理せず終了

    ```console
    $ haniwers run2csv 200
    | INFO     | Load config from: runs.csv.
    | INFO     | Get RunData: 200.
    | ERROR    | Run #200 is out of range. Quit.
    | WARNING  | Check or Fix configuration file: ../data/runs.csv.
    ```

    """

    from .config import RunManager
    from .preprocess import run2csv

    _setup_logger(level="INFO")
    rm = RunManager(load_from=load_from, drive=drive)
    msg = f"Load config from: {load_from}."
    logger.info(msg)

    msg = f"Get RunData: {run_id}."
    logger.info(msg)

    run = rm.get_run(run_id)
    logger.info(f"description: {run.description}")
    logger.info(f"read_from: {run.read_from}")
    logger.debug(f"srcf: {run.srcf}")

    gzip, csv = run2csv(run)
    if save:
        fname = run.raw2gz
        gzip.to_csv(fname, index=False, compression="gzip")
        logger.info(f"Save data to: {fname} ({len(gzip)} rows).")
        fname = run.raw2csv
        csv.to_csv(fname, index=False)
        logger.info(f"Save data to: {fname} ({len(csv)} rows).")
    else:
        logger.warning("No data saved. Add --save to save data.")
        logger.debug(f"gzip: {len(gzip)}.")
        logger.debug(f"csv:  {len(csv)}.")


@app.command()
def mock_daq(
    quiet: Annotated[bool, typer.Option(help="Quied mode.")] = False,
    load_from: Annotated[str, typer.Option(help="Set filename")] = "daq.toml",
    log_level: Annotated[str, typer.Option(help="Change log level")] = "DEBUG",
):
    """Dummy DAQ

    シリアル通信をモックして、OSECHIがない場合でもデータを作成できるようにしたコマンド。
    デバッグ用に使う時があるかもしれない。

    """
    from unittest.mock import MagicMock, patch

    import serial

    from .config import Daq
    from .daq import run
    from .mimic import FakeEvent

    # ログレベルを設定
    _setup_logger(level=log_level)
    logger.debug("mock-daq")

    # DAQの初期設定
    args = Daq()
    args.load_toml(load_from)
    args.quiet = quiet

    # データの保存先をymdに変更
    now = pendulum.now().format("YYYYMMDD")
    args.saved = str(Path(args.saved) / now)
    args.max_rows = 10
    args.max_files = 5
    logger.debug(args)

    # シリアル通信をモック
    mock_port = MagicMock()
    mock_port.readline().decode.return_value = FakeEvent().to_mock_string()
    mock_port.name.return_value = "mock"

    with patch("serial.Serial", return_value=mock_port):
        with serial.Serial() as port:
            logger.debug(f"Port opened: {port.name}")
            run(port, args)
    logger.debug(f"Port closed: {port.name}")


if __name__ == "__main__":
    app()
