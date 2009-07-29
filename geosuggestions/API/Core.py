from APIApp import APIApp
from geosuggestions import Geosuggestions

class CoreHandler (Geosuggestions, APIApp) :

  def __init__ (self) :
    Geosuggestions.__init__(self)    
    APIApp.__init__(self)

