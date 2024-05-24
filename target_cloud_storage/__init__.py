#!/usr/bin/env python3
import os
import json
import argparse
import logging

from google.cloud import storage

logger = logging.getLogger("target-cloud-storage")
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_json(path):
    with open(path) as f:
        return json.load(f)


def parse_args():
    '''Parse standard command-line args.
    Parses the command-line arguments mentioned in the SPEC and the
    BEST_PRACTICES documents:
    -c,--config     Config file
    -s,--state      State file
    -d,--discover   Run in discover mode
    -p,--properties Properties file: DEPRECATED, please use --catalog instead
    --catalog       Catalog file
    Returns the parsed args object from argparse. For each argument that
    point to JSON files (config, state, properties), we will automatically
    load and parse the JSON file.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config',
        help='Config file',
        required=True)

    args = parser.parse_args()
    if args.config:
        setattr(args, 'config_path', args.config)
        args.config = load_json(args.config)

    return args


def upload(args):
    logger.debug(f"Exporting data...")
    config = args.config
    bucket_name = config['bucket']
    target_path = config['path_prefix']
    local_path = config['input_path']

    # Upload all data in input_path to Google Cloud Storage
    storage_client = storage.Client.from_service_account_json(args.config_path)
    bucket = storage_client.bucket(bucket_name)

    for root, dirs, files in os.walk(local_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Skip certain files, can be configurable using config file
            if file in ["data.txt", "data.singer"]:
                logger.debug(f"Skipping : {bucket_name}:/{file}")
                continue
            remote_file_path = file_path.replace(local_path, target_path)

            logger.debug(f"Uploading: {bucket_name}:{remote_file_path}/{file}")

            blob = bucket.blob(remote_file_path)
            blob.upload_from_filename(file_path)

    logger.debug(f"Data exported.")


def main():
    # Parse command line arguments
    args = parse_args()

    # Upload the data
    upload(args)


if __name__ == "__main__":
    main()
