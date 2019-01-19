#!/usr/bin/env bash

###############################################################################
# Script that should be run pre-commit after making any changes 
#
# Runs:
#   Unit tests
#   Linting
#   Type checking
###############################################################################

set -e

failures=""

function banner() {
    echo
    echo "================================================================================"
    echo $*
    echo "================================================================================"
    echo
}

#####################################################################
# Takes two parameters, a "name" and a "command". 
# Runs the command and prints out whether it succeeded or failed, and
# also tracks a list of failed steps in $failures.
#####################################################################
function run() {
    local name=$1
    local cmd=$2

    banner "Running $name"
    set +e
    $cmd
    exit_code=$?
    set -e
    
    if [[ $exit_code == 0 ]]; then
        echo Passed $name 
    else
        echo Failed $name
        failures="$failures $name"
    fi
}

parent=$(cd $(dirname $0) && pwd -P)
root=$(dirname ${parent} | xargs dirname)

pushd $root > /dev/null
banner "Executing in directory ${root}"
# FIXME: no unit tests as of yet
#run "Unit Tests"    "pytest -v -r sx ${root}/src/python"
run "Linting"       "flake8 flake8 --config=${root}/src/scripts/flake8.cfg ${root}/src/python"
pushd ${root}/src/python > /dev/null
pwd
run "Type Checking" "mypy . --config ${root}/src/scripts/mypy.ini"
popd > /dev/null
popd > /dev/null

if [ -z "$failures" ]; then
    banner "Precommit Passed"
else
    banner "Precommit Failed with failures in: $failures"
    exit 1
fi
