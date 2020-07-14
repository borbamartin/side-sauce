import logging
import os
import sys

# SET HANDLER TO STDOUT
from xml.etree import ElementTree

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# CREATE LOGGER
logger = logging.getLogger('report-fixer')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# START
logger.info('Starting...\n\nSIDE REPORT FIXER\n')
logger.info('Searching for .xml files in current path...')

report_filename = None

for f in os.listdir('.'):
    if f.endswith('.xml'):
        report_filename = f
        logger.info('Found: "' + report_filename + '"')
        break

if report_filename is None:
    raise EnvironmentError("No file with .xml extension in the current path")

# PARSE SIDE FILE
with open(report_filename, 'r') as side_file:
    report = ElementTree.parse(report_filename)

root = report.getroot()

# Set the real suite name
logger.info('Setting suite name...')
suite_name = report_filename.split('.xml')[0]
root.attrib['name'] = suite_name

# Edit nodes
logger.info('Fixing JUnit structure...')

for test_suite in root.findall('testsuite'):
    test_case = test_suite.find('testcase')
    test_name = test_case.get('name').strip()
    test_case.attrib['name'] = test_name
    test_case.attrib['classname'] = 'SIDE.' + suite_name
    test_suite.attrib['name'] = test_name

logger.info('Saving report...')
report.write(report_filename)

logger.info('Done.\n')
