#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports from mraa and upm libraries
#------------------------------------
import mraa
import thread, time, math

import pyupm_tsl2561

# Constant declarations
#----------------------
# i2c bus 1 on RaspBerry Pi
bus1 = 0
tslAddr = 0x39

# create sensors on the bus 1
#tsl = pyupm_tsl2561.TSL2561(bus1)
tsl = pyupm_tsl2561.TSL2561(bus1, tslAddr)

#Functions
#---------
# TSL2561
#*******
def mes_tslLux() :
	lux = tsl.getLux ()
	return(lux)
		
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
			elif CheckInput != [] :
				print 'Commande inconnue : "%s"\n'%CheckInput
				thread.start_new_thread(input_thread, (CheckInput,))
				del CheckInput[:]
			else :
				time.sleep (0.5)
			lux = mes_tslLux()
			if nbmes == 0 :
				print 'Intensité Lumineuse : ' 
				nbmes += 1
			elif nbmes == 9 :
				nbmes = 0
			else :
				nbmes += 1
			print '%.2f\t\t' %lux 
			
			time.sleep (5)
	else :
		print 'Bye...'
	return

measureMeteoParams()

