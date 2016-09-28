#!/usr/bin/env python
# -*- coding: utf-8 -*-


import thread, time
import pyupm_htu21d
import pyupm_bmp180
import mraa

# i2c bus
bus = 1
tempAddress = 0x40
pressAddress = 0x77
altitudeMeters = 165.5
#check = raw_input()

# create sensor on the bus
htu21df = pyupm_htu21d.HTU21D(bus, tempAddress)
bmp180 = pyupm_bmp180.BMP180(bus, pressAddress)

def reset():
	htu21df.resetSensor ()
	time.sleep(2)
	return

def test():
	htu21df.testSensor ()
	time.sleep(2)
	return

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
   
def mesureTempPressHygro():
	CheckInput = []
#	test()
	reset()
	hygro = htu21df.getHumidity ()	
	thread.start_new_thread(input_thread, (CheckInput,))
	print '\nTapez "stop" pour arrêter les mesures, "testhtu" pour tester le capteur htu21f\n'
	print '"testbmp" pour tester le capteur bmp180 et "reset" pour le réinitialiser.\n'
# Add local altitude to obtain sea Level pressure value 
#change print instruction to introduce sealevel
#	print 'Température :\t\t' +'Pression :\t\t' +'Pression niveau de la mer :'
	print 'Températurehtu :\t\t' +'Hygrométrie :\t\t' 'Hygro Corrigée :\t\t'+'Températurebmp :\t\t' +'Pression :'
# Loop
	while True :
        	if CheckInput == ['stop']  : 
        		print 'Arrêt demandé.'
        		break
        	elif CheckInput == ['reset'] :
        		reset()
        		print 'Reset effectué.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput == ['testhtu'] :
        		test()
        		print 'Test effectué.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput == ['testbmp'] :
        		testIfPresent()
        		print 'Test effectué.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput != [] :
        		print 'Commande inconnue.'
        		CheckInput = []
        		thread.start_new_thread(input_thread, (CheckInput,))
		htu21df.sampleData()
		RH = htu21df.getCompRH()
		temphtu = htu21df.getTemperature()
		hygro = htu21df.getHumidity ()
		tempbmp = bmp180.getTemperatureCelcius() /10.0
		press = bmp180.getPressurePa () /100.0
		print '\t%.3f\t\t\t\t'%temphtu + '%.3f\t\t\t'%hygro + '%.3f\t\t\t'%RH + '%.1f\t\t\t\t'%tempbmp + '%.2f\t\t\t'%press
# Add local altitude to obtain sea Level pressure value
# Uncomment conversion function call and change print function
#		seaLevelPress = convertSeaLevel (press)
#		print '%.3f\t\t\t'%temphtu + '%.3f\t\t\t'%hygro + '%.3f'%RH + '%.1f\t\t\t'%temp + '%.2f\t\t\t'%press + '%.2f\t\t\t'%seaLevelPress
		time.sleep (2)
	return
	
mesureTempPressHygro()	

