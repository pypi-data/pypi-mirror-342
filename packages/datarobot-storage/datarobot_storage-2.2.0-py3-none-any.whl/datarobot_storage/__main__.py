import argparse
import sys

from datarobot_storage import get_storage

parser = argparse.ArgumentParser(
    description='DataRobot common storage utility', prog='datarobot_storage'
)

subparsers = parser.add_subparsers(
    title='Available actions', metavar='ACTION', required=True, dest='action'
)

parser.add_argument('-v', '--verbose', action='store_true', help='Print additional info')

list_parser = subparsers.add_parser('list', help='List remote objects')
list_parser.add_argument('prefix', help='remote prefix', metavar='PREFIX')

delete_parser = subparsers.add_parser('delete', help='Delete single remote object')
delete_parser.add_argument('key', help='object key to delete', metavar='KEY')

get_parser = subparsers.add_parser('get', help='Download remote object locally')
get_parser.add_argument('remote', help='remote object key', metavar='REMOTE')
get_parser.add_argument('local', help='local file path', metavar='LOCAL')

put_parser = subparsers.add_parser('put', help='Upload local file to storage')
put_parser.add_argument('local', help='local file to upload', metavar='LOCAL')
put_parser.add_argument('remote', help='remote destination', metavar='REMOTE')


if __name__ == '__main__':
    args = parser.parse_args()
    success = False
    storage = get_storage()

    if args.verbose:
        print(repr(storage))

    if args.action == 'list':
        args.verbose and print(f"List files in {args.prefix}")

        # Strip leading slash
        prefix = args.prefix[1:] if args.prefix.startswith('/') else args.prefix

        for key in storage.list(prefix):
            print(key)
        success = True

    if args.action == 'delete':
        args.verbose and print(f"Delete files under {args.key}")
        success = storage.delete(args.key)

    if args.action == 'get':
        args.verbose and print(f"Get {args.remote} -> {args.local}")
        success = storage.get(args.remote, args.local)

    if args.action == 'put':
        args.verbose and print(f"Put {args.local} -> {args.remote}")
        success = storage.put(args.remote, args.local)

    sys.exit(int(not success))
