#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mraa
import pyupm_mpl3115a2
import thread, time

# i2c bus pre-cabled bus on arduino breakout
bus = 6
pressAddress = 0x60
localAlt = 189.5

# create sensor on the bus
mpl = pyupm_mpl3115a2.MPL3115A2(bus, pressAddress)

def reset():
	mpl.resetSensor ()
	time.sleep(2)
	return

def test():
	mpl.testSensor ()
	time.sleep(2)
	return

def input_thread(CheckInput):
	check = raw_input()
	CheckInput = CheckInput.append(check)
	return
   
def mesurePressTemp():
	CheckInput = []
	thread.start_new_thread(input_thread, (CheckInput,))
	print '\nTapez "stop" pour arrêter les mesures, test pour tester le capteur \net reset pour le réinitialiser.\n'
	print 'Température :\t\t' +'Hygrométrie :\t\t' 'Hygro Corrigée :'
# Loop
	while True :
        	if CheckInput == ['stop']  : 
        		print 'Arrêt demandé.'
        		break
        	elif CheckInput == ['test'] :
        		test()
        		print 'Reset effectué.'
        		Checkinput = CheckInput.remove('test')
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput == ['reset'] :
        		reset()
        		print 'Reset effectué.'
        		Checkinput = CheckInput.remove('reset')
        		thread.start_new_thread(input_thread, (CheckInput,))
		mpl.sampleData()
		RH = mpl.getCompRH()
		temp = mpl.getTemperature()
		hygro = htu21df.getHumidity ()
		print '\t%.3f\t\t\t'%temp + '%.3f\t\t\t'%hygro + '%.3f'%RH
		time.sleep (5)
	return

mesurePressTemp()

