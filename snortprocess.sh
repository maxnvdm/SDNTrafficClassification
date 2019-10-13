#!/bin/bash

if test -f ../pcaps/filename.pcap; then
    sudo rm ../pcaps/filename.pcap
fi

if test -f ../pcaps/filename.arff; then
    sudo rm ../pcaps/filename.arff
fi

if test -f ../pcaps/filtered.arff; then
    sudo rm ../pcaps/filtered.arff
fi

# Initiate packet capture on mirrored interface, saving results to capturedata.txt and printing to the terminal 
sudo snort -i snort0 -l /home/osboxes/Documents/tests/snorts/ -n 200 | tee -a /home/osboxes/Documents/tests/pcaps/capturedata.txt
# Conver snort packet capture into a pcap file (it is stored in a pcap format, thus requireing only a name change)
sudo cp /home/osboxes/Documents/tests/snorts/snort.log.* /home/osboxes/Documents/tests/pcaps/filename.pcap &&
# Invoke Netmate on the pcap file, using the -r flag to point Netmate to the flow feature rules to be used
sudo ../netmate-flowcalc-master/src/netmate/netmate -r ../netmate-flowcalc-master/netAI-rules-stats-ni.xml -f ~/Documents/tests/pcaps/filename.pcap | tee -a /home/osboxes/Documents/tests/pcaps/capturedata.txt
# Using Weka, remove the source and destination IP addresses from the dataset
java -cp ../weka-3-8-3/weka.jar weka.filters.unsupervised.attribute.Remove -R 1,3 -i ../pcaps/filename.arff -o ../pcaps/filtered.arff
# Add a class label to each flow in the dataset (set to ? (unkown) by default)
java -cp ../weka-3-8-3/weka.jar weka.filters.unsupervised.attribute.Add -T NOM -N class -L outlook,vula,youtube -C last -W 1.0 -i ../pcaps/filtered.arff -o ../pcaps/filteredclass${1}.arff
# Use the pre-built classifier to make predictions on the classes of the recorded flows
java -cp ../weka-3-8-3/weka.jar weka.classifiers.trees.J48 -T /home/osboxes/Documents/tests/pcaps/filteredclass${1}.arff -l /home/osboxes/Documents/tests/j48resampled.model -p 0 | tee -a /home/osboxes/Documents/tests/pcaps/youtuberealtime.txt
sudo rm ../snorts/snort.log.*

sudo rm ../pcaps/filename.arff
sudo rm ../pcaps/filtered.arff
#sudo rm ../pcaps/filteredclass.arff
