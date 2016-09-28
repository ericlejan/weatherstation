#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mraa
import thread, time
import pyupm_th02

# create sensor
th02 = pyupm_th02.TH02(6,0x40)
print th02.name()
print th02

def input_thread(CheckInput):
	check = raw_input()
	CheckInput = CheckInput.append(check)
	return
   
def mesureTempHygro():
	CheckInput = []
	thread.start_new_thread(input_thread, (CheckInput,))
	print '\nTapez "stop" pour arrêter les mesures.\n'
	print 'Température :\t\t' +'Hygrométrie :\t\t'
# Loop
	while True :
        	if CheckInput == ['stop']  : 
        		print 'Arrêt demandé.'
        		break
		if th02.getStatus() :
			temp = th02.getTemperature()
			hygro = th02.getHumidity ()
			print '\t%.3f\t\t\t'%temp + '%.3f\t\t\t'%hygro
			time.sleep (5)
#		else :
#			print 'Sensor is off'
#			break
	return

mesureTempHygro()

