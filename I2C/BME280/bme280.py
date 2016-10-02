#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports from mraa and upm libraries
#------------------------------------
import mraa
import thread, time, math

import pyupm_bmp280

# Constant declarations
#----------------------
# i2c bus 1 on mini breakout
bus1 = 0
bmeAddr = 0x77

localAlt = 156.5
UPPER_TEMP = 0x02
LOWER_TEMP = 0x03
CRIT_TEMP = 0x04

# create sensors on the bus 1
bme = pyupm_bmp280.BME280(bus1)
#bme = pyupm_bmp280.BME280(bus1, bmeAddr)

#Functions
#---------
# bmp and bme 280
#****************
def get_bmSensor(thisSensor) :
	name = thisSensor.getModuleName ()
	bmpId = thisSensor.getChipID ()
	print 'capteur : %s\t'%name + 'Id : %d\n'%bmpId
	return
	
def reset_bmSensor(thisSensor) :
	thisSensor.reset()
	return

def mes_bmTPA(thisSensor) :
	thisSensor.update ()
	bmTemp = thisSensor.getTemperature (false)
	bmPress = thisSensor.getPressure ()
	bmAlt = thisSensor.getAltitude (1013.25)
	return(bmTemp, bmPress, bmAlt)
	
def mes_bmeHum(thisSensor) :
	thisSensor.update ()
	bmeHum = thisSensor.getHumidity ()
	return(bmeHum)
	
def convertSeaLevel (m_Pressure):
	s_Pressure = m_Pressure / math.pow(1.0 - localAlt/44330, 5.255)
	return s_Pressure
	
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
	print '\t\t"resetBME" pour redémarrer le capteur BME280'
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
						option3 = raw_input('Informations sur le capteurs BME280 (1) exit (0)\n----> ')
						if option3 == '0' :
							break
						elif option3 == '1' :
							get_bmSensor(bme)
						else :
							print 'Code inconnu : %s'%option3
				elif option2 == 'changer' :
					option3 = 3
					while option3 != 0 :
						option3 = raw_input('Changement des paramètres des capteurs :\n\tBME280_mode (1)\n\t sortir (0)\n----> ')
						if option3 == '0' :
							break
						elif option3 == '1' :
							val = raw_input("precision value (0 1 2 3 4 5 ) : ")
							if val == '0' :
								bme.setUsageMode(0)
							elif val == '1' :
								bme.setUsageMode(1)
							elif val == '2' :
								bme.setUsageMode(2)
							elif val == '3' :
								bme.setUsageMode(3)
							elif val == '4' :
								bme.setUsageMode(4)
							elif val == '5' :
								bme.setUsageMode(5)
							else :
								print 'Code inconnu : %s'%val
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
			elif CheckInput == ['resetBME'] :
				reset_bmSensor(bme)
				print 'Reset BME effectué.'
				CheckInput.remove('resetBME')
				thread.start_new_thread(input_thread, (CheckInput,))
			elif CheckInput != [] :
				print 'Commande inconnue : "%s"\n'%CheckInput
				thread.start_new_thread(input_thread, (CheckInput,))
				del CheckInput[:]
			else :
				time.sleep (0.5)
			bme.update()
			tempBME = bme.getTemperature()
			pressBME = bme.getPressure() / 100.0
			hygroBME = bme.getHumidity()
			seaLevelPress = convertSeaLevel (pressBME)
			if nbmes == 0 :
				print 'Humid(BME) : \tTemp(BME) : \tPress(BME) : \tPress(SealevelPress) : ' 
				nbmes += 1
			elif nbmes == 9 :
				nbmes = 0
			else :
				nbmes += 1
			print "{0:.2f} %\t\t{1:.2f} °C\t{2:.2f} hPa\t{2:.2f} hPa".format(hygroBME,tempBME,pressBME,seaLevelPress)
			
			time.sleep (5)
	else :
		print 'Bye...'
	return

measureMeteoParams()

