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

#the generator class takes as input the id and an array representing the power profile generated
import random
import csv

class Generator:
    #class-level counter
    all_gen = []

    #constructor for the class
    def __init__(self, id, profile):
        self.id = id
        self.profile = profile
        Generator.all_gen.append(self)
    
    #method to scale the generator profile
    def scale_profile(self, factor):
        self.profile = [val * factor for val in self.profile]

    #adapts the dimesnion of the profile to the new length
    #if the new length is smaller than the current one, it randomly deletes elements
    #if the new length is greater than the current one, it randomly adds elements
    #by taking the average of the two neighbours
    def resize_profile(self, new_len):
        while len(self.profile) > new_len:
            idx = random.randint(0, len(self.profile) - 1)
            del self.profile[idx]

        while len(self.profile) < new_len:
            idx = random.randint(1, len(self.profile) - 2)
            avg = (self.profile[idx - 1] + self.profile[idx + 1]) / 2
            self.profile.insert(idx, avg)

    #class method to get the all generators
    @classmethod
    def get_allGen(cls):
        return cls.all_gen
    
    #class method to create a generator from a csv file column
    @classmethod
    def from_csv_column(cls, gen_id, filepath, col_index, delimiter=","):
        with open(filepath, newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            profile = [float(row[col_index]) for row in reader if row]
        return cls(gen_id, profile)

    #class method to create a generator from a csv file row
    @classmethod
    def from_csv_row(cls, gen_id, filepath, row_index, delimiter=","):
        with open(filepath, newline='') as f:
            reader = list(csv.reader(f, delimiter=delimiter))
            profile = [float(val) for val in reader[row_index]]
        return cls(gen_id, profile)
