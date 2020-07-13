# SIDE Sauce
A simple script to add test name, build id and test result information to Selenium IDE scripts running
on Sauce Labs.

One issue when running Selenium IDE tests on Sauce Labs is that test information is not sent, so you end
up with a bunch of "Unnamed job xxx", with no test result or build grouping, which makes reviewing results 
difficult and time-consuming.

This script will pick the first .side file it finds in the folder you run it from, parse it and add 
some steps in order to set the test name, build and result for each test.

#### Test name
Test name will match the one you set in Selenium IDE.

#### Build ID
Build ID will be `LOCAL BUILD [{user}][{timestamp}]` if run locally. When run from Jenkins the build name
will match Jenkins's job name and build number.

#### Test result
Test result can only be sent if the test passes, so you will see 2 types of results: Passed and Completed.
If a test is marked as "Completed" that will most likely mean it has failed.

### File placement
Make sure you include this script in the same folder as your .side file, and that you run it before running
the selenium command-line runner. The exported file will be named after the original, with a trailing
`-sauce.side`.

### Running the script
To run the file simply do: `python ./side-sauce.py`

###### Please note this is a temporary workaround until the Selenium team adds the feature, or I get the time to contribute to it.
