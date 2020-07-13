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
job_info_template = {
    'id': '',
    'comment': '',
    'command': 'executeScript',
    'target': '',
    'targets': [],
    'value': ''
}

job_status_template = {
    'id': '',
    'comment': '',
    'command': 'executeScript',
    'target': 'sauce:job-result=passed',
    'targets': [],
    'value': ''
}

# START
logger.info('Starting...\n\nSIDE SAUCE\n')
logger.info('Searching for .side files in current path...')

side_filename = None

for f in os.listdir('.'):
    if f.endswith('.side'):
        side_filename = f
        logger.info('Found: "' + side_filename + '"')
        break

if side_filename is None:
    raise EnvironmentError("No file with .side extension in the current path")

# PARSE SIDE FILE
with open(side_filename, 'r') as side_file:
    side_json = json.load(side_file)

# SET BUILD ID
jenkins_job_name = os.environ.get('JOB_NAME', None)
jenkins_build_number = os.environ.get('BUILD_NUMBER', None)

if jenkins_job_name is None or jenkins_build_number is None:
    timestamp = datetime.datetime.now().strftime('[%b %d %H:%M]').format()
    user = '[{}]'.format(getpass.getuser())
    build_id = 'LOCAL BUILD ' + user + timestamp
else:
    build_id = jenkins_job_name + '[' + jenkins_build_number + ']'

logger.info('Sauce Build ID: ' + build_id)
logger.info('Injecting Sauce steps to ' + str(len(side_json['tests'])) + ' tests')

# INJECT SAUCE STEPS
for test in side_json['tests']:
    # Set job build step
    job_build_step = deepcopy(job_info_template)
    job_build_step['id'] = str(uuid.uuid4())
    job_build_step['target'] = 'sauce:job-build=' + build_id

    # Set job name step
    job_name_step = deepcopy(job_info_template)
    job_name_step['id'] = str(uuid.uuid4())
    job_name_step['target'] = 'sauce:job-name=' + test['name']

    # Set job status step
    job_status_step = deepcopy(job_status_template)
    job_status_step['id'] = str(uuid.uuid4())

    # Insert steps
    test['commands'].insert(0, job_build_step)
    test['commands'].insert(1, job_name_step)
    test['commands'].append(job_status_step)

new_side_filename = side_filename.split('.')
new_side_filename = new_side_filename[0] + '-sauce.side'

# Write SIDE file
logger.info('New SIDE file: "' + new_side_filename + '"')

with open(new_side_filename, 'w') as new_side_file:
    json.dump(side_json, new_side_file, indent=4)

logger.info('Done.\n')
