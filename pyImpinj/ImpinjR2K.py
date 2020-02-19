# !/usr/bin/python
# -*- coding:utf-8 -*-
""" Impinj R2000 module."""
# Python:   3.6.5+
# Platform: Windows/Linux/MacOS
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Impinj R2000 module protocol.
# Package:  None.
# Drivers:  None.
# History:  2020-02-17 Ver:1.0 [Heyn] Initialization

import struct
import libscrc
import logging

from enums import ImpinjR2KCommands
from constant import TAG_MEMORY_BANK

# logging.basicConfig( level=logging.DEBUG )

class ImpinjR2KProtocols( object ):
    """
        R2000 = ImpinjR2KProtocols( )
        print( R2000.reset( ) )
        print( R2000.power( 20, 21, 20, 20 ) )
        print( R2000.work_antenna(0) )

    """
    def register( command ):
        def decorator( func ):
            def wrapper( self, *args, **kwargs ):
                data = func( self, *args, **kwargs )
                data = [] if data is None else data
                message = [ self.__head ]
                message.extend( [ 3 + len( data ), self.__address, command ] )
                message.extend(  data   )
                message.append( libscrc.lrc( bytes( message ) ) )
                self.__address = data[0] if command == ImpinjR2KCommands.SET_READER_ADDRESS else self.__address
                # logging.debug( [ hex(x) for x in message ] )

                if self.serial is not None:
                    try:
                        return self.serial.write( bytes( message ) )
                    except BaseException as err:
                        logging.error( err )
                return bytes( message )
            return wrapper
        return decorator

    def __init__( self, address=0xFF, serial=None ):
        self.serial = serial
        self.__head, self.__address = 0xA0, address

    @register( ImpinjR2KCommands.RESET )
    def reset( self ):
        pass

    @register( ImpinjR2KCommands.SET_UART_BAUDRATE )
    def baudrate( self, value=115200 ):
        """
            38400bps or 115200bps.
        """
        return [ 4 if value == 115200 else 3 ]

    @register( ImpinjR2KCommands.SET_READER_ADDRESS )
    def address( self, addr=0 ):
        assert ( 0 <= addr <= 254 )
        return [ addr ]

    @register( ImpinjR2KCommands.GET_FIRMWARE_VERSION )
    def version( self ):
        pass

    @register( ImpinjR2KCommands.SET_WORK_ANTENNA )
    def work_antenna( self, antenna=0 ):
        """ Set reader work antenna.
            @param      antenna(int) : 0 ~ 3
        """
        assert ( 0 <= antenna <= 3 )
        return [ antenna ]

    @register( ImpinjR2KCommands.SET_RF_POWER )
    def power( self, ant1=0x00, ant2=0x00, ant3=0x00, ant4=0x00 ):
        assert ( 0 <= ant1 <= 33 ) and ( 0 <= ant2 <= 33 ) and ( 0 <= ant3 <= 33 ) and ( 0 <= ant4 <= 33 )
        return [ ant1, ant2, ant3, ant4 ]

    @register( ImpinjR2KCommands.SET_TEMPORARY_OUTPUT_POWER )
    def fast_power( self, value=22 ):
        assert ( 22 <= value <= 33 )
        return [ value ]

    @register( ImpinjR2KCommands.SET_BEEPER_MODE )
    def beeper( self, mode=0 ):
        assert ( 0 <= mode <= 2 )
        return [ mode ]

    @register( ImpinjR2KCommands.INVENTORY )
    def inventory( self, repeat=0xFF ):
        return [ repeat ]

    @register( ImpinjR2KCommands.REAL_TIME_INVENTORY )
    def rt_inventory( self, repeat=0xFF ):
        return [ repeat ]

    @register( ImpinjR2KCommands.CUSTOMIZED_SESSION_TARGET_INVENTORY )
    def session_inventory( self, session='S1', target='A', repeat=1 ):
        sess = dict( S0=0, S1=1, S2=2, S3=3 )
        return [ sess.get( session, 1 ), 1 if target == 'B' else 0, repeat ]

    @register( ImpinjR2KCommands.FAST_SWITCH_ANT_INVENTORY )
    def fast_switch_ant_inventory( self, param=dict( A=0, ACounter=1, B=1, BCounter=1, C=2, CCounter=1, D=3, DCounter=1, Interval=5, Repeat=1 ) ):
        """
            When xCounter > 3, disabled the antenna.
            Interval : ( Unit : ms  )
            Repeat   : ( Uint : int )
        """

        DISABLED = 4
        return [ param.get( 'A', DISABLED ), param.get( 'ACounter', 1 ),
                 param.get( 'B', DISABLED ), param.get( 'BCounter', 1 ),
                 param.get( 'C', DISABLED ), param.get( 'CCounter', 1 ),
                 param.get( 'D', DISABLED ), param.get( 'DCounter', 1 ),
                 param.get( 'Interval', 5 ),
                 param.get( 'Repeat',   1 ) ]

    def gpio( self, port, level=False ):
        """
            ONLY [R] : GPIO1 and GPIO2
            ONLY [W] : GPIO3 and GPIO4

            e.g:
                R2000 = ImpinjR2KProtocols( )
                print( R2000.gpio( 1 ) )
        """
        assert ( 1 <= port <= 4 )
        if 3 <= port <= 4:
            ret = ImpinjR2KProtocols.register( ImpinjR2KCommands.SET_GPIO_VALUE )( lambda x, y : y )( self, [ port, 0x01 if level else 0x00 ] )
        else:
            ret = ImpinjR2KProtocols.register( ImpinjR2KCommands.GET_GPIO_VALUE )( lambda x, y : y )( self, [  ] )
        return ret

    @register( ImpinjR2KCommands.GET_READER_TEMPERATURE )
    def temperature( self ):
        pass

    @register( ImpinjR2KCommands.READ )
    def read( self, bank='EPC', addr=2, size=8, password=[ 0 ]*4 ):
        body = []
        body.append( TAG_MEMORY_BANK.get( bank, 1 ) )
        body.append( addr )
        body.extend( list( struct.pack( '>H', size ) ) )
        body.extend( password )
        return body

    @register( ImpinjR2KCommands.WRITE )
    def write( self, data:list, bank='EPC', addr=2, password=[ 0 ]*4 ):
        body = []
        body.extend( password )
        body.append( TAG_MEMORY_BANK.get( bank, 1 ) )
        body.append( addr )
        body.extend( list( struct.pack( '>H', len(data)//2 ) ) )
        body.extend( data )
        return body

    @register( ImpinjR2KCommands.WRITE_BLOCK )
    def write_block( self, data:list, bank='EPC', addr=2, password=[ 0 ]*4 ):
        body = []
        body.extend( password )
        body.append( TAG_MEMORY_BANK.get( bank, 1 ) )
        body.append( addr )
        body.extend( list( struct.pack( '>H', len(data)//2 ) ) )
        body.extend( data )
        return body

    @register( ImpinjR2KCommands.LOCK )
    def lock( self, bank='EPC', lock_type='OPEN', password=[ 0 ]*4 ):
        """
            @param
                bank      = [ 'USER', 'TID', 'EPC', 'ACCESS_PASSWORD', 'KILL_PASSWORD' ]
                lock_type = [ 'OPEN', 'LOCK', 'OPEN_FOREVER', 'LOCK_FOREVER' ]
        """
        assert ( type( password ) is list )
        membank  = dict( USER=1, TID=2, EPC=3, ACCESS_PASSWORD=4, KILL_PASSWORD=5 )
        locktype = dict( OPEN=0, LOCK=1, OPEN_FOREVER=2, LOCK_FOREVER=3 )
        body = []
        body.extend( password )
        body.append( membank.get( bank, 1 ) )
        body.append( locktype.get( lock_type, 1 ) )
        return body

    @register( ImpinjR2KCommands.KILL )
    def kill( self, password=[ 0 ]*4 ):
        assert ( type( password ) is list )
        return password

    @register( ImpinjR2KCommands.ISO18000_6B_INVENTORY )
    def iso1800_6b_inventory( self ):
        """ ISO 18000 - 6B """
        pass





R2000 = ImpinjR2KProtocols( )
print( R2000.kill() )
# print( R2000.power( 20,21,20,20) )
# print( R2000.work_antenna(0) )
# R2000.gpio = ( 4, True )
# print( R2000.gpio )
# R2000.address( 5 )
# print( R2000.reset() )