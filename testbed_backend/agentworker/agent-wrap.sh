#! /bin/bash
source {OSPLdir}/release.com
export LD_LIBRARY_PATH="{TOPdir}/testbed/lib:$LD_LIBRARY_PATH"
export PYTHONPATH="$PYTHONPATH:{TOPdir}/testbed"
python3.7 {TOPdir}/testbed/agentworker/worker.py
