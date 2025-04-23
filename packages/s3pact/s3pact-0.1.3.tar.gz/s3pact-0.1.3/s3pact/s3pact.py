#!/usr/bin/env python3
import boto3
import botocore
import logging
import argparse
import locale
import os
import concurrent.futures

logging.basicConfig()
logger = logging.getLogger("s3pact")
logger.setLevel(logging.INFO)

locale.setlocale(locale.LC_ALL, "")

MAX_S3_WORKERS = 20


def get_args():
    description = "S3 Parallel Action\n\n"
    description += "Output:\n Key, Key Version, Key Size, Key Date, Is Latest/Current, Number of returned objects, Size of returned objects, Action Status"
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Warning Note: rm 'action' using 'versions' option remove specific object version/s and DO NOT CREATE DELETE MARKER!!!",
    )

    # common parser
    parser.add_argument("--region", help="Region", type=str)
    parser.add_argument("--profile", help="AWS Profile", type=str)
    parser.add_argument(
        "-w",
        "--max-s3-workers",
        help=f"Max S3 Workers to use [{MAX_S3_WORKERS}]",
        type=int,
        default=MAX_S3_WORKERS,
    )
    parser.add_argument("--stop-on-error", help="Stop on Action Error")

    # subparser
    subparsers = parser.add_subparsers(
        help="Desired Action", required=True, dest="action"
    )

    # parent parser args
    parent_parser = argparse.ArgumentParser(add_help=False)

    parent_parser.add_argument(
        "-p",
        "--prefix",
        help="S3 key Prefix",
        default="",
    )
    parent_parser.add_argument("-b", "--bucket", help="Bucket", required=True)
    parent_parser.add_argument("--dry", help="Dry Run", action="store_true")
    parent_parser.add_argument(
        "--skip-current-version",
        help="Do not act on Current Version",
        action="store_true",
    )
    parent_parser.add_argument("--start-after", help="Start after the specified key")
    parent_parser.add_argument("--key", help="Act only on this key")

    # key version/marker group
    kv_group = parent_parser.add_mutually_exclusive_group()
    kv_group.add_argument(
        "--key-version", help="For key option, act only on this specific version"
    )
    kv_group.add_argument(
        "--version-id-marker",
        help="For the start-after key, act on versions older than this one only",
    )

    # versions/delete-marker group
    vm_group = parent_parser.add_mutually_exclusive_group()
    vm_group.add_argument(
        "--delete-marker", help="Act ONLY on DeleteMarkers", action="store_true"
    )
    vm_group.add_argument(
        "--versions", help="Act on Non-Current Versions", action="store_true"
    )

    # ls parser
    subparsers.add_parser(
        "ls",
        parents=[parent_parser],
        help="List s3 keys versions and optionally DeleteMarker",
    )

    # rm parser
    subparsers.add_parser(
        "rm",
        parents=[parent_parser],
        help="Remove s3 keys, optionally versions and delete marker",
    )

    # tag parser
    parser_tag = subparsers.add_parser(
        "tag",
        parents=[parent_parser],
        help="Tag s3 keys, optionally versions and delete marker",
    )
    parser_tag.add_argument("--tag-name", help="Tag Name", required=True)
    parser_tag.add_argument("--tag-value", help="Tag Value", required=True)

    # cp parser
    parser_cp = subparsers.add_parser(
        "cp",
        parents=[parent_parser],
        help="Copy Key from Bucket to SourceBucket",
    )
    parser_cp.add_argument(
        "-d", "--dest-bucket", help="Destination Bucket", required=True
    )
    parser_cp.add_argument(
        "--dest-prefix", help="put keys under this prefix on destination Bucket"
    )
    parser_cp.add_argument("--dest-region", help="Destination Region")

    # download parser
    parser_dl = subparsers.add_parser(
        "dl",
        parents=[parent_parser],
        help="Download Key from Bucket to local dir",
    )
    parser_dl.add_argument(
        "-d",
        "--directory",
        help="directory where to download files",
        default=os.getcwd(),
    )

    # upload parser
    parser_ul = subparsers.add_parser(
        "ul",
        parents=[parent_parser],
        help="Upload file/dir to S3 Bucket",
    )
    parser_ul.add_argument(
        "-s",
        "--source",
        required=True,
        help="Source file/dir to upload",
        default=os.getcwd(),
    )
    parser_ul.add_argument(
        "-c",
        "--storage-class",
        help="Storage class",
        choices=[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
            "OUTPOSTS",
            "GLACIER_IR",
            "SNOW",
            "EXPRESS_ONEZONE",
        ],
        default="STANDARD",
    )
    parser_ul.add_argument(
        "-d", "--dest-prefix", help="put files under this prefix on destination Bucket"
    )

    args = parser.parse_args()
    return args


