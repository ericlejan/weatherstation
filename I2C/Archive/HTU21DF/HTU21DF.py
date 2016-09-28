#!/usr/bin/env python
# -*- coding: utf-8 -*-


import thread, time
import pyupm_htu21d
import mraa

# i2c bus
bus = 6
tempAddress = 0x40
#check = raw_input()

# create sensor on the bus
htu21df = pyupm_htu21d.HTU21D(bus, tempAddress)

def reset():
	htu21df.resetSensor ()
	time.sleep(2)
	return

def test():
	htu21df.testSensor ()
	time.sleep(2)
	return

def input_thread(CheckInput):
	check = raw_input()
	CheckInput = CheckInput.append(check)
	return
   
def messureTempHygro():
	CheckInput = []
	test()
	reset()
	hygro = htu21df.getHumidity ()	
	thread.start_new_thread(input_thread, (CheckInput,))
	print '\nTapez "stop" pour arrêter les mesures, "test" pour tester le capteur \net "reset" pour le réinitialiser.\n'
	print 'Température :\t\t' +'Hygrométrie :\t\t' 'Hygro Corrigée :'
# Loop
	while True :
        	if CheckInput == ['stop']  : 
        		print 'Arrêt demandé.'
        		break
        	elif CheckInput == ['test'] :
        		test()
        		print 'Test effectué.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput == ['reset'] :
        		reset()
        		print 'Reset effectué.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput != [] :
        		print 'Commande inconnue.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
		htu21df.sampleData()
		RH = htu21df.getCompRH()
		temp = htu21df.getTemperature()
		hygro = htu21df.getHumidity ()
		print '%.3f\t\t\t'%temp + '%.3f\t\t\t'%hygro + '%.3f'%RH
		time.sleep (5)
	return
messureTempHygro()
