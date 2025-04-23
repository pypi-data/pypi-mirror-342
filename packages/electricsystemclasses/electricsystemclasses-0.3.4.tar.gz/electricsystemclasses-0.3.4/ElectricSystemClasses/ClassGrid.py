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

#class grid, it has no power limits
class Grid:
    def __init__(self, id):
        self.id = id
        self.power_history = [0]

    def exchange(self, power_value):
        self.power_history.append(power_value)

    #method to get update the power history if the grid is not exchanging in the simul frame
    def updateGrid(self, i):
        if len(self.power_history) < i:
            self.power_history.append(0)
