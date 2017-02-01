#!/usr/bin/python
#
# Script for Raspberry Pi read of RLS encoder via GPIO
# This version is MODIFIED to only generate the clock
# Author: Dayle Kotturi
# Site: 94560
#
# Date   : 1/20/2014
#

# The wiring for the encoder connector is as follows:
# 1 : 5V
# 2 : GND
# 3 : SL OUT P
# 4 : SL OUT M
# 5 : CLK P
# 6 : CLK M
# 7 : GND
# 8 : 5V

# Imports
import RPi.GPIO as GPIO
import time
import os

# Define GPIO to encoder mapping
SLOUTP = 18
SLOUTM = 23
CLKP = 18 
CLKM = 27 

# Timing constants
E_DELAY = 0.00005  # hold 50 usec delay to begin
E_PULSE = 0.000005 # 5 usec delay for each pulse -> 200 kHz edge freq -> 100 kHz

def falling_edge_pulse():
  clkp = 0
  clkm = 1
  GPIO.output(CLKP,clkp)
  GPIO.output(CLKM,clkm)
  time.sleep(E_PULSE)


def rising_edge_pulse():
  clkp = 1
  clkm = 0
  GPIO.output(CLKP,clkp)
  GPIO.output(CLKM,clkm)
  time.sleep(E_PULSE)


def pulse():
  rising_edge_pulse()
  falling_edge_pulse()


def main():
  # Main program block
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

  print "Begin"

  # read the outputs from SN5C1168ERGY which are the data from the AM8192B
  GPIO.setup(SLOUTP, GPIO.IN)
  GPIO.setup(SLOUTM, GPIO.IN)
  # use raspberry pi to create the clocks
  GPIO.setup(CLKP, GPIO.OUT)
  GPIO.setup(CLKM, GPIO.OUT)

  try:
    while 1:

      print 'Initializing'
      # step 0: give rising edge clock
      rising_edge_pulse()

      # prolong it for 50 additional usec
      time.sleep(E_DELAY)

      falling_edge_pulse()

      while 1:
        pulse()

  except KeyboardInterrupt:
         GPIO.cleanup()

if __name__ == '__main__':
  main()


