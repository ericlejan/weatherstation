#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports from mraa and upm libraries
#------------------------------------
import mraa
import thread, time, math

import pyupm_si114x

# Constant declarations
#----------------------
# i2c bus 1 on RaspBerry Pi
bus1 = 0
siAddr = 0x18

# create sensors on the bus 1
si = pyupm_si114x.SI114X(bus1)
#si = pyupm_si114x.SI114X(bus1, siAddr)

#Functions
#---------
# SI114X
#*******
def mes_siUvi() :
	si.update()
	uvi = si.getUVIndex ()
	return(uvi)
	
#Activate or test some sensors
#---------------------
si.initialize()
	
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
			si.update()
			uvi = si.getUVIndex()
			if nbmes == 0 :
				print 'UV Index : ' 
				nbmes += 1
			elif nbmes == 9 :
				nbmes = 0
			else :
				nbmes += 1
			print '%.2f\t\t' %uvi 
			
			time.sleep (5)
	else :
		print 'Bye...'
	return

measureMeteoParams()

