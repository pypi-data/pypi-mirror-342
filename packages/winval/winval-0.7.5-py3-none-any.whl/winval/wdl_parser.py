from __future__ import annotations

import re
from os.path import dirname, join

from winval import logger
from winval.parsed_workflow_inputs import ParsedWorkflowInputs
from winval.workflow_var import WorkflowVar, WorkflowVarType


class WdlParser:

    def __init__(self, wdl_file):
        self.wdl_file = wdl_file
        self.structs: dict[str, dict[str, WorkflowVar]] = {}
        self.workflow_vars: dict[str, WorkflowVar] = {}
        self.imported_wdls = set()
        self.workflow_name = None

    def parse_workflow_variables(self) -> ParsedWorkflowInputs:
        wdl_code_lines = self.__read_wdl_code_lines(self.wdl_file)
        self._parse_workflow_name(wdl_code_lines)
        self.__parse_structs(self.wdl_file)
        self._parse_variables_from_lines(wdl_code_lines)
        return ParsedWorkflowInputs(self.workflow_vars, self.structs)

    def __read_wdl_code_lines(self, wdl_file: str):
        with open(wdl_file) as wf:
            wdl_lines = wf.readlines()
            wdl_code_lines = self.get_code_lines(wdl_lines)
        return wdl_code_lines

    @staticmethod
    def get_code_lines(wdl_lines):
        wdl_code_lines = [strip_comments(line) for line in wdl_lines if is_code_line(line)]
        return wdl_code_lines

    def _parse_workflow_name(self, wdl_lines):
        for line in wdl_lines:
            line = line.strip()
            tokens = re.split(r'\s+', line)
            if tokens[0] == 'workflow':
                self.workflow_name = re.match(r'\w*', tokens[1]).group(0)
                logger.debug(f'workflow: {self.workflow_name}')
                return

    def _parse_variables_from_lines(self, wdl_lines) -> None:
        # For extra safety, in case someone uses this protected function from outside
        wdl_lines = self.get_code_lines(wdl_lines)
        for line_num, line in enumerate(wdl_lines):
            line = line.strip()
            tokens = re.split(r'\s+', line)

            if re.match('input{?', tokens[0]):
                if self.workflow_name is None:
                    raise ValueError('Undefined workflow name')
                workflow_vars = self.__parse_variables_from_block(wdl_lines[(line_num + 1):])
                self.workflow_vars.update(workflow_vars)
                return
        raise ValueError('Could not parse workflow args')

    def __parse_variables_from_block(self, wdl_lines_after_block_start: list) -> dict[str, WorkflowVar]:
        """
        Internal parsing function which is used both for workflow inputs variables and structs fields
        :param wdl_lines_after_block_start:
        :return dictionary of workflow variables:
        """
        workflow_vars = {}
        curly_brackets_scope = 1
        straight_brackets_scope = 0

        while len(wdl_lines_after_block_start) > 0:
            # end of inputs block
            if curly_brackets_scope <= 0:
                break
            line = wdl_lines_after_block_start.pop(0)
            curly_brackets_scope, straight_brackets_scope = \
                self.__update_scope(curly_brackets_scope, line, straight_brackets_scope)

            # inside internal brackets, meaning multiline complex variable default init
            while curly_brackets_scope > 1 or straight_brackets_scope > 0:
                next_line = wdl_lines_after_block_start.pop(0)
                line += next_line
                curly_brackets_scope, straight_brackets_scope = \
                    self.__update_scope(curly_brackets_scope, next_line, straight_brackets_scope)

            line = line.strip()
            if len(line) == 0 or line.startswith('}'):
                continue

            # parse single-line default value (if default is multiline, will ignore all but first
            equal_split = line.split('=')
            if len(equal_split) == 0 or equal_split == ['']:
                continue
            var_str = equal_split[0]
            if len(equal_split) == 2:  # has default value
                default_value_str = equal_split[1].strip()
            else:
                default_value_str = None

            var_tokens = [token for token in re.split('[ ]', var_str) if token != '']
            var_name = var_tokens[-1]
            var_type = ''.join(var_tokens[:-1])
            is_optional = '?' in var_type
            var_type = var_type.replace('?', '')
            # ignore is_non_empty qualifier
            var_type = var_type.replace('+', '')

            if default_value_str is not None:
                is_optional = True

            # If struct is used, add all of its fields as variables to workflow
            if var_type in self.structs:
                workflow_var_type = WorkflowVarType.STRUCT
                struct_type = var_type
            else:
                workflow_var_type = WorkflowVarType.from_string(var_type)
                struct_type = None

            workflow_vars[var_name] = WorkflowVar(var_name,
                                                  workflow_var_type,
                                                  is_optional,
                                                  default_value_str,
                                                  self.workflow_name,
                                                  struct_type)
        return workflow_vars

    def __update_scope(self, curly_brackets_scope, line, straight_brackets_scope):
        curly_brackets_scope -= line.count('}')
        curly_brackets_scope += line.count('{')
        straight_brackets_scope -= line.count(']')
        straight_brackets_scope += line.count('[')
        return curly_brackets_scope, straight_brackets_scope

    def __parse_structs(self, wdl_file) -> None:
        self.imported_wdls.update({wdl_file})
        wdl_lines = self.__read_wdl_code_lines(wdl_file)
        self._parse_structs_iter(wdl_lines)
        for line in wdl_lines:
            line = line.strip()
            tokens = re.split(r'\s+', line)
            # stop parsing at workflow/task definition
            if tokens[0] in ['workflow', 'task']:
                return
            if tokens[0] == 'import':
                import_wl = tokens[1].replace('"', '').replace("'", '')
                import_path = join(dirname(wdl_file), import_wl)
                if import_path not in self.imported_wdls:
                    logger.debug(f'importing structs from {import_path}')
                    self.__parse_structs(import_path)

    def _parse_structs_iter(self, wdl_lines: list[str]) -> None:
        # For extra safety, in case someone uses this protected function from outside
        wdl_lines = self.get_code_lines(wdl_lines)
        wdl_text = '\n'.join(wdl_lines)
        struct_paragraphs: list[str] = \
            re.findall(r'struct\s+\w+\s*{\s*\n*[\[\]\w+\s*?\n]*}', wdl_text)

        for struct_paragraph in struct_paragraphs:
            struct_lines = re.split(r'[\n{}]', struct_paragraph)
            tokens = re.split(r'\s+', struct_lines[0])
            struct_name = tokens[1]
            logger.debug(f'\t{struct_name}')
            struct_variables = self.__parse_variables_from_block(struct_lines[1:])
            self.structs[struct_name] = struct_variables


def is_code_line(line: str) -> bool:
    line = line.strip()
    tokens = re.split(r'\s+', line)
    is_comment = tokens[0].startswith('#')
    is_empty = len(tokens) == 0 or tokens == ['']
    return not (is_comment or is_empty)


def strip_comments(line: str) -> str:
    return re.split('#', line)[0].strip()
