#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyViCare.PyViCare import PyViCare


class GazBoiler():
    def __init__(self, email, password, client_id, 
                 token="./token.save"):
        vicare = PyViCare()
        vicare.initWithCredentials(email, 
                                   password,
                                   client_id, 
                                   token)
        self._device = vicare.devices[0]
    
    @property
    def is_online(self):
        return self._device.isOnline()
    
    @property
    def outside_temperature(self):
        if self.is_online:
            t = self._device.asGazBoiler()
            return t.getOutsideTemperature()
        else:
            return None
    
    @property
    def heating_consumption(self):
        if self.is_online:
            t = self._device.asGazBoiler()
            return t.getGasSummaryConsumptionHeatingCurrentDay()
        else:
            return None
    
    @property
    def hotwater_consumption(self):
        if self.is_online:
            t = self._device.asGazBoiler()
            return t.getGasSummaryConsumptionDomesticHotWaterCurrentDay()
        else:
            return None
    
    @property
    def model(self):
        return self._device.getModel()


if __name__ == "__main__":
    
    from configparser import ConfigParser
    
    parser = ConfigParser()
    parser.read("./config.ini")
    
    boiler = GazBoiler(**parser["viessmann"])
    if boiler.is_online:
        print("Boiler Viessmann connected !")
        print(f"Temperature : {boiler.outside_temperature} °C")
        print(f"Consommation : {boiler.heating_consumption} m3")