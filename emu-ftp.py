from __future__ import annotations

import argparse
import io
import json
import os
from enum import Enum
from ftplib import FTP

import dacite

from config import Config, GameType


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=Mode, choices=list(Mode))
    parser.add_argument('game', type=GameType, choices=list(GameType))
    args = parser.parse_args()

    with open('config.json', 'r') as file:
        config = json.load(file)
        config = dacite.from_dict(Config, config)

    src_host = config.n3ds.host if args.mode == Mode.EXPORT else config.switch.host
    dst_host = config.switch.host if args.mode == Mode.EXPORT else config.n3ds.host

    src_filename = get_src_filename(config, args.mode, args.game)
    dst_filename = get_dst_filename(config, args.mode, args.game)

    with FTP() as ftp:
        ftp.connect(host=src_host, port=5000)

        data = bytearray()
        ftp.retrbinary(cmd=f'RETR {src_filename}', callback=data.extend)

    # trim save file to remove RTC data
    if len(data) > 0x8010:
        data = data[:0x8010]

    with FTP() as ftp:
        ftp.connect(host=dst_host, port=5000)
        ftp.storbinary(cmd=f'STOR {dst_filename}',
                       fp=io.BytesIO(data))


class Mode(str, Enum):
    EXPORT = 'export'
    IMPORT = 'import'

    def __str__(self) -> str:
        return self.value


def get_n3ds_file(config: Config, mode: Mode, game: GameType) -> str:
    dirname = os.path.join(config.n3ds.directory, config.n3ds.saves.get(str(game)))
    return os.path.join(dirname, str(mode).capitalize(), 'sav.dat')


def get_switch_file(config: Config, mode: Mode, game: GameType) -> str:
    return os.path.join(config.switch.directory, config.switch.saves.get(str(game)))


def get_src_filename(config: Config, mode: Mode, game: GameType) -> str:
    fn = get_n3ds_file if mode == Mode.EXPORT else get_switch_file
    return fn(config, mode, game)


def get_dst_filename(config: Config, mode: Mode, game: GameType) -> str:
    fn = get_n3ds_file if mode == Mode.IMPORT else get_switch_file
    return fn(config, mode, game)


if __name__ == '__main__':
    main()
