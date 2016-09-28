#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mraa
import pyupm_mics6814
import thread, time

# i2c bus pre-cabled bus on arduino breakout
bus = 6
multiAddress = 0x04

# create sensor on the bus
mics = pyupm_mics6814.MICS6814(bus, multiAddress)

def changeI2cBusAddr(newAddr):
	mics.changeI2cAddr(newAddr)
	print 'Bus Address changed to : \t' + newAddr
	return

def calibrSensor():
	mics.doCalibrate()
	print 'Prformed re-calibration of the sensor'
	return

def input_thread(CheckInput):
	check = raw_input()
	CheckInput = CheckInput.append(check)
	return
   
def messureGaz():
	CheckInput = []
	thread.start_new_thread(input_thread, (CheckInput,))
	print '\nTapez "stop" pour arrêter les mesures, "calib" pour recalibrer.\n'
	print '\nTapez "changeAddr" pour changer d adresse sur le bus.\n'
	print '\tCO :\t' + 'NO2 :\t' + 'NH3 :\t' + 'C3H8 :\t\t' + 'C4H10 :\t' + 'CH4 :\t\t' + 'H2 :\t' + 'C2H5OH :\t'
	mics.powerOn()
	mes_co = mics.measure_CO()
	mes_no2 = mics.measure_NO2()
	mes_nh3 = mics.measure_NH3()
	mes_c3h8 = mics.measure_C3H8()
	mes_c4h10 = mics.measure_C4H10()
	mes_ch4 = mics.measure_CH4()
	mes_h2 = mics.measure_H2()
	mes_c2h5oh = mics.measure_C2H5OH()
# Loop
	while True :
        	if CheckInput == ['stop']  : 
        		print 'Arrêt demandé.'
			mics.powerOff()
        		break
        	elif CheckInput == ['calib'] :
        		calibrSensor()
        		Checkinput = CheckInput.remove('calib')
        		thread.start_new_thread(input_thread, (CheckInput,))
        	elif CheckInput == ['changeAddr'] :
        		print 'Entrez la nouvelle adresse :'
        		newAddress = CheckInput
        		changeI2cBusAddr(newAddress)
    		mes_co = mics.measure_CO()
    		mes_no2 = mics.measure_NO2()
    		mes_nh3 = mics.measure_NH3()
    		mes_c3h8 = mics.measure_C3H8()
    		mes_c4h10 = mics.measure_C4H10()
    		mes_ch4 = mics.measure_CH4()
    		mes_h2 = mics.measure_H2()
    		mes_c2h5oh = mics.measure_C2H5OH()
		print '\t%.3f\t'%mes_co + '%.3f\t'%mes_no2 + '%.3f\t'%mes_nh3 + '%.3f\t'%mes_c3h8 + '%.3f\t'%mes_c4h10 + '%.3f\t'%mes_ch4 + '%.3f\t'%mes_h2 + '%.3f\t'%mes_c2h5oh
		time.sleep (5)
	return

messureGaz()

