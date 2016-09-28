#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports from mraa and upm libraries
#------------------------------------
import mraa
import thread, time, math

import pyupm_htu21d

# Constant declarations
#----------------------
# i2c bus 1 on RaspBerryPI
bus1 = 0
tempAddress = 0x40

# create sensors on the bus 1
htu21df = pyupm_htu21d.HTU21D(bus1)
#htu21df = pyupm_htu21d.HTU21D(bus1, tempAddress)

#Functions
#---------
# HTU21D-F
#*********
def htuReset():
	htu21df.resetSensor ()
	time.sleep(2)
	return

def htuTest():
	htu21df.testSensor ()
	time.sleep(2)
	return

#Activate or test some sensors
#---------------------
htuReset()
htuTest()
	
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
	print '\t\t"resetHTU" pour redémarrer le capteur HTU21D'
	return (CheckInput)
	   
def measureMeteoParams():
	nbmes = 0
	while True :
		option1 = raw_input('Instructions :  \t"start" pour démarrer les mesures "exit" pour sortir.\n--> ')
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
			elif CheckInput == ['resetHTU'] :
				htuReset()
				print 'Reset HTU effectué.'
				CheckInput.remove('resetHTU')
				thread.start_new_thread(input_thread, (CheckInput,))
			elif CheckInput != [] :
				print 'Commande inconnue : "%s"\n'%CheckInput
				thread.start_new_thread(input_thread, (CheckInput,))
				del CheckInput[:]
			else :
				time.sleep (0.5)
			htu21df.sampleData()
			tempHTU = htu21df.getTemperature()
			rhHTU = htu21df.getCompRH()
			hygroHTU = htu21df.getHumidity ()
			if nbmes == 0 :
				print 'Humid(HTU) : \tHumid(HTUcor) : \tTemp(HTU) : ' 
				nbmes += 1
			elif nbmes == 9 :
				nbmes = 0
			else :
				nbmes += 1
			print '%2.1f\t\t' %hygroHTU + '%2.1f\t\t\t' %rhHTU + '%.2f °C' %tempHTU 
			
			time.sleep (5)
	else :
		print 'Bye...'
	return

measureMeteoParams()

