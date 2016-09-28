#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mraa
import pyupm_mpl3115a2
import thread, time

# i2c bus pre-cabled bus on arduino breakout
bus = 6
pressAddress = 0x60

# create sensor on the bus
mpl = pyupm_mpl3115a2.MPL3115A2(bus, pressAddress)

def reset():
	htu21df.resetSensor ()
	time.sleep(1)
	return

def input_thread(CheckInput):
	check = raw_input()
	CheckInput = CheckInput.append(check)
	return
   
def messureTempHygro():
	CheckInput = []
	thread.start_new_thread(input_thread, (CheckInput,))
	print '\nTapez "stop" pour arrêter les mesures.\n'
	print 'Température :\t\t' +'Hygrométrie :\t\t' 'Hygro Corrigée :'
# Loop
	while True :
        	if CheckInput == ['stop']  : 
        		print 'Arrêt demandé.'

        		break
        	elif CheckInput == ['reset'] :
        		reset()
        		print 'Reset effectué.'
        		Checkinput = CheckInput.remove('reset')
        		thread.start_new_thread(input_thread, (CheckInput,))
		htu21df.sampleData()
		RH = htu21df.getCompRH()
		temp = htu21df.getTemperature()
		hygro = htu21df.getHumidity ()
		print '\t%.3f\t\t\t'%temp + '%.3f\t\t\t'%hygro + '%.3f'%RH
		time.sleep (2)
	return

messureTempHygro()

