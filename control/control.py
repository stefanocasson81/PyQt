import os
import sys
#from time import sleep
#from typing import List
from model.AppConfigurator import AppConfigurator

class Control():
   def __init__(self):
      self.app_config = AppConfigurator('./config/isin_config.yaml')
      self.app_config.loadConfig()
      self.app_config.getIsinCode()
   
