# !/usr/bin/python
# -*- coding:utf-8 -*-
""" Test script."""
# Python:   3.6.5+
# Platform: Windows/Linux/MacOS
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test script.
# Package:  None.
# Drivers:  None.
# History:  2020-02-20 Ver:1.0 [Heyn] Initialization

import time
import queue
import logging

from pyImpinj import ImpinjR2KReader

from pyImpinj.constant import READER_ANTENNA
from pyImpinj.enums    import ImpinjR2KFastSwitchInventory

logging.basicConfig( level=logging.INFO )

def main( ):
    TAG_QUEUE = queue.Queue( 1024 )
    R2000 = ImpinjR2KReader( TAG_QUEUE, address=1 )

    try:
        R2000.connect( 'COM9' )
    except BaseException as err:
        print( err )
        return

    R2000.worker_start()
    R2000.fast_power( 22 )
    # print( R2000.get_rf_port_return_loss() )
    # print( R2000.get_ant_connection_detector() )
    # print( R2000.set_ant_connection_detector( 10 ) )

    antenna_array = [ READER_ANTENNA['ANTENNA1'],
                      READER_ANTENNA['ANTENNA2'],
                      READER_ANTENNA['ANTENNA3'],
                      READER_ANTENNA['ANTENNA4'] ]
    index = 0
    while True:
        try:
            data = TAG_QUEUE.get( timeout=0.1 )
        except BaseException:
            print( R2000.set_work_antenna( antenna_array[index] ) )
            # time.sleep( 0.1 )
            R2000.rt_inventory( repeat=10 )
            # time.sleep( 0.5 )
            # R2000.fast_switch_ant_inventory( param = dict( A=ImpinjR2KFastSwitchInventory.ANTENNA1, Aloop=1,
            #                                                B=ImpinjR2KFastSwitchInventory.ANTENNA4, Bloop=1,
            #                                                C=ImpinjR2KFastSwitchInventory.DISABLED, Cloop=1,
            #                                                D=ImpinjR2KFastSwitchInventory.DISABLED, Dloop=1,
            #                                                Interval = 0,
            #                                                Repeat   = 1 ) )
            
            index = index + 1
            index = 0 if index >= len( antenna_array ) else index
            continue

        if data['type'] == 'ERROR':
            index = index + 1
            index = 0 if index >= len( antenna_array ) else index
            print( R2000.set_work_antenna( antenna_array[index] ) )
            R2000.rt_inventory( repeat=10 )

        print( data )

if __name__ == "__main__":
    main()
