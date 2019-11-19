Important To Note:
All of the following scripts were executed inside an ubuntu 16.04 VM running in virtual box. Running containernet outside of virtual box (on the native ubuntu OS) presented network configuration issues where the docker hosts could not connect to the internet through the SDN. 

A list of all the prerequisite programs is still yet to be compiled. A few programs that are immediatly necessary are (all the following programs were installed on the vm inside virtual box):
- Docker
- Selenium
- Ryu https://ryu.readthedocs.io/en/latest/index.html
- Containernet (bare-metal install) https://containernet.github.io/#installation

Explanation of various files (further details can be found in the comments of  the files themselves):
The Selenium traffic generation programs are vulatest.py, outlooktest.py and youtubetest.py. 
These are run on the docker container inside the SDN.

The Dockerfile creates the docker image used to run the various tests inside Containernet (the SDN implementation used).

Classify.sh is a simple bash loop used to run the live classification program repeatedly.

Snortprocess.sh facilitates the live classificaiton process, consisting of:
  1. Start live packet capture on the mirrored interface (snort0)
  2. Pre-process captured packets
  3. Run saved classification model on the processed packets.

Controllerinet.py creates the SDN using Containernet, starting the docker host and switches and then running the various tests on the docker host.

Runnet.sh is a bash script which starts the ryu controller, followed by running controllerinet.py.
This script is for ease of use and essentailly runs commands 1. and 2. in from below.

General process followed for strating traffic generation in containernet
1. Start ryu controller running simpleswitch_snort (https://ryu.readthedocs.io/en/latest/snort_integrate.html)
2. Start the containernet network
3. Run test on docker host d1

Steps followed, with commands
1. Running ryu and Snort in controllerinet.py (on the virtual box vm):

sudo ryu-manager ryu.app.simple_switch_snort

1.5 (Optional, instead of 1.) Run ryu and snort along with flowmanager (web dashboard to monitor traffic):

sudo ryu-manager ~/flowmanager/flowmanager.py ryu.app.simplswitch_snort

2. Run containernet network (controllerinet.py)

sudo python controllerinet.py

3. Run test on docker host d1 (run command inside containernet)

d1 python /mnt/vol1/WebTrafficSDN/vulatest.py

4. Snort a specified number (100) of packets on interface snort0 and store logged file in tests dir (run on virtual box vm):

sudo snort -i snort0 -l /home/osboxes/Documents/tests -n 100

4.5 (Optional, instead of 4.) Use -A unsock to send alerts to ryu controller:

sudo snort -i s1-eth1 -A unsock -l /home/osboxes/Documents/tests/ -c /etc/snort/snort.conf

5. Rename snort log to filename.pcap

sudo mv snort.log.123456 filename.pcap

6.0 Edit netmate flowcalc netAI-rules-stats-ni.xml
- change output file location and name
- change export name from "ac_file" to "netai_arff"

6.1 Install libs for netmate flowcalc (https://github.com/danielarndt/netmate-flowcalc)
- sudo apt-get install libreadline-dev
- sudo apt-get install libxml2-dev

6.2 netmate-flowcalc, Edit netAI-rules-stats-ni.xml to output the desired file name and location.

sudo netmate -r netAI-rules-stats-ni.xml -f ~/Documents/tests/outlooktestuct.pcap 

7. Start weka to open flow features and train classifier

java -jar weka.jar

The steps taken to train a classifier are too long to detail here but can also be found on various youtube videos on using weka.
The trained classifier in weka needs to be saved (.model extension) and the snortprocess.sh file needs to be edited so that the j48resampled.model is replaced with your newly trained model.


For real-time classification, follow these steps:
1. Run runnet.sh to start Ryu controller (running snort application) and the Containernet program (controllerinet.py)

sudo bash runnet.sh

2. Next run the the real-time classificaiton program in a separate terminal

sudo bash classify.sh
