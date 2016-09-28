#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports from mraa and upm libraries
#------------------------------------
import mraa
import thread, time, math

import pyupm_mcp9808
import pyupm_si114x
import pyupm_mpl3115a2
import pyupm_bmp280
import pyupm_htu21d

# Constant declarations
#----------------------
# i2c bus 1 on mini breakout
bus1 = 1
siAddr = 0x18
mcpAddr = 0x60
bmeAddr = 0x77

# i2c bus 6 on mini breakout
bus6 = 6
mplAddr = 0x60
bmpAddr = 0x77
tempAddress = 0x40

localAlt = 189.5
UPPER_TEMP = 0x02
LOWER_TEMP = 0x03
CRIT_TEMP = 0x04

# create sensors on the bus 1
si = pyupm_si114x.SI114X(bus1)
mcp = pyupm_mcp9808.MCP9808(bus1)
bme = pyupm_bmp280.BME280(bus1)
#si = pyupm_si114x.SI114X(bus1, siAddr)
#mcp = pyupm_mcp9808.MCP9808(bus1, mcpAddr)
#bme = pyupm_bmp280.BME280(bus1, bmeAddr)

# create sensors on the bus 6
mpl = pyupm_mpl3115a2.MPL3115A2(bus6)
bmp = pyupm_bmp280.BMP280(bus6)
htu21df = pyupm_htu21d.HTU21D(bus6, tempAddress)
#mpl = pyupm_mpl3115a2.MPL3115A2(bus6, mplAddr)
#bmp = pyupm_bmp280.BMP280(bus6, bmpAddr)

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
	
# SI114X
#*******
def mes_siUvi() :
	si.update()
	uvi = si.getUVIndex ()
	return(uvi)
	
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
mcp.shutDown(False)
si.initialize()
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
	print '\t\t"resetBMP" pour redémarrer le capteur BMP280'
	print '\t\t"resetBME" pour redémarrer le capteur BME280'
	print '\t\t"resetHTU" pour redémarrer le capteur HTU21D'
	return (CheckInput)
	   
def measureMeteoParams():
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
						option3 = raw_input('Informations sur les capteurs : BMP280 (1) BME280 (2) MCP9808 (3) exit (0)\n----> ')
						if option3 == '0' :
							break
						elif option3 == '1' :
							get_bmSensor(bmp)
						elif option3 == '2' :
							get_bmSensor(bme)
						elif option3 == '3' :
							get_mcpSensor()
						else :
							print 'Code inconnu : %s'%option3
				elif option2 == 'changer' :
					option3 = 3
					while option3 != 0 :
						option3 = raw_input('Changement des paramètres des capteurs :\n\tMCP9808-precision (1)\n\tMCP9808-hysteresis (2)\n\tBME280_mode (3)\n\t sortir (0)\n----> ')
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
						elif option3 == '3' :
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
			elif CheckInput == ['resetBMP'] :
				reset_bmSensor(bmp)
				print 'Reset BMP effectué.'
				CheckInput.remove('resetBMP')
				thread.start_new_thread(input_thread, (CheckInput,))
			elif CheckInput == ['resetBME'] :
				reset_bmSensor(bme)
				print 'Reset BME effectué.'
				CheckInput.remove('resetBME')
				thread.start_new_thread(input_thread, (CheckInput,))
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
			tempHR = mcp.getTemp()
			si.update()
			uvi = si.getUVIndex()
			bmp.update()
			tempBMP = bmp.getTemperature()
			pressBMP = bmp.getPressure() / 100.0
			bme.update()
			tempBME = bme.getTemperature()
			pressBME = bme.getPressure() / 100.0
			hygroBME = bme.getHumidity()
			mpl.sampleData()
			pressMPL = mpl.getPressure() / 100.0
			tempMPL = mpl.getTemperature()
			tempHTU = 
			RH
			hygroHTU 
			print 'UV Index : %.2f\t' %uvi + 'Humid(BME) : %2.1f\t' %hygroBME + 'Temp(MCP) : %.4f °C\t\t' %tempHR + 'Temp(BMP) : %.2f °C  ' %tempBMP +  'Temp(BME) : %.2f °C  ' %tempBME + 'Temp(MPL) : %.2f °C\t' %tempMPL + 'Press(BMP) : %.2f hPa  ' %pressBMP + 'Press(BME) : %.2f hPa  ' %pressBME + 'Press(MPL) : %.2f hPa' %pressMPL 
			time.sleep (60)
	else :
		print 'Bye...'
	return

measureMeteoParams()

