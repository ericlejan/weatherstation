#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports from mraa and upm libraries
#------------------------------------
import mraa
import thread, time, math

import pyupm_mpl3115a2

# Constant declarations
#----------------------
# i2c bus 1 on RaspBerry Pi
bus1 = 0
mplAddr = 0x60

localAlt = 156.5
UPPER_TEMP = 0x02
LOWER_TEMP = 0x03
CRIT_TEMP = 0x04

# create sensors on the bus 1
mpl = pyupm_mpl3115a2.MPL3115A2(bus1)
#mpl = pyupm_mpl3115a2.MPL3115A2(bus1, mplAddr)

#Functions
#---------
#MPL3115A2
#*********
def reset_mpl() :
	mpl.reserSensor()
	return

def dump_mpl() :
	mpl.dumpSensor
	return
	
def test_mpl() :
	mpl.testSensor()
	return
	
def mes_mplPT() :
	mpl.sampleData()
	mplPress = mpl.getPressure()
	mplTemp = mpl.getTemperature
	mplSealevpress = mpl.getSealevelPressure(localAlt)
	return(mplPress, mplTemp, mplSealevpress)
	
def convertSeaLevel (m_iPressure):
	fPressure = m_iPressure / math.pow(1.0 - localAlt/44330, 5.255)
	return fPressure
	
# Main function
###############	
def input_thread(CheckInput):
	check = raw_input()
	CheckInput.append(check)
	return
	
def init_Thread () :
	CheckInput = []
	thread.start_new_thread(input_thread, (CheckInput,))
	print 'Instructions :  \t"stop" pour arrêter les mesures.\n'
	return (CheckInput)
	   
def measureMeteoParams():
	nbmes = 0
	while True :
		option1 = raw_input('Instructions :  \t"start" pour démarrer les mesures "check" pour la maintenance "exit" pour sortir.\n--> ')
		if option1 == 'exit' :
			break
		elif option1 == 'start' :
			break
		else :
			print 'Commande inconnue : "%s"\n'%option1
# Main loop
	if option1.strip() == 'start' :
		CheckInput = init_Thread()
		while True :
			if CheckInput == ['stop']: 
				print 'Arrêt demandé.'
				break
			elif CheckInput != [] :
				print 'Commande inconnue : "%s"\n'%CheckInput
				thread.start_new_thread(input_thread, (CheckInput,))
				del CheckInput[:]
			else :
				time.sleep (0.5)
			mpl.sampleData()
			pressMPL = mpl.getPressure() / 100.0
			tempMPL = mpl.getTemperature()
			seaLevelPress = convertSeaLevel (pressMPL)
			if nbmes == 0 :
				print 'Temp(MPL) : \tPress(MPL) : \tPress(SealevelMPL) : ' 
				nbmes += 1
			elif nbmes == 9 :
				nbmes = 0
			else :
				nbmes += 1
			print '%.2f °C\t' %tempMPL + '%.2f hPa\t' %pressMPL  + '%.2f hPa\t' %seaLevelPress
			
			time.sleep (5)
	else :
		print 'Bye...'
	return

measureMeteoParams()

