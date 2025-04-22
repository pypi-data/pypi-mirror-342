#! /bin/bash

OUT_DIR=`readlink -f "./tmp/new_big"`
POSITIVE_FILE_NAME="positive_files.json"
FINE_CASES_NAME="fine.json"
NO_ARG_CASES_NAME="error_no_arg.json"


mkdir -p $OUT_DIR
cd .. && python -m solfuse.tools.iter_cases_cgt ~/datasets/DISL/extracted_contracts/source_code --ignore_fail -cq --list_buggy --list_failed --clear_flags --no_include_state_machine --use_new_big_id_and_contract --use_timeout --timeout 40s --output_dir=$OUT_DIR \
&& python -m solfuse.tools.filter_runnable_echidna --output_dir=$OUT_DIR --positive_files_json=${OUT_DIR%/}/${POSITIVE_FILE_NAME}\
&& python -m solfuse.tools.fix_no_arg_echidna --output_dir=$OUT_DIR --fine_json=${OUT_DIR%/}/${FINE_CASES_NAME} --no_arg_json=${OUT_DIR%/}/${NO_ARG_CASES_NAME}
# cd .. && python -m solfuse.tools.iter_cases_cgt ~/datasets/cgt/source --ignore_fail -cq --list_buggy --list_failed --clear_flags --no_include_state_machine --output_dir=$OUT_DIR && cp ${OUT_DIR%/}/fine.json ${OUT_DIR%/}/fine_fixing.json
