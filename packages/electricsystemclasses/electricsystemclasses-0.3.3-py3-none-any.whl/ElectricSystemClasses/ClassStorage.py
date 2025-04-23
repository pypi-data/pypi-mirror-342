# Copyright 2025 ropimen
#
# This file is licensed under the Server Side Public License (SSPL), Version 1.0.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# https://www.mongodb.com/legal/licensing/server-side-public-license
#
# This file is part of ElectricSystemClasses.
#
# ElectricSystemClasses is a Python package providing a collection of classes for simulating electric systems.

class Storage:
    #class counter of all storages
    all_storages = []

    def __init__(self, id, capacity, max_charge_power, max_disch_power, soc_init_kwh):
        self.storage_id = id
        self.capacity = capacity
        self.max_charge_power = max_charge_power
        self.max_disch_power = max_disch_power
        self.soc_history_kwh = [soc_init_kwh]

        Storage.all_storages.append(self)

    #method to charge the storage, returns the excess power
    def charge(self, power, t):
        excess_power = power - self.max_charge_power
        excess_energy = 0
        #recharge power greater than max charge power
        if excess_power > 0:
            energy_to_charge = self.max_charge_power * t
            #energy to be stored greater than available capacity
            if self.soc_history_kwh[-1] + energy_to_charge > self.capacity:
                excess_energy = self.soc_history_kwh[-1] + energy_to_charge - self.capacity
                excess_power += excess_energy / t
                self.soc_history_kwh.append(self.capacity)
            #energy to be stored less than available capacity
            else:
                self.soc_history_kwh.append(self.soc_history_kwh[-1] + self.max_charge_power * t)
        #recharge power less than max charge power
        else:
            #charge the vehicle at input power
            energy_to_charge = power * t
            #energy to be stored greater than available capacity
            if self.soc_history_kwh[-1] + energy_to_charge > self.capacity:
                excess_energy = self.soc_history_kwh[-1] + energy_to_charge - self.capacity
                excess_power += excess_energy / t
                self.soc_history_kwh.append(self.capacity)
            #energy to be stored less than available capacity
            else:
                self.soc_history_kwh.append(self.soc_history_kwh[-1] + power * t)
        return excess_power
    
    #method to discharge the storage, returns the excess power that cant be handled
    def discharge(self, power, t):
        excess_power = power - self.max_disch_power
        excess_energy = 0
        #discharge power greater than max discharge power
        if excess_power > 0:
            energy_to_discharge = self.max_disch_power * t
            #energy to be discharged greater than available capacity
            if self.soc_history_kwh[-1] - energy_to_discharge < 0:
                excess_energy = energy_to_discharge - self.soc_history_kwh[-1]
                excess_power += excess_energy / t
                self.soc_history_kwh.append(0)
            #energy to be discharged less than available capacity
            else:
                self.soc_history_kwh.append(self.soc_history_kwh[-1] - energy_to_discharge)
        #discharge power less than max discharge power
        else:
            #discharge the vehicle at input power
            energy_to_discharge = power * t
            #energy to be discharged greater than available capacity
            if self.soc_history_kwh[-1] - energy_to_discharge < 0:
                excess_energy = energy_to_discharge - self.soc_history_kwh[-1]
                excess_power += excess_energy / t
                self.soc_history_kwh.append(0)
            else:
                #energy to be discharged less than available capacity
                self.soc_history_kwh.append(self.soc_history_kwh[-1] - energy_to_discharge)
        return excess_power
    
    #class method to get all storages
    @classmethod
    def get_all_storages(cls):
        return cls.all_storages
    
    #class method to update storage soc values
    @classmethod
    def updateAllStg(cls, i):
        for stg in cls.all_storages:
            if len(stg.soc_history_kwh) < i:
                stg.soc_history_kwh.append(stg.soc_history_kwh[-1])