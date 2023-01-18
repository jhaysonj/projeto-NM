#!/bin/bash

# execute like "sudo"
# 1) chmod +x wifi.sh --> 2) sudo wifi.sh

search_channel () {
    channel=$1
    
    channel2ghz='1 2 3 4 5 6 7 8 9 10 11'
    channel5ghz='36 40 44 48 52 56 60 64 100 104 108 112 116 120 124 128 132 136 140 149 153'
    
    # scan the list channel2ghz searching for the chosen channel
    for num in $channel2ghz;do

        # finded the chosen channel
        if [ $channel == $num ];then
            return 1
        fi
    done

    # scan the list channel5ghz searching for the chosen channel
    for num in $channel5ghz;do
        # finded the chosen channel
        if [ $channel == $num ];then
            return 1
        fi
    done

    # channel doesnt exist on both lists
    return 0
}

echo -e "[1] Manager Manager\n[2] Monitor Mode\n[3] Change Channel\n[0] Exit\n\nChoose one option:"
read choice

#antenna_name = `iwconfig 2>&1 | grep '^wl' | awk '{print $1}'`
antenna_name=`iwconfig 2>&1 | grep wl | cut -d ' ' -f1 | cut -d '.' -f 1`

while [ $choice != 0 ]
do
	while [[ $choice -lt 0 && $choice -gt 3 ]]
	do
	echo -e '[1] Manager Manager\n[2] Monitor Mode\n[3] Change Channel\n[0] Exit\n'
        read choice
	done	

	if [ $choice == 1 ]
	then
		ifconfig $antenna_name down
		iwconfig $antenna_name mode manager
		ifconfig $antenna_name up
		sleep 1
		iwconfig

	elif [ $choice == 2 ]
	then
		ifconfig $antenna_name down
		iwconfig $antenna_name mode monitor
		ifconfig $antenna_name up
		sleep 1
		iwconfig

	elif [ $choice == 3 ]
	then
			
		echo -e "\nChannel:"
		read channel
		search_channel $channel
		resp=$?
		# find the channel on list
		if [ $resp == 1 ]
		then
			airmon-ng check kill

			airmon-ng start $antenna_name

			# derruba a placa 
			ifconfig $antenna_name down

			# change channel
			iwconfig $antenna_name channel $channel

			# sobe a placa
			ifconfig $antenna_name up

			sleep 1

			# list the current channel
			iwlist $antenna_name channel | grep 'Current'
		
			sleep 1

		# channel doesn't exist
		else 
			echo "Error, channel doesn't exist"
			sleep 1.5
		fi	
	fi

	echo -e '\n\n\n[1] Manager Manager\n[2] Monitor Mode\n[3] Change Channel\n[0] Exit\n'
	read choice
done