def human_readable_size(size, decimal_places=2):
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def execute_s3_action(args, kwargs, client, data):
    date = data["date"]
    n_tot = data["n_tot"]
    key = src_key = data["key"]
    version_id = data["version"]
    s_tot = human_readable_size(data["s_tot"])
    key_size = human_readable_size(data["size"])

    if args.action in ["cp", "ul"] and args.dest_prefix:
        # append prefix
        key = f"{args.dest_prefix}{key}"
    if args.action == "ul":
        # strip full path prefix "before" last dir of args.source
        key = key.replace(f"{os.path.dirname(args.source)}/", "")

    try:
        if args.dry or args.action == "ls":
            pass
        elif args.action == "rm":
            kwargs["Key"] = key
            if args.versions:
                kwargs["VersionId"] = version_id
            client.delete_object(**kwargs)
        elif args.action == "tag":
            kwargs["Key"] = key
            kwargs["Tagging"] = {
                "TagSet": [
                    {
                        "Key": args.tag_name,
                        "Value": args.tag_value,
                    }
                ]
            }
            if args.versions:
                kwargs["VersionId"] = version_id
            client.put_object_tagging(**kwargs)
        elif args.action == "cp":
            kwargs["Key"] = key
            kwargs["CopySource"]["Key"] = src_key
            if args.versions:
                kwargs["CopySource"]["VersionId"] = version_id
            client.copy_object(**kwargs)
        elif args.action == "dl":
            kwargs["Key"] = key
            os.makedirs(os.path.dirname(f"{args.directory}/{key}"), exist_ok=True)
            with open(f"{args.directory}/{key}", "wb") as s3_key_data:
                kwargs["Fileobj"] = s3_key_data
                client.download_fileobj(**kwargs)
        elif args.action == "ul":
            kwargs["Key"] = key
            kwargs["ExtraArgs"] = {"StorageClass": args.storage_class}
            with open(src_key, "rb") as f:
                kwargs["Fileobj"] = f
                client.upload_fileobj(**kwargs)

    except Exception as e:
        status = f"ERROR [{e}]"
    else:
        status = "OK [DRY]" if args.dry else "OK"

    return {
        "KEY": key,
        "KV": version_id,
        "KS": key_size,
        "KD": f"{date}",
        "L/C": data["latest"],
        "N": f"{n_tot:n}",
        "S": s_tot,
        "STATUS": status,
    }


def get_kwargs_clients(args):
    k_s3_ls = {}
    k_s3_act = {}
    k_s3_act_cfg = {}

    if args.region:
        k_s3_ls["region_name"] = args.region
        k_s3_act_cfg["region_name"] = args.region
    if args.profile:
        k_s3_ls["profile_name"] = args.profile
        k_s3_act_cfg["profile_name"] = args.profile

    k_s3_act_cfg["max_pool_connections"] = args.max_s3_workers
    if args.action == "cp" and args.dest_region:
        k_s3_act_cfg["region_name"] = args.dest_region
    k_s3_act["config"] = botocore.client.Config(**k_s3_act_cfg)

    return k_s3_ls, k_s3_act


def get_kwargs_ls(args):
    k = {"Bucket": args.bucket}
    if args.prefix:
        k["Prefix"] = args.prefix
    if args.start_after:
        k["KeyMarker"] = args.start_after
        if args.version_id_marker:
            k["VersionIdMarker"] = args.version_id_marker
    return k


def get_kwargs_acts(args):
    k = {"Bucket": args.bucket}
    if args.action == "cp":
        k["Bucket"] = args.dest_bucket
        k["CopySource"] = {
            "Bucket": args.bucket,
        }
    return k


def reverse_versions(objs):
    resp = []
    list_versions = []
    s3_key_before = None
    for o in objs:
        s3_key = o.get("Key")
        if s3_key_before != s3_key and list_versions:
            list_versions.reverse()
            resp.extend(list_versions)
            list_versions.clear()
        list_versions.append(o)
        s3_key_before = s3_key

    # need to invert
    list_versions.reverse()

    # and append the last obj versions or i will miss it
    return resp + list_versions


