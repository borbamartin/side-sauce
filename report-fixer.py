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
logger.info('Searching for .xml files...')

reports = []

for f in os.listdir('.'):
    if f.endswith('.xml'):
        reports.append(f)

if not reports:
    raise EnvironmentError("Unable to find any XML files in the current path")

logger.info('Found {} file(s): {}'
            .format(len(reports), str(reports).strip('[]')))

for report_name in reports:
    # PARSE REPORT FILES
    with open(report_name, 'r') as report_file:
        report = ElementTree.parse(report_file)
        root = report.getroot()

        logger.info('-----------------------------------')
        logger.info("Working on '{}'".format(report_name))

        # Set the real suite name
        suite_name = report_name.split('.xml')[0]
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
        report.write(report_name)

logger.info('-----------------------------------')
logger.info('Done.\n')
