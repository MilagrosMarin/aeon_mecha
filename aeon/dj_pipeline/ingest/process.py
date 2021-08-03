import sys
import os
import time
import logging

from aeon.dj_pipeline import experiment, tracking, analysis


log = logging.getLogger(__name__)


"""
Auto-processing routines defined to operate the DataJoint pipeline for the Aeon project
Several "process" functions defined to call the `populate()` for different grouping of tables,
depending on their priority in the ingestion routines.

Each process function is ran in a while-loop with the total run-duration 
configurable via environment variable 'POPULATE_DURATION' (if not set, runs perpetually)
    - the loop will not begin a new cycle after this period of time (in second)
    - the loop will run perpetually if limit<0 or if limit==None
    - the script will not be killed _at_ this limit, it will keep executing, 
        and just stop repeating after the time limit is exceeded

Some populate settings (e.g. 'limit', 'max_calls') can be set to process 
some number of jobs at a time for every iteration of the loop, instead of all jobs.
This allows the processing to propagate through the pipeline more horizontally

Usage as a script:
    
    python aeon/dj_pipeline/ingest/process.py high

(or this can be used as python module normally)

"""


# ---------------- Auto Ingestion -----------------
default_run_duration = float(os.environ.get('POPULATE_DURATION'))

settings = {'reserve_jobs': True,
            'suppress_errors': True,
            'display_progress': True}


def process_high_priority(run_duration=default_run_duration, sleep_duration=600):
    start_time = time.time()
    while (time.time() - start_time < run_duration) or (run_duration is None) or (run_duration < 0):
        experiment.TimeBin.generate_timebins(experiment_name='exp0.1-r0')
        experiment.SubjectEnterExit.populate(**settings)
        experiment.SubjectAnnotation.populate(**settings)
        experiment.SubjectWeight.populate(**settings)

        experiment.FoodPatchEvent.populate(**settings)
        experiment.WheelState.populate(**settings)

        experiment.Session.populate(**settings)
        experiment.SessionEnd.populate(**settings)
        experiment.SessionEpoch.populate(**settings)

        time.sleep(sleep_duration)


def process_middle_priority(run_duration=default_run_duration, sleep_duration=5):
    start_time = time.time()
    settings['max_calls'] = 5
    while (time.time() - start_time < run_duration) or (run_duration is None) or (run_duration < 0):
        tracking.SubjectPosition.populate(**settings)

        analysis.SessionTimeDistribution.populate(**settings)
        analysis.SessionSummary.populate(**settings)

        time.sleep(sleep_duration)


def process_low_priority(run_duration=default_run_duration, sleep_duration=5):
    start_time = time.time()
    settings['max_calls'] = 5
    while (time.time() - start_time < run_duration) or (run_duration is None) or (run_duration < 0):
        experiment.FoodPatchWheel.populate(**settings)
        tracking.SubjectDistance.populate(**settings)

        time.sleep(sleep_duration)


actions = {'high': process_high_priority,
           'middle': process_middle_priority,
           'low': process_low_priority}


if __name__ == '__main__':

    if len(sys.argv) < 1 or sys.argv[1] not in ('high', 'middle', 'low'):
        print(f'Usage error! Run ingestion with:\n\t"process.py <mode>"'
              f'\n\t\t where mode is one of: "high", "middle", "low"')
        sys.exit(0)

    try:
        action = sys.argv[1]
        actions[action]()
    except Exception:
        log.exception("action '{}' encountered an exception:".format(action))
