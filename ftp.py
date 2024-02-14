import argparse
import io
import os
from ftplib import FTP


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    shared_args = argparse.ArgumentParser(add_help=False)
    shared_args.add_argument('-p', '--port', type=int, default=5000)
    shared_args.add_argument('host')

    def init_get(p: argparse.ArgumentParser):
        p.set_defaults(func=get)
        p.add_argument('remote_file')
        p.add_argument('--local-file')

    def init_put(p: argparse.ArgumentParser):
        p.set_defaults(func=put)
        p.add_argument('local_file')
        p.add_argument('remote_file')

    init_get(subparsers.add_parser('get', parents=[shared_args]))
    init_put(subparsers.add_parser('put', parents=[shared_args]))
    args = parser.parse_args()
    args.func(args)


def get(args: argparse.Namespace):
    data = bytearray()
    with FTP() as ftp:
        ftp.connect(host=args.host, port=args.port)
        ftp.retrbinary(cmd=f'RETR {args.remote_file}', callback=data.extend)

    local_file = args.local_file or os.path.basename(args.file)
    with open(local_file, 'wb') as file:
        file.write(data)


def put(args: argparse.Namespace):
    with open(args.local_file, 'rb') as file:
        data = file.read()
    with FTP() as ftp:
        ftp.connect(host=args.host, port=args.port)
        ftp.storbinary(cmd=f'STOR {args.remote_file}',
                       fp=io.BytesIO(data))


if __name__ == '__main__':
    main()
