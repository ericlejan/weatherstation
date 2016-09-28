import time
import mraa
import math


# i2c bus, if you have a Raspberry Pi Rev A, change this to 0
bus = 6
i2c = mraa.I2c(bus)

# HTU21D-F Address
addr = 0x40
i2c.address(addr)

#define TH02_ADDR                
addr = 0x40 // device address
#define TH02_REG_STATUS          0x00
#define TH02_REG_DATA_H          0x01
#define TH02_REG_DATA_L          0x02
#define TH02_REG_CONFIG          0x03
#define TH02_REG_ID              0x11
#define TH02_STATUS_RDY_MASK     0x01
rdstatus = 0x01
#define TH02_CMD_MEASURE_HUMI    0x01
rdhumi = 0x01
#define TH02_CMD_MEASURE_TEMP    0x11
rdtemp = 0x11

# HTU21D-F Commands
rdtemp = 0xE3
rdhumi = 0xE5
wtreg = 0xE6
rdreg = 0xE7
reset = 0xFE

def htu_reset():
	i2c.writeByte(handle, reset) # send reset command
	time.sleep(0.2) # reset takes 15ms so let's give it some time

def read_temperature():
        data = bytearray ([]]
	data = i2c.writeByte(rdtemp) # send read temp command
	time.sleep(0.055) # readings take up to 50ms, lets give it some time
	data.append(i2c.read(data, 3)) # vacuum up those bytes
	t1 = byteArray[0] # most significant byte msb
	t2 = byteArray[1] # least significant byte lsb
	temp_reading = (t1 * 256) + t2 # combine both bytes into one big integer
	temp_reading = math.fabs(temp_reading) # I'm an idiot and can't figure out any other way to make it a float 
	temperature = ((temp_reading / 65536) * 175.72 ) - 46.85 # formula from datasheet
	return temperature

#def read_humidity():
#	handle = pi.i2c_open(bus, addr) # open i2c bus
#	pi.i2c_write_byte(handle, rdhumi) # send read humi command
#	time.sleep(0.055) # readings take up to 50ms, lets give it some time
#	(count, byteArray) = pi.i2c_read_device(handle, 3) # vacuum up those bytes
#	pi.i2c_close(handle) # close the i2c bus
#	h1 = byteArray[0] # most significant byte msb
#	h2 = byteArray[1] # least significant byte lsb
#	humi_reading = (h1 * 256) + h2 # combine both bytes into one big integer
#	humi_reading = math.fabs(humi_reading) # I'm an idiot and can't figure out any other way to make it a float
#	uncomp_humidity = ((humi_reading / 65536) * 125 ) - 6 # formula from datasheet
#	# to get the compensated humidity we need to read the temperature
#	temperature = read_temperature()
#	humidity = ((25 - temperature) * -0.15) + uncomp_humidity
#	return humidity



