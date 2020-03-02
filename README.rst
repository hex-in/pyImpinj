Impinj R2000 protocol. 
=========================
 
    pyImpinj is a protocol library for R2000 reader.


Installation
------------

* Compile and install the library::

    pip3 install pyImpinj

Usage
-----

* In Python 3
  
    from pyImpinj import ImpinjR2KReader
  

Example
-------

    **from pyImpinj import ImpinjR2KReader**

    TAG_QUEUE = queue.Queue( 1024 )

    R2000 = ImpinjR2KReader( TAG_QUEUE, address=1 )

    R2000.connect( 'COM9' )
    
    R2000.worker_start()
    
    R2000.rt_inventory( repeat=100 )
    
    print( TAG_QUEUE.get( ) )
    
V1.2 (2020-02-27)
-----------------

* Release ver1.2

    New add get(set)_frequency_region  

    New add set_frequency_region_user  

    New add test/auto_config.py

V1.1 (2020-02-20)
-----------------

* Release ver1.1

