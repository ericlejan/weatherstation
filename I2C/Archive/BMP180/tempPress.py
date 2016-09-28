#!/usr/bin/env python
# -*- coding: utf-8 -*-


import thread, time
import pyupm_bmpx8x
import mraa
import math 

# i2c bus
bus = 1
pressAddress = 0x77
altitudeMeters = 165.5
#check = raw_input()

# create sensor on the bus
bmp180 = pyupm_bmpx8x.BMPX8X(bus, pressAddress)

def testIfPresent():
	test = bmp180.isAvailable ()
	time.sleep(2)
	return test

def convertSeaLevel (m_iPressure):
	fPressure = m_iPressure / math.pow(1.0-altitudeMeters/44330, 5.255)
	return fPressure


def input_thread(CheckInput):
	check = raw_input()
	CheckInput = CheckInput.append(check)
	return
   
def messureTempPress():
	CheckInput = []
	thread.start_new_thread(input_thread, (CheckInput,))
	print '\nTapez "stop" pour arrêter les mesures, "test" pour tester le capteur \n'
# Add local altitude to obtain sea Level pressure value 
#change print instruction to introduce sealevel
#	print 'Température :\t\t' +'Pression :\t\t' +'Pression niveau de la mer :'
	print 'Température :\t\t' +'Pression :'
# Loop
	while True :
        	if CheckInput == ['stop']  : 
        		print 'Arrêt demandé.'
        		break
        	elif CheckInput == ['test'] :
        		testIfPresent()
        		print 'Test effectué.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput != [] :
        		print 'Commande inconnue.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
		temp = bmp180.getTemperatureCelcius()  * 1.0
		press = bmp180.getPressurePa () /100.0
# Add local altitude to obtain sea Level pressure value
# Uncomment conversion function call and change print function
#		seaLevelPress = convertSeaLevel (press)
#		print '%.1f\t\t\t'%temp + '%.2f\t\t\t'%press + '%.2f\t\t\t'%seaLevelPress
		print '%.1f\t\t\t'%temp + '%.2f\t\t\t'%press
		time.sleep (5)
	return
messureTempPress()
