import argparse
import json

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
#    Validate set of constraints defined on workflow inputs, as defined inside a wdl file, on a specified input json


from winval.wdl_parser import WdlParser
from winval.constraints_pre_processor import ConstraintsPreProcessor
from winval.winval_class import Winval
from winval import logger


def run_winval(wdl_file: str, json_file: str) -> bool:
    logger.debug('--------------')
    logger.debug('--- WINVAL ---')
    logger.debug('--------------')
    with open(json_file) as json_file:
        json_dict = json.load(json_file)
        workflow_inputs = WdlParser(wdl_file).parse_workflow_variables()
        workflow_inputs.fill_values_from_json(json_dict)
        constraints = ConstraintsPreProcessor(wdl_file).process_constraint_strings()
        return Winval(workflow_inputs, constraints).workflow_input_validation()
    

def get_args():
    parser = argparse.ArgumentParser("winval")
    parser.add_argument('--wdl', required=True)
    parser.add_argument('--json', required=True)
    parser.add_argument('--log_level', default='INFO')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    [handler.setLevel(args.log_level.upper()) for handler in logger.handlers]
    run_winval(args.wdl, args.json)
