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

#class representing a programmable load requiring coonstant power
#when supplying the load the method returns the excess power and
#if required power greater than input power it returns the input power printing an error
#ton min in hours, t is the time in the simulation frame

class Programmable_Load_W_Reactivation:
    #class-level counter
    all_programm_loads = []
    activable_loads = []
    active_loads = []

    def __init__(self, id, required_power, t_start, t_end, t_on_min, reactivation=False):
        self.load_id = id
        self.required_power = required_power
        self.t_start = t_start
        self.t_end = t_end
        self.t_on_min = t_on_min
        self.reactivation = reactivation
        self.activation_time = None
        self.power_history = [0]

        Programmable_Load_W_Reactivation.all_programm_loads.append(self)

    @classmethod
    def check_activable_loads(cls, t):
        cls.activable_loads.clear()
        for load in cls.all_programm_loads:
            if t < load.t_end and t >= load.t_start:
                cls.activable_loads.append(load)

    def activate(self, t):
        if self in Programmable_Load_W_Reactivation.activable_loads:
            if self not in Programmable_Load_W_Reactivation.active_loads:
                Programmable_Load_W_Reactivation.active_loads.append(self)
                self.activation_time = t

    def supply(self, input_power):
        if input_power >= self.required_power:
            excess_power = input_power - self.required_power
            self.power_history.append(self.required_power)
            return excess_power
        else:
            #not enough power, throw an error and block the execution of the script
            raise ValueError(f"Error: Not enough power to supply load {self.load_id}.")
    
    #class method to get all loads
    @classmethod
    def get_allLoads(cls):
        return cls.all_loads
    
    @classmethod
    def updateProgrammableLoadActivation(cls, t):
        for load in cls.all_programm_loads:
            if load in cls.active_loads:
                if t - load.activation_time >= load.t_on_min:
                    if not load.reactivation:
                        cls.active_loads.remove(load)
            else:
                load.power_history.append(0)