#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports from mraa and upm libraries
#------------------------------------
import mraa
import thread, time, math

import pyupm_mcp9808

# Constant declarations
#----------------------
# i2c bus 0 on RaspBerry Pi 
bus1 = 0
mcpAddr = 0x60
UPPER_TEMP = 0x02
LOWER_TEMP = 0x03
CRIT_TEMP = 0x04


# create sensors on the bus 1
mcp = pyupm_mcp9808.MCP9808(bus1)
#mcp = pyupm_mcp9808.MCP9808(bus1, mcpAddr)

#Functions
#---------
# MCP9808
#********
def get_mcpSensor():
	unity = mcp.isCelsius()
	upper = mcp.getMonitorReg (UPPER_TEMP)
	lower = mcp.getMonitorReg (LOWER_TEMP)
	critic = mcp.getMonitorReg (CRIT_TEMP)
	hyst = mcp.getHysteresis ()
	resol = mcp.getResolution ()
	idManuf = mcp.getManufacturer ()
	mcpId = mcp.getDevicedId ()
	if unity :
		print 'We are measuring in Celsius'
	else :
		print 'We are measuring in Fahrenheit'
	print '\tLower T° : %.3f\n'%lower + '\tUpperT° : %.3f\n'%upper + '\tCritical T° : %.3f\n'%critic
	print 'Hysteresis value : %.3f'%hyst
	print 'Resolution : %.4f'%resol
	print 'Manufacturer Id : %d'%idManuf
	print 'Device Id : %d\n'%mcpId
	return
	
def mes_mcpTemp():
	mcpTemp = mcp.getTemp ()
	return (mcpTemp)

#Activate or test some sensors
#---------------------
#mcp.shutDown(False)
	
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
		elif option1 == 'check' :
			option2 = 'ready'
			while option2.strip != exit :
				option2 = raw_input('Taper "info" pour avoir des informations, "changer" pour modifier les paramètres des capteurs, "exit" pour sortir.\n---> ')
				if option2 == 'exit':
					break
				elif option2 == 'info':
					option3 = 4
					while option3 != 0 :
						option3 = raw_input('Informations sur les capteurs : MCP9808 (1) exit (0)\n----> ')
						if option3 == '0' :
							break
						elif option3 == '1' :
							get_mcpSensor()
						else :
							print 'Code inconnu : %s'%option3
				elif option2 == 'changer' :
					option3 = 3
					while option3 != 0 :
						option3 = raw_input('Changement des paramètres des capteurs :\n\tMCP9808-precision (1)\n\tMCP9808-hysteresis (2)\n\t sortir (0)\n----> ')
						if option3 == '0' :
							break
						elif option3 == '1' :
							val = raw_input("precision value (LOW MED HI MAX) : ")
							if val == 'LOW' :
								mcp.setResolution (0x00)
							elif val == 'MED' :
								mcp.setResolution (0x01)
							elif val == 'HI' :
								mcp.setResolution (0x02)
							elif val == 'MAX' :
								mcp.setResolution (0x03)
							else :
								print 'Commande inconnue : "%s"\n'%val
						elif option3 == '2' :
							val = raw_input("Hysteresis value  (HYST_0 HYST_1_5 HYST_3_0 HYST_6_0) : ")
							if val == 'HYST_0' :
								mcp.setHysteresis (0x0000)
							elif val == 'HYST_1_5' :
								mcp.setHysteresis (0x0002)
							elif val == 'HYST_3_0' :
								mcp.setHysteresis (0x0004)
							elif val == 'HYST_6_0' :
								mcp.setHysteresis (0x0006)
							else :
								print 'Commande inconnue : "%s"\n'%val
						else :
							print 'Code inconnu : "%s"\n'%option3
				else :
					print 'Commande inconnue : "%s"\n'%option2
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
			tempHR = mcp.getTemp()
			if nbmes == 0 :
				print 'Temp(MCP) : ' 
				nbmes += 1
			elif nbmes == 9 :
				nbmes = 0
			else :
				nbmes += 1
			print '%.4f °C\t' %tempHR
			
			time.sleep (5)
	else :
		print 'Bye...'
	return

measureMeteoParams()

