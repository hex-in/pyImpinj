# !/usr/bin/python
# -*- coding:utf-8 -*-
""" Test script."""
# Python:   3.6.5+
# Platform: Windows/Linux/MacOS
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test script( Inventory ).
# Package:  pip3 install pyImpinj.
# Drivers:  None.
# History:  2020-02-25 Ver:1.0 [Heyn] Initialization

import time
import queue
import logging

from pyImpinj import ImpinjR2KReader

from pyImpinj.constant import READER_ANTENNA
from pyImpinj.enums    import ImpinjR2KFastSwitchInventory

logging.basicConfig( level=logging.ERROR )

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

    # R2000.set_work_antenna( READER_ANTENNA['ANTENNA4'] )

    MAX_TAGS = 9
    R2000.set_work_antenna( READER_ANTENNA['ANTENNA4'] )
    while True:
        # for index in [ READER_ANTENNA['ANTENNA1'], READER_ANTENNA['ANTENNA4'] ]:
        #     R2000.set_work_antenna( antenna_array[index] )
        # for _ in range( 10 ):
        count = R2000.inventory( repeat=0xFF )
        #     if count == MAX_TAGS:
        #         break
        # if count == 0:
        #     continue
        time.sleep( 0.1 )
        print( R2000.get_and_reset_inventory_buffer( count ) )

if __name__ == "__main__":
    main()
