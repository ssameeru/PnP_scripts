PnP_utilities
===========

This project consists of series of scripts, which were used by Intel
Chrome PnP BA Team in their day to day Job. You can find the
Introduction and usage of each script below.

Autotest Processing Script
-----------------
This script is used to process the PLT autotest Battery Rundown results.
PLT is a Google Script which was created to emulate average user bhaviour
and measure the resultant battery life.

How to use the script?
-----
Once the PLT Autotest is completed, it will generate the results directory
which will have CPU, Power, Thermal, Fan RPM related statistics for complete
test duration.

* copy the power_LoadTest directory which is under results/default/ directory in
  /usr/local/autotest, from Device Under Test(DUT) into your Linux/Windows Machine.

* Please use the below command to process the results of PLT. Python version >3 is
the minimal requirement for this script to work.

cmd: python3 autotest_processing.py <absolute patht to power_LoadTest directory>
Example: python3 autotest_processing.py /home/ssameeru/work/raptorlake/power_LoadTest/

* A summary file will be generated by the script which will give you the below Average
statistics of the test.

   * Package Residencies
   * Core Residencies
   * Browsing Package and Core residencies
   * Email Package and Core residencies
   * Document Package and Core reisdencies
   * Video Playback Package and Core residencies.


Copyright and License
====================
These are opensource scripts which were licensed under GPL V2,
You can modify the scripts to suit your needs, These scripts comes with
absolutely No Warranty, but you are not allowed remove the Author, License
Header from the script file.
