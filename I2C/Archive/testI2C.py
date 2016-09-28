#http://www.mikroe.com/click/altitude/      mpl3115a2
#http://cache.nxp.com/files/sensors/doc/data_sheet/MPL3115A2.pdf?pspll=1

#https://www.adafruit.com/products/1899
#https://www.adafruit.com/datasheets/1899_HTU21D.pdf

import time
import mraa
import pyupm_htu21d
import pyupm_mpl3115a2
import pyupm_guvas12d
import pyupm_mq135
import pyupm_mics6814
import pyupm_gas
import pyupm_th02

bus = 1
bus = 6
I2C_STD = 0
I2C_FAST = 1
I2C_HIGH = 2 
tempAddress = 0x40
pressAdress = 0x60
multiAdress = 0x04

i2cBus = mraa.I2c(bus)
i2cBus.frequency(I2C_STD)
i2cBus.frequency(I2C_FAST)
mraa.printError(i2cBus.frequency(I2C_FAST))
MRAA: SUCCESS


press = pyupm_mpl3115a2.MPL3115A2(bus, pressAdress)
temp = pyupm_htu21d.HTU21D(bus, tempAddress)
uv = pyupm_guvas12d.GUVAS12D(0)
air = pyupm_mq135.MQ135(1)
ch4 = pyupm_gas.MQ4(2)
th02 = pyupm_th02.TH02(bus, tempAddress)

i2cBus.address(tempAddress)
temp.resetSensor ()
temp.sampleData()
RH = temp.getCompRH()
temperature = temp.getTemperature()
hygro = temp.getHumidity ()
print '\t%.3f\t\t'%temperature + '%.3f\t\t'%hygro + '%.3f'%RH

i2cBus.address(pressAdress)
press.sampleData()
temperatureP = press.getTemperature()
pressure = press.getPressure()
pressea = press.getSealevelPressure()
alt = press.getAltitude()
print '\t%.3f\t\t'%temperatureP + '%.3f\t\t'%pressure + '%.3f\t\t'%pressea + '%.3f'%alt
ultrav = uv.value(5.0,10)
print ultrav
resist = air.getResistance()
corresist = air.getCorrectedResistance(temperature, hygro)
ppm = air.getPPM()
corppm = air.getCorrectedPPM(temperature, hygro)
print '\t%.3f\t\t\t'%resist + '%.3f\t\t\t'%corresist + '%.3f\t\t\t'%ppm + '%.3f'%corppm


TH02_ADDR = 0x40 # device address
TH02_REG_STATUS = 0x00
TH02_REG_DATA_H = 0x01
TH02_REG_DATA_L = 0x02
TH02_REG_CONFIG = 0x03
TH02_REG_ID = 0x11
TH02_STATUS_RDY_MASK = 0x01
TH02_CMD_MEASURE_HUMI = 0x01
TH02_CMD_MEASURE_TEMP = 0x11

# HTU21D Commands 
HTU21D_READ_TEMP_HOLD     0xE3
HTU21D_READ_HUMIDITY_HOLD 0xE5
HTU21D_WRITE_USER_REG     0xE6
HTU21D_READ_USER_REG      0xE7
HTU21D_SOFT_RESET         0xFE
# User Register Bit Definition 
HTU21D_DISABLE_OTP        0x02
HTU21D_HEATER_ENABLE      0x04
HTU21D_END_OF_BATTERY     0x40
HTU21D_RESO_RH12_T14      0x00
HTU21D_RESO_RH8_T12       0x01
HTU21D_RESO_RH10_T13      0x80
HTU21D_RESO_RH11_T11      0x81

MPL3115A2_NAME  =      "mpl3115a2"
MPL3115A2_I2C_ADDRESS =   0x60
MPL3115A2_DEVICE_ID =     0xc4
MPL3115A2_STATUS =        0x00
MPL3115A2_OUT_PRESS =     0x01  #/* MSB first, 20 bit */
MPL3115A2_OUT_TEMP =      0x04  #/* MSB first, 12 bit */
MPL3115A2_WHO_AM_I =      0x0c
MPL3115A2_PT_DATA_CFG =   0x13
MPL3115A2_P_MIN  =        0x1C
MPL3115A2_T_MIN  =        0x1F
MPL3115A2_P_MAX =         0x21
MPL3115A2_T_MAX =         0x24
MPL3115A2_CTRL_REG1 =     0x26
MPL3115A2_CTRL_SBYB =     0x01  #/* Standby (not) */
MPL3115A2_CTRL_OST =      0x02  #/* One-shot trigger */
MPL3115A2_CTRL_RESET =    0x04  #/* RESET device */
MPL3115A2_CTRL_ALT_MODE = 0x80  #/* Altitude mode */
MPL3115A2_SETOVERSAMPLE(a) ((a & 7) << 3)
MPL3115A2_GETOVERSAMPLE(a) ((a >> 3) & 7)
MPL3115A2_MAXOVERSAMPLE   7


