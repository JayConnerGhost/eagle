#!/usr/bin/python3

import sys, getopt
import ifaddr
import pyric             # pyric errors
import pyric.pyw as pyw  # iw functionality

def main(argv):
  
   try:
      opts, args = getopt.getopt(argv,"hl:i:",["--list","--interfaceName="])
   except getopt.GetoptError:
      print ('eagle.py -l <list network interfaces> -i <put interface into monitor mode >')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':   
         print ('eagle.py -l <list network interfaces> -i <put interface into monitor mode >')

         sys.exit()
      elif opt in ("-l", "--list"):
        #todo - return list of network interfaces
        listInterfaces()
      elif opt in ("-i", "--interfaceName"):
       #todo put network card into monitor mode
       listenOnInterface(arg)
 
def listInterfaces():
   print("interfaces") 
   adapters = ifaddr.get_adapters()
   for adapter in adapters:
        print ("IPs of network adapter " + adapter.nice_name)
        for ip in adapter.ips:
            print ("   %s/%s" % (ip.ip, ip.network_prefix))
def listenOnInterface(interfaceName):
    try:
      print("is valid interface " + str(pyw.isinterface(interfaceName)))
      print("is wireless interface " + str(pyw.iswireless(interfaceName)))
      w0=pyw.getcard(interfaceName)
      print(str(w0))
      print("is valid card "+ str(pyw.validcard(w0)))
      print("performing a card restart to ensure health ")
      pyw.down(w0)
      pyw.up(w0)
      print("card ready")
    except pyric.error as e: 
      print(str(e))
if __name__ == "__main__":
   main(sys.argv[1:])