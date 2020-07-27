import datetime
import getpass
import json
import logging
import os
import sys
import uuid
from copy import deepcopy

# SET HANDLER TO STDOUT
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# CREATE LOGGER
logger = logging.getLogger('side-sauce')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# SAUCE STEP TEMPLATES
step_template = {
    'id': '',
    'comment': '',
    'command': 'executeScript',
    'target': '',
    'targets': [],
    'value': ''
}

# START
logger.info('Starting...\n\nSIDE SAUCE\n')
logger.info('Searching for .side files...')

side_files = []

for f in os.listdir('.'):
    if f.endswith('.side') and not f.endswith('-sauce.side'):
        side_files.append(f)

if not side_files:
    raise EnvironmentError("Unable to find any Selenium IDE files in the current path")

logger.info('Found {} file(s): {}'
            .format(len(side_files), str(side_files).strip('[]')))

# SET BUILD ID
jenkins_job_name = os.environ.get('JOB_NAME', None)
jenkins_build_number = os.environ.get('BUILD_NUMBER', None)

if jenkins_job_name is None or jenkins_build_number is None:
    timestamp = datetime.datetime.now().strftime('[%b %d %H:%M]').format()
    user = '[{}]'.format(getpass.getuser())
    build_id = 'LOCAL BUILD ' + user + timestamp
else:
    build_id = jenkins_job_name + ' #' + jenkins_build_number

logger.info('Sauce Build ID: \'' + build_id + '\'')

for side_filename in side_files:
    # PARSE SIDE FILES
    with open(side_filename, 'r') as side_file:

        logger.info('-----------------------------------')
        logger.info('Parsing file: ' + side_filename)

        side_json = json.load(side_file)

        logger.info('Injecting Sauce steps to ' + str(len(side_json['tests'])) + ' tests')

        # INJECT SAUCE STEPS
        for test in side_json['tests']:
            # Set job build step
            job_build_step = deepcopy(step_template)
            job_build_step['id'] = str(uuid.uuid4())
            job_build_step['target'] = 'sauce:job-build=' + build_id

            # Set job name step
            job_name_step = deepcopy(step_template)
            job_name_step['id'] = str(uuid.uuid4())
            job_name_step['target'] = 'sauce:job-name=' + test['name']

            # Set job failed step
            job_failed_step = deepcopy(step_template)
            job_failed_step['id'] = str(uuid.uuid4())
            job_failed_step['target'] = 'sauce:job-result=failed'

            # Set job passed step
            job_passed_step = deepcopy(step_template)
            job_passed_step['id'] = str(uuid.uuid4())
            job_passed_step['target'] = 'sauce:job-result=passed'

            # Insert steps
            test['commands'].insert(0, job_build_step)
            test['commands'].insert(1, job_name_step)
            test['commands'].insert(2, job_failed_step)
            test['commands'].append(job_passed_step)

        new_side_filename = side_filename.split('.')
        new_side_filename = new_side_filename[0] + '-sauce.side'

        # Write SIDE file
        logger.info("New SIDE file: '{}'".format(new_side_filename))

        with open(new_side_filename, 'w') as new_side_file:
            json.dump(side_json, new_side_file, indent=4)

logger.info('-----------------------------------')
logger.info('Done.\n')
