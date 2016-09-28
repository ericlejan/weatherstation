#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mraa

import thread, time, math 
import pyupm_htu21d
import pyupm_bmpx8x

# i2c bus
bus = 1
tempAddress = 0x40
pressAddress = 0x77
altitudeMeters = 165.5

# create sensors on the bus
htu21df = pyupm_htu21d.HTU21D(bus, tempAddress)
bmp180 = pyupm_bmpx8x.BMPX8X(bus, pressAddress)

# define functions
def htuReset():
	htu21df.resetSensor ()
	time.sleep(2)
	return

def htuTest():
	htu21df.testSensor ()
	time.sleep(2)
	return

def bmpTest():
	test = bmp180.isAvailable ()
	time.sleep(2)
	return test

def input_thread(CheckInput):
	check = raw_input()
	CheckInput = CheckInput.append(check)
	return
   
def convertSeaLevel (m_iPressure):
	fPressure = m_iPressure / math.pow(1.0-altitudeMeters/44330, 5.255)
	return fPressure

def input_thread(CheckInput):
	check = raw_input()
	CheckInput = CheckInput.append(check)
	return

def mesureTempPressHygro():
	CheckInput = []
	htuReset()
	htuTest()
#	bmpTest()
	hygro = htu21df.getHumidity ()	
	thread.start_new_thread(input_thread, (CheckInput,))
	print '\nTapez "stop" pour arrêter les mesures, "test" pour tester les capteurs \net "reset" pour réinitialiser htu21d.\n'
#	print 'Hygrométrie :\t\t' 'Hygro Corrigée :\t\t' + 'Température HTU :\t\t' + 'Température BMP :\t\t' + 'Pression :'
	print 'Hygrométrie :\t\t' 'Hygro Corrigée :\t\t' + 'Température HTU :\t\t' + 'Température BMP :\t\t' + 'Pression :\t\t' +'Pression niveau de la mer :'
# Loop
	while True :
        	if CheckInput == ['stop']  : 
        		print 'Arrêt demandé.'
        		break
        	elif CheckInput == ['test'] :
        		htuTest()
        		bmpTest()
        		print 'Test effectué.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput == ['reset'] :
        		htuReset()
        		print 'Reset effectué.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput != [] :
        		print 'Commande inconnue.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
		htu21df.sampleData()
		RH = htu21df.getCompRH()
		tempHTU = htu21df.getTemperature()
		hygro = htu21df.getHumidity ()
		tempBMP = bmp180.getTemperatureCelsius()  * 1.0
		press = bmp180.getPressurePa () /100.0
# Add local altitude to obtain sea Level pressure value
# Uncomment conversion function call and change print function
		seaLevelPress = convertSeaLevel (press)
		print '%.3f\t\t\t'%hygro + '%.3f\t\t\t\t'%RH + '%.2f\t\t\t\t'%tempHTU + '%.2f\t\t\t\t'%tempBMP + '%.2f\t\t\t'%press + '%.2f\t\t\t'%seaLevelPress	
#		print '%.3f\t\t\t'%hygro + '%.3f\t\t\t\t'%RH + '%.2f\t\t\t\t'%tempHTU + '%.2f\t\t\t\t'%tempBMP + '%.2f\t\t\t'%press
		time.sleep (2)
	return

mesureTempPressHygro()
	
