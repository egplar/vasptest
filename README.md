Test suite for VASP
========================

Description
-----------

A collection of VASP calculations that can be used with the "Behave" testing framework for Python to validate a VASP installation. There are currently five test suites:

* **basic**: a small test suite with simple calculations that completes quickly
* **geometry**: various kinds of geometry optimization of Si cell
* **custom**: tests for the presence of custom modifications made at NSC/SNIC sites.
* **functional**: test more advanced features like GW, hybrid calculations, and DOS plots.
* **production**: assorted troublesome production jobs that can run on more than one compute node.

Please note that these are far from complete and do not cover all of VASP's functionality. For example, there are currently no tests for molecular dynamics simulations.

The actual tests are coded into the `*.feature` files in the `feature/` folder. There are some more descriptions there about what each test is doing. The actual test input may be found in the `input/` folder.

Requirements
------------

* Python 2.7
* Python Behave
* Unix-like environment
* The new VASP PBE POTCAR library (released in April 2012)

How to install
--------------

1. Copy/extract/clone the vasptest folder to a suitable place.
2. Locate the path to your VASP PBE POTCAR library (the folder named "potpaw_PBE.52"). If you do not have the full POTCAR library, any licensed VASP user can download the file "potpaw_PBE.52.tar.gz" from the VASP community web.
3. Run the script build-potcar.sh with the path to the POTCAR library as argument. E.g.:

	source build-potcar.sh /opt/vasp/potpaw_PBE.52/

4. The test suite is now ready to use. See below.

How to run
----------

Cd to the directory containing the VASP test suite. Before running, you need to tell where your VASP binary is located that you want to test. This is done by setting the VASPTEXT_EXE environment variable.

For serial VASP:

	export VASPTEST_EXE=/path/to/vasp

For parallel VASP, insert your MPI launcher command and give the **maximum** number of ranks that you want to run on. The test runner will automatically scale down smaller jobs. E.g. for Intel MPI with maximum 64 cores:

	export VASPTEST_EXE="mpiexec.hydra -np 64 /path/to/vasp"

Run the test suite via the `behave` command.

	behave -s -c -k

When you run the test, output will given in the following form

 	...
 	Scenario: Si-hybrid 
	    Given that the POTCAR MD5 is 4e058592231fc4e091ac0c92d87797b0
	    When I run VASP with a maximum of 8 ranks
	    Then the total energy should be -41.86884258 +/- 1.0e-5 eV
	    And self consistency should be reached in 14 iterations
	    And the point group symmetry should be T_d
	    And the XML output should be valid
	...

Unless something goes wrong, this is what you should see. There is one check or test per line written, and if something is found, a Python assertion will be triggered, and usually some indication of what was wrong also gets written out.

 	Scenario: Si-hybrid 
	    Given that the POTCAR MD5 is 4e058592231fc4e091ac0c92d87797b0
	    When I run VASP with a maximum of 8 ranks
	    Then the total energy should be -41.86884258 +/- 1.0e-5 eV
	      Assertion Failed: got -41.82492826 eV instead

All output is also logged to a file called `vasptest.log` by default (the name can be changed in behave.ini). The input and output from the actual calculations can be found in the `tmp/` directory for inspection. It is a good idea to manually empty this folder before each invocation of the test suite.

To select individual test suites, you can give the direct path to a feature definition file:

	behave -s -c -k features/basic.feature

The `behave` program has many features for controlling test execution and reporting. More information can be found either on the web

	http://pythonhosted.org/behave/behave.html

or by invoking the help flag:

	behave -h

Happy testing!
