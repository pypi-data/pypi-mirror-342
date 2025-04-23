# Copyright 2022 Ultima Genomics Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
# DESCRIPTION
#    Validate all files defined by  workflow inputs json conf are found in google-cloud-storage

import argparse
import json
import re
import google
import subprocess
from google.cloud import storage
import boto3
import botocore
from enum import Enum
from winval.workflow_var import WorkflowVarType
from winval.wdl_parser import WdlParser
from winval import logger
from datetime import datetime, timezone


STORAGE_PREFIX_REGEX = "^^(gs|s3)://"

#StorageClass could be EXIST,MISSING,GLACIER

class StorageClass(Enum):
    EXIST = 1
    MISSING = 2
    GLACIER = 3

def get_args():
    parser = argparse.ArgumentParser('cloud_files_validator', description='Validate GCS inputs actually exist')
    parser.add_argument('--json', required=True)
    parser.add_argument('--wdl', required=True)
    return parser.parse_args()


def split_uri(uri: str):
    matches = re.match(rf"{STORAGE_PREFIX_REGEX}(.*?)/(.*)", uri)
    if matches:
        return matches.groups()
    else:
        return None, None, None


class CloudFilesValidator:

    def __init__(self, wdl_file: str, json_file: str):
        logger.debug('-----------------------------')
        logger.debug('---- CloudFilesValidator ----')
        logger.debug('-----------------------------')
        self.json_file = json_file
        self.workflow_vars = None
        wdl_inputs = WdlParser(wdl_file).parse_workflow_variables()
        self.workflow_vars = wdl_inputs.workflow_vars
        with open(json_file) as jf:
            wdl_inputs.fill_values_from_json(json.load(jf))
        self.validated_files = []
        self.non_validated_files = []
        self.glacier_files = []


    def validate(self) -> bool:
        for workflow_var in self.workflow_vars.values():
            if workflow_var.type == WorkflowVarType.FILE and workflow_var.value is not None:
                self.validate_file(workflow_var.value)
            elif workflow_var.type == WorkflowVarType.FILE_ARRAY and workflow_var.value is not None:
                for file_uri in workflow_var.value:
                    self.validate_file(file_uri)

        logger.debug('-------------------------------------------')
        summary_str = f"Existing URI's: {len(self.validated_files)}, Non-existing URI's: {len(self.non_validated_files)}, Glacier URI's: {len(self.glacier_files)}"
        logger.info(summary_str)
        for fn in self.non_validated_files:
            logger.error(f'Missing URI: {fn}')
        for fn in self.glacier_files:
            logger.error(f'Glacier URI: {fn}')

        return len(self.non_validated_files) == 0


    def validate_file(self, file_uri: str):
        file_uri = file_uri.replace('"', '')
        if not re.match(fr"{STORAGE_PREFIX_REGEX}", file_uri):
            return
        try:
            proto, bucket_name, file_name = split_uri(file_uri)
        except AttributeError:
            self.non_validated_files.append(file_uri)
        else:
            exists = self.blob_exists(bucket_name, file_name, storage_type=proto)
            if exists == StorageClass.EXIST:
                self.validated_files.append(file_uri)
            else:
                self.non_validated_files.append(file_uri)
            if exists == StorageClass.GLACIER:
                self.glacier_files.append(file_uri)

    def blob_exists(self, bucket_name, file_name, storage_type="gs"):
        exists = StorageClass.MISSING
        if storage_type == "gs":
            try:
                client = storage.Client()
                bucket = client.get_bucket(bucket_name)
                blob = bucket.blob(file_name)
                exists = blob.exists()
                if exists:
                    return StorageClass.EXIST
                else:
                    return StorageClass.MISSING
            # blob_exists requires storage.bucket.get access which might be forbidden, 
            # yet objects in this bucket can still be accessed by gsutil
            # Could not fine a python api to access the object in this case
            except google.api_core.exceptions.Forbidden:
                full_uri = f"gs://{bucket_name}/{file_name}"
                process = subprocess.run(f'gsutil ls {full_uri}'.split(), capture_output=True)
                if process.returncode == 0:
                    exists = StorageClass.EXIST
        if storage_type == "s3":
            try:
                client = boto3.client("s3")
                ho = client.head_object(
                    Bucket=bucket_name,
                    Key=file_name
                )
                if 'StorageClass' in ho and ho['StorageClass'] == 'GLACIER':
                    if not self._is_available(ho):
                        exists = StorageClass.GLACIER
                    else:
                        exists = StorageClass.EXIST
                    return exists
                exists = StorageClass.EXIST
            except botocore.exceptions.ClientError:
                pass
        return exists
                
    def _is_available(self, ho):
        """
        Check if the object is available in S3 Glacier
        :param ho: head_object response
        :return: True if the object is available, False otherwise
        """
        if 'Restore' in ho:
            restore_info = ho['Restore']
            if restore_info and 'ongoing-request="false"' in restore_info:

                date_txt = re.search(r'expiry-date="([^"]+)"', restore_info).group(1)
                expiry_dt = datetime.strptime(date_txt, '%a, %d %b %Y %H:%M:%S GMT').replace(tzinfo=timezone.utc)
                now_utc    = datetime.now(timezone.utc) 
                if expiry_dt > now_utc:
                    return True
        return False

    def validate_files_in_object(self, o):
        if type(o) is dict:
            for key, value in o.items():
                self.validate_files_in_object(value)
        elif type(o) is list:
            for value in o:
                self.validate_files_in_object(value)
        elif type(o) is str:
            self.validate_file(o)


def main():
    """
    validate all GCP/AWS URLs in json inputs point to existing objects
    """
    args = get_args()
    validated = CloudFilesValidator(args.wdl, args.json).validate()
    if not validated:
        raise RuntimeError('Found non existing files!')


if __name__ == '__main__':
    main()
