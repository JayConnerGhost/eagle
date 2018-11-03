from __future__ import print_function 
import argparse as ap
import time
import sys
import pyric
import pyric.pyw as pyw
import pyric.utils.hardware as hw
from pyric.utils.channels import rf2ch

def execute(dev):
      print('setting up...')
      ifaces=pyw.interfaces()
      wifaces=pyw.winterfaces()

      if dev  not in ifaces:
        print("Device {0} is not valid, use one of {1}".format(dev, ifaces))
        return
      elif dev not in wifaces:
        print("Devise {0} is not wireless, use one of {1}".format(dev, wifaces))

      print("Regulatory Domain Currently: ", pyw.regget()) 
      dinfo =pyw.devinfo(dev)
      card =dinfo['card']
      pinfo = pyw.phyinfo(card)
      driver = hw.ifdriver(card.dev)
      chipset =hw.ifchipset(driver)
      msg = "Using {0} currently in mode: {1}\n".format(card,dinfo['mode'])
      msg += "\tDriver: {0} Chipset: {1}\n".format(driver,chipset)
      if dinfo['mode'] == 'managed':
        msg += "\tcurrently on channel {0} width {1}\n".format(rf2ch(dinfo['RF']),
                                                               dinfo['CHW'])
      msg += "\tSupports modes {0}\n".format(pinfo['modes'])
      msg += "\tSupports commands {0}".format(pinfo['commands'])
      msg += "\thw addr {0}".format(pyw.macget(card))
      print(msg)

      print ('Preparing pent0 for monitor mode')
      pdev='pent0'

      pcard = pyw.devadd(card, pdev, 'monitor')

      for iface in pyw.ifaces(card):
            if iface[0].dev !=pcard.dev:
                  print("deleting {0} in mode {1}".format(iface[0],iface[1]))
                  pyw.devdel(iface[0])
      pyw.up(pcard)
      print("using pcard")
      print("Setting channel to 6 NOHT")
      pyw.chset(pcard,6,None)
      msg = "Virtual interface {0} in monitor mode on ch 6".format(pcard)
      print(msg + ", using hwaddr: {0}".format(pyw.macget(pcard)))

#------
if __name__ == '__main__':
    # create arg parser and parse command line args
    print("Wireless Pentest Environment using PyRIC v{0}".format(pyric.version))
    argp = ap.ArgumentParser(description="Wireless Pentest")
    argp.add_argument('-d','--dev',help="Pentesting Wireless Device")
    args = argp.parse_args()
    try:
        dname = args.dev
        if dname is None:
            print("usage: python pentest.py -d <dev>")
            sys.exit(0)
        else:
            execute(dname)
    except pyric.error as e:
        print(e)