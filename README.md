# SIDE Sauce
A simple script to add test name, build id and test result information to Selenium IDE scripts running
on Sauce Labs.

One issue when running Selenium IDE tests on Sauce Labs is that test information is not sent, so you end
up with a bunch of "Unnamed job xxx", with no test result or build grouping, which makes reviewing results 
difficult and time-consuming.

This script will grab every `.side` file it finds in the folder you run it from, parse it and add 
the steps to set the name, build and result for each test.

#### Test name
Test name will match the one you set in Selenium IDE.

#### Build ID
Build ID will be `LOCAL BUILD [{user}][{timestamp}]` if run locally. When run from Jenkins the build name
will match Jenkins's job name and build number.

#### Test result
Test result cannot be sent if a test fails, since the execution won't reach that step, therefore we set the
test as initially failing. If the test is completed successfully it will be marked as passed.

### File placement
Make sure you include this script in the same folder as your .side file, and that you run it before running
the selenium command-line runner. The exported file will be named after the original, with a trailing
`-sauce.side`.

### Running the script
To run the file simply do: `python ./side-sauce.py`


# Report fixer
Selenium IDE's command line runner gives you the option to export test results in JUnit format. When you set
your suite to run in parallel, SIDE splits your tests into suites, resulting in a new suite per each test.
The JUnit XML created by Jest sets every `<testsuite>` name to `undefined`, so when Jenkins parses it the results
get overwritten, showing only 1 result, so if you run 10 tests from the same suite in parallel, Jenkins will show
as if you would have executed 1 test only.

The report fixer takes care of this, renaming every test suite to match the name of your test case, as well as
adding a `SIDE` default package, and a class name that will match the name of your SIDE project for a clean look
to your JUnit results in Jenkins.

### File placement
Make sure the results are outputted to `/results`. This path is relative to where your `report-fixer.py` file 
is placed. Please consider the script will modify every `XML` file in that path, so it should not be shared. 

### Running the script
Simply do: `python ./report-fixer.py` after your SIDE execution has finished.

Keep in mind that if the SIDE execution fails this step won't run unless you configure it as a post-build action,
or if you capture the exit code and throw it after the reporter finishes the execution.


###### Please note these are temporary workarounds until the Selenium team adds-fixes the features, or I get the time to contribute.