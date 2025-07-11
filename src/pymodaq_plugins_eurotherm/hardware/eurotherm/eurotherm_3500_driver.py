# -*- coding: utf-8 -*-
"""
Python wrapper for Eurotherm 3500 process controllers, with communication via the Modbus RTU protocol.

Highly inspired from minimalmodbus library's example driver for Eurotherm 3500 (eurotherm3500.py file 
originally created by Jonas Berg <pyhys@users.sourceforge.net> in 2012) and adapted for PyMoDAQ software
"""
from tkinter import E
import minimalmodbus, serial
# from typing import Union#, Tuple
from time import sleep

DEBUG = True

class Eurotherm3500(minimalmodbus.Instrument):
    """Instrument class for Eurotherm 3500 process controller. 
    
    Communicates via Modbus RTU protocol (via RS232 or RS485), using the *MinimalModbus* Python module.
    Implemented with these function codes (in decimal):
        
    ==================  ====================
    Description         Modbus function code
    ==================  ====================
    Read registers      3
    Write registers     16
    ==================  ====================
    """
    unit:               str = '°C'  # Instrument.Display.Units - Unité d'affichage de l'instrument
    possibleUnits:      list[str] = ['°C', '°F', 'K'] # Possible units
    instrumentSerial:   serial.Serial = None
    slaveAddress:       int = 1     # 0 value is only for slave broadcasting

    defaults = {
        # 'encoding':             'ascii',
        'baudrate':             19200,
        # 'timeout':              2000,
        'parity':               serial.PARITY_NONE,
        'bytesize':             8,
        'stopbits':             serial.STOPBITS_ONE,
        'timeout':              0.05,
        'write_timeout':        2.0
    }

    def __init__(
        self,
        portname:       str,# = 'COM4',
        slaveaddress:   int = '1'   # 0 value is only for slave broadcasting
        ):
        """
        Args:
            * portname (str): port name
            * slaveaddress (int): slave address in the range 1 to 247
        """
        # minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.instrumentSerial = serial.Serial(
            port=None, # Port is set to none to not open port immediately
            baudrate=self.defaults['baudrate'],
            parity=self.defaults['parity'],
            bytesize=self.defaults['bytesize'],
            stopbits=self.defaults['stopbits'],
            timeout=self.defaults['timeout'],
            write_timeout=self.defaults['write_timeout'],
            )
        self.slaveAddress: int = slaveaddress
        self.instrumentSerial.port = portname # Port is set afterward none to not open port immediately

    def open_communication(self):
        """Instrument serial port opening
        Returns
        -------
        info: str
        opened: bool
            False if initialization failed otherwise True
        """
        try:
                
            super().__init__(port = self.instrumentSerial, slaveaddress = self.slaveAddress)
            # self.instrumentSerial.open() # Already called in parent init

            sleep(0.2) # Make sure connection is established before doing anything else

        except: # serial.SerialException:
            info = f"Failed to open instrument serial at port : {self.instrumentSerial.port}"
            # raise
            pass
        else:
            info =  f"Eurotherm 3500 connection opened at port : {self.instrumentSerial.port}"

        opened = self.instrumentSerial.is_open

        return info, opened

    def close_communication(self):
        self.instrumentSerial.close()
        return not self.instrumentSerial.is_open
        

    ###############
    #### Loop 1 ###
    ###############
    
    ## Process value
    
    def get_pv_loop1(self):
        """Return the process value (PV) for loop1."""
        return self.read_register(1, 1)

    ## Auto/manual mode
    
    def is_manual_loop1(self):
        """Return True if loop1 is in manual mode."""
        return self.read_register(3, 1) > 0
        
    ## Setpoint
    
    def get_targetSP_loop1(self):
        """Return the current setpoint (SP) target for loop1."""
        return self.read_register(2, 1)
    
    def get_workingSP_loop1(self):
        """Return the current working setpoint (SP) for loop1."""
        return self.read_register(5, 1)
    
    def get_SPselect_loop1(self):
        """Return the selected setpoint (SP) for loop1.
        Reads 0 for SP1 and 1 for SP2
        But returns value = 1 for SP1 and 2 for SP2
        """
        return (self.read_register(15, 1) + 1)

    def set_SPselect_loop1(self, value):
        """Set the selected setpoint (SP) for loop1.
        Input 1 for SP1 and 2 for SP2
        """
        self.write_register(15, (value - 1), 1)

    def set_SP1_loop1(self, value):
        """Set the SP1 for loop1.
        
        Note that this is not necessarily the working setpoint.
        Args:
            value (float): Setpoint (most often in degrees)
        """
        self.write_register(24, value, 1)

    def set_SP2_loop1(self, value):
        """Set the SP2 for loop1.
        
        Note that this is not necessarily the working setpoint.
        Args:
            value (float): Setpoint (most often in degrees)
        """
        self.write_register(25, value, 1)

    def get_SPrate_loop1(self):
        """Return the current setpoint (SP) rate for loop1 : Loop.1.SP.Rate """
        return self.read_register(35, 1)

    ## PID

    def get_P_loop1(self, value):
        """Return the current Proportional Band for loop1."""
        return self.read_register(6, 1)
    
    def get_I_loop1(self, value):
        """Return the current Proportional Band for loop1."""
        return self.read_register(8, 1)
    
    def get_D_loop1(self, value):
        """Return the current Proportional Band for loop1."""
        return self.read_register(9, 1)
    
    ## Output

    def get_OPrate_loop1(self):
        """Return the current output (OP) rate for loop1 : Loop.1.OP.Rate """
        return self.read_register(37, 1)

    def get_activeOut_loop1(self):
        """Return the current active output for loop1.
        May be in % of output range"""
        return self.read_register(4, 1)

    ###############
    #### Loop 2 ###
    ###############
    
    ## Process value
    
    def get_pv_loop2(self):
        """Return the process value (PV) for loop2."""
        return self.read_register(1025, 1)

    ## Auto/manual mode
    
    def is_manual_loop2(self):
        """Return True if loop2 is in manual mode."""
        return self.read_register(1027, 1) > 0
        
    ## Setpoint
    
    def get_targetSP_loop2(self):
        """Return the tager setpoint (SP) target for loop2."""
        return self.read_register(1026, 1)
    
    def get_workingSP_loop2(self):
        """Return the current working setpoint (SP) for loop2."""
        return self.read_register(1029, 1)
    
    def get_SPselect_loop2(self):
        """Return the selected setpoint (SP) for loop2.
        Reads 0 for SP1 and 1 for SP2
        But returns value = 1 for SP1 and 2 for SP2
        """
        return (self.read_register(1039, 1) + 1)

    def set_SPselect_loop2(self, value):
        """Set the selected setpoint (SP) for loop2.
        Input 1 for SP1 and 2 for SP2
        """
        self.write_register(1039, (value - 1), 1)

    def set_SP1_loop2(self, value):
        """Set the SP1 for loop2.
        
        Note that this is not necessarily the working setpoint.
        Args:
            value (float): Setpoint (most often in degrees)
        """
        self.write_register(1048, value, 1)

    def set_SP2_loop2(self, value):
        """Set the SP2 for loop2.
        
        Note that this is not necessarily the working setpoint.
        Args:
            value (float): Setpoint (most often in degrees)
        """
        self.write_register(1049, value, 1)

    def get_SPrate_loop2(self):
        """Return the current setpoint (SP) rate for loop2."""
        return self.read_register(1059, 1)

    def is_sprate_disabled_loop1(self):
        """Return True if Loop1 setpoint (SP) rate is disabled."""
        return self.read_register(78, 1) > 0

    def disable_sprate_loop1(self):
        """Disable the setpoint (SP) change rate for loop1. """
        VALUE = 1
        self.write_register(78, VALUE, 0) 
        
    def enable_sprate_loop1(self):
        """Set disable=false for the setpoint (SP) change rate for loop1.
        
        Note that also the SP rate value must be properly set for the SP rate to work.
        """
        VALUE = 0
        self.write_register(78, VALUE, 0) 
    
    ## PID

    def get_P_loop2(self):
        """Return the current Proportional Band for loop2."""
        return self.read_register(1030, 1)
    
    def get_I_loop2(self):
        """Return the current Proportional Band for loop2."""
        return self.read_register(1032, 1)
    
    def get_D_loop2(self):
        """Return the current Proportional Band for loop2."""
        return self.read_register(1033, 1)
    
    ## Output

    def get_OPrate_loop2(self):
        """Return the current output (OP) rate for loop2."""
        return self.read_register(1061, 1)

    def get_activeOut_loop2(self):
        """Return the current active output for loop2.
        May be in % of output range"""
        return self.read_register(1028, 1)
        # return self.read_register(1109, 1) Loop.2.OP.Ch1Out

    ####################
    #### IO Module 1 ###
    ####################

    # def get_rangeHigh_module1(self):
    #     """Return the range of power supply output within the max 0-10 V range : IO.Mod.1.A.RangeHigh """
    #     return self.read_register(x, 1) # register not reachable through Modbus, no available SCADA address


    ########################
    #### Instrument Info ###
    ########################
    
    def get_instrument_version(self):
        """Return the instrument version information of the device."""
        return self.read_register(107)

    # def get_instrument_homepage(self):
    #     """Return the instrument homepage of the device."""
    #     return self.read_register(106)

    def get_instrument_type(self):
        """Return a string to precise whether it is a 3508 or 3504 process controller."""
        res = self.read_register(122) # Returns 0 for 3508 device and 1 for 3504 device
        if res == 0:
            return "Eurotherm 3508"
        elif res == 1:
            return "Eurotherm 3504"
        else:
            return "Unknown" 

    def get_instrument_display_units(self):
        """"""
        value = self.read_register(516) # Returns 0 if Deg C; 1 if Deg F; 2 if K

        if value == 0:
            self.unit = "°C"
        elif value == 1:
            self.unit =  "°F"
        elif value == 2:
            self.unit =  "K"
        else:
            self.unit =  "unknown unit"

        return self.unit
    
    def set_instrument_display_units(self, unitsStr):
        """Accepted values = {'°C'; '°F'; 'K'}"""

        # Write 0 if Deg C; 1 if Deg F; 2 if K
        if unitsStr == "°C":
            value = 0
        elif unitsStr == "°F":
            value = 1
        elif unitsStr == "K":
            value = 2
        else:
            raise ValueError
        
        self.write_register(516, value, 1)
        self.unit = unitsStr

########################
## Testing the module ##
########################

if __name__ == '__main__':
    print( 'TESTING EUROTHERM 3500 MODBUS MODULE ON COM4 PORT WITH SLAVE ADDRESS 1')

    serialPort = 'COM4'
    slaveAddress = 1

    a = Eurotherm3500(serialPort, slaveAddress)
    a.debug = DEBUG
    info, opened = a.open_communication()

    if opened == False:
        print(f"Failed to open serial port", serialPort, " --> Opening info = ", info)
    else:
        if a.debug == True:
            print(f"Successfully opened serial port ", serialPort, "  --> Opening info = ", info)
        
        # if a.instrumentSerial.is_open:
        print( 'PV:                     {0}'.format(  a.get_pv_loop1()             ))
        print( 'Target SP:              {0}'.format(  a.get_targetSP_loop1()       ))
        print( 'Working SP:             {0}'.format(  a.get_workingSP_loop1()      ))
        print( 'SP-rate Loop1 disabled: {0}'.format(  a.is_sprate_disabled_loop1() ))
        print( 'Output:                 {0} %'.format( a.get_activeOut_loop1()      ))
        print( 'Manual mode Loop1:      {0}'.format(  a.is_manual_loop1()          ))
        print( 'SP rate:                {0}'.format(  a.get_SPrate_loop1()         ))
        print( 'OP rate:                {0} %'.format( a.get_OPrate_loop1()      ))


        print( 'Instrument version:     {0}'.format(  a.get_instrument_version()      ))
        # print( 'Instrument homepage:    {0}'.format(  a.get_instrument_homepage()  ))

        answer = a.get_instrument_type()
        print(f"Connected instruement is an {a.get_instrument_type()}.")

        print(f'Instrument display units:            {a.get_instrument_display_units()}')

        print( 'EUROTHERM TESTING DONE!' )

# pass