def act_on_key(args, kwargs_s3_client_ls, kwargs_s3_action, s3_client_action):
    kwargs_s3_get = {
        "Bucket": args.bucket,
        "Key": args.key,
        "ObjectAttributes": ["ObjectSize"],
    }
    if args.key_version:
        kwargs_s3_get["VersionId"] = args.key_version

    s3_client_get = boto3.client("s3", **kwargs_s3_client_ls)
    resp = s3_client_get.get_object_attributes(**kwargs_s3_get)
    print(
        execute_s3_action(
            args,
            kwargs_s3_action,
            s3_client_action,
            {
                "key": args.key,
                "version": resp.get("VersionId"),
                "size": resp.get("ObjectSize", 0),
                "latest": False if args.key_version else True,
                "date": resp.get("LastModified"),
                "n_tot": 1,
                "s_tot": resp.get("ObjectSize", 0),
            },
        )
    )


def run():
    n_tot = s_tot = 0
    stop = False

    args = get_args()

    if args.key and (args.key_version or args.version_id_marker):
        args.versions = True
    if args.skip_current_version and not args.versions:
        return

    kwargs_s3_client_ls, kwargs_s3_client_action = get_kwargs_clients(args)
    s3_client_ls = boto3.client("s3", **kwargs_s3_client_ls)
    s3_client_action = boto3.client("s3", **kwargs_s3_client_action)

    kwargs_s3_action = get_kwargs_acts(args)

    # Act only on a specific key
    if args.key:
        if args.version_id_marker:
            # For a specific key show versions starting from marker
            args.start_after = args.key
        elif args.versions and not args.key_version:
            # For a specifi key show all versions including current
            args.prefix = args.key
        else:
            # For specific key/version show it and quit
            act_on_key(args, kwargs_s3_client_ls, kwargs_s3_action, s3_client_action)
            return

    if args.action == "ul":
        # upload action, simulate a structure like the one returned by list_object_versions
        if os.path.isfile(args.source):
            f_stat = os.stat(args.source)
            response_iterator = [
                {
                    "Versions": [
                        {"Key": args.source, "IsLatest": True, "Size": f_stat.st_size}
                    ]
                }
            ]
        elif os.path.isdir(args.source):
            response_iterator = []
            for root, _, filenames in os.walk(args.source, topdown=True):
                for name in filenames:
                    f_path = os.path.join(root, name)
                    f_stat = os.stat(f_path)
                    response_iterator.append(
                        {
                            "Versions": [
                                {
                                    "Key": os.path.join(root, name),
                                    "IsLatest": True,
                                    "Size": f_stat.st_size,
                                }
                            ]
                        }
                    )

    else:
        kwargs_s3_ls = get_kwargs_ls(args)

        paginator = s3_client_ls.get_paginator("list_object_versions")
        response_iterator = paginator.paginate(**kwargs_s3_ls)

    for r in response_iterator:
        if stop:
            break

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.max_s3_workers
        ) as executor:
            future_to_stack = {}

            if args.delete_marker:
                list_objs = r.get("DeleteMarkers", [])
            else:
                list_objs = r.get("Versions", [])
                if args.versions:
                    list_objs = reverse_versions(list_objs)

            for p in list_objs:
                # Act only on a specific key
                if args.key and p.get("Key") != args.key:
                    stop = True
                    break

                if args.skip_current_version and p.get("IsLatest"):
                    # skip current
                    continue
                if not args.versions and not p.get("IsLatest"):
                    # skip versions
                    continue

                n_tot += 1
                s_tot += p.get("Size", 0)
                s3_key_data = {
                    "key": p.get("Key"),
                    "version": p.get("VersionId"),
                    "size": p.get("Size", 0),
                    "latest": p.get("IsLatest"),
                    "date": p.get("LastModified"),
                    "n_tot": n_tot,
                    "s_tot": s_tot,
                }

                ex_sub = executor.submit(
                    execute_s3_action,
                    args,
                    kwargs_s3_action,
                    s3_client_action,
                    s3_key_data,
                )
                future_to_stack[ex_sub] = s3_key_data["key"]

            for future in future_to_stack:
                future_to_stack[future]
                try:
                    s3_status = future.result()
                except Exception as e:
                    logger.error(f"Found error stopping: {e}")
                    break
                else:
                    if s3_status:
                        print(s3_status)

            if args.stop_on_error:
                for future in future_to_stack:
                    future.cancel()


if __name__ == "__main__":
    run()