bus = 6

# mraa
i2c = mraa.I2c(bus)
i2c.address(0x40)
i2c.frequency(mraa.I2C_FAST)
print i2c

i2c.writeReg(TH02_REG_CONFIG, TH02_CMD_MEASURE_HUMI)
print i2c.readReg(TH02_REG_STATUS)

i2c.writeReg(TH02_REG_CONFIG, TH02_CMD_MEASURE_TEMP)
status = i2c.readReg(TH02_REG_STATUS)
data = i2c.readReg(TH02_REG_DATA_H)


print i2c.readReg(TH02_REG_STATUS)

i2c.writeReg(TH02_REG_CONFIG, TH02_CMD_MEASURE_HUMI)
humidity = i2c.readReg(TH02_REG_DATA_H) << 8
temperature = i2c.readReg(TH02_REG_DATA_H)
temperature |= i2c.readReg(TH02_REG_DATA_L)
print data

mraa.printError()



i2c.writeReg(TH02_REG_CONFIG, TH02_CMD_MEASURE_HUMI)
humidity = i2c.readReg(TH02_REG_DATA_H) << 8
humidity |= i2c.readReg(TH02_REG_DATA_L)
humidity >>= 4
print humidity
hum = humidity / 16.0 - 24.0
print hum

temperature = i2c.readReg(TH02_REG_DATA_H) << 8
temperature |= i2c.readReg(TH02_REG_DATA_L)
temperature >>= 2;
temp = temperature / 32.0 - 50.0


****************************************************
# htu21df
htu21df = pyupm_htu21d.HTU21D(bus)
print htu21df
# grove
grove = pyupm_grove.Grove()
print grove


data = bytearray([0xE3,0xE6])
print 'data value : ' + str(data)

toto = i2c.write(data)
toto = i2c.writeByte(0xE3)
print 'toto value : ' + str(toto_1) + ' 2 ' + str(toto_2)

time.sleep(1.3)
d = 3
temp=[]
u = i2c.read(d)

print 'nb requested : ' + str(d) + ' nb read : ' + str(u_1) + str(u_2)


LowLevel mraa
=============
mraa.getVersion()
'v0.9.4-4-g8e8ed7d'
mraa.getI2cBusCount ()
9
mraa.getPlatformName ()
'Intel Edison'
mraa.getPlatformVersion ()
'arduino'
mraa.getI2cBusId (6)   
6
mraa.getI2cBusId (1)
-1
i2c = mraa.I2c(6)
mraa.getDefaultI2cBus()
i2c.address(0x60)

>>> import mraa
>>> import pyupm_htu21d
>>> import pyupm_mq135
>>> import pyupm_gas
>>> bus = 6
>>> tempAddress = 0x40
>>> temp = pyupm_htu21d.HTU21D(bus, tempAddress)
>>> air = pyupm_mq135.MQ135(2)
>>> ch4 = pyupm_gas.MQ4(2)
>>> temp.resetSensor ()
>>> temp.sampleData()
0
>>> RH = temp.getCompRH()
>>> temperature = temp.getTemperature()
>>> hygro = temp.getHumidity ()
>>> print '\t%.3f\t\t'%temperature + '%.3f\t\t'%hygro + '%.3f'%RH
	23.849		35.992		36.164
>>> air.getCorrectionFactor(temperature, hygro)
0.94084972143173218
>>> air.getPPM()
5.7011075019836426
>>> air.getCorrectedPPM(temperature, hygro)
4.1966991424560547
>>> ch4.getSample()
207

********************************
mics6814
========
import mraa
import pyupm_mics6814

bus = 6
multiAdress = 0x04
mics = pyupm_mics6814.MICS6814(bus, multiAdress)



i2c = mraa.I2c(bus)
i2c.address(multiAdress)
# readData
i2c.writeByte(0x11)
status = i2c.read(4)

MPL3115A2
=========
>>> import time
>>> import mraa
>>> import pyupm_mpl3115a2
>>> bus = 6
>>> I2C_STD = 0
>>> pressAdress = 0x60
press = pyupm_mpl3115a2.MPL3115A2(bus, pressAdress)
MPL3115A2_WHO_AM_I =      0x0c

>>> i2c = mraa.I2c(bus)
>>> i2c.address(0x60)
i2c.frequency(I2C_STD)
0














