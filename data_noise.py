# File name: data_noise.py
# Author: Julia Hardy
# Date created: 22/01/2020
# Python Version: 3.7
# program options:
# 1. Numeric description of noise of this test (provide number or numbers) --noise
# 2. Regressions, improvements (provide version(s) of driver) --performance
# 3. Any other observations --observations

import pandas as pd
import sys


def write_data_to_data_frame(csv_file):
    data = pd.read_csv(csv_file, sep='\t')
    return data


data = write_data_to_data_frame("perf_data.csv")


class DataProcess:
    def __init__(self, data_in_data_frame_format):
        self.data = data_in_data_frame_format
        self._standard_deviations = pd.Series()
        self._averages = pd.Series

    @property
    def averages(self):
        if self._averages.empty:
            self._averages = self.data.groupby('Software version')['perf value'].mean()
        return self._averages

    @property
    def standard_deviations(self):
        if self._standard_deviations.empty:
            self._standard_deviations = self.data.groupby('Software version')['perf value'].std()
        return self._standard_deviations

    def calculate_standard_deviations_variance(self):
        sum1 = sum2 = 0
        for x in self.standard_deviations:
            sum1 += x

        n = len(self.standard_deviations)
        mean = sum1 / n

        for y in self.standard_deviations:
            sum2 += (y - mean) * (y - mean)

        variance = sum2 / (n - 1)
        return variance

    def calculate_performance_change(self):
        variance = round(self.calculate_standard_deviations_variance(), 3)
        previous_value = self.averages.values[0]
        print("Software versions performance changes")
        for i, v in self.averages.items():
            diff = v - previous_value
            if diff > 0:
                diff -= variance
            elif diff < 0:
                diff += variance
            previous_value = v
            print('software version: ', i, 'performance change: ', diff)

    def data_noise_numeric_description(self):
        results = pd.concat([p.averages, p.standard_deviations], axis=1)
        results.columns = ['averages', 'standard deviation']
        variance = self.calculate_standard_deviations_variance()
        print("Data Noise represented as variance of standard deviations: {}".format(variance))
        print("Averages and standard deviations for Software version:")
        print(results)

    def calculate_additional_data(self):
        max_performance = self.data[self.data['perf value'] == self.data['perf value'].max()]
        min_performance = self.data[self.data['perf value'] == self.data['perf value'].min()]
        max_std = self.standard_deviations.idxmax()
        min_std = self.standard_deviations.idxmin()
        print("Additional data analysis for test results:")
        print("max performance value: ", float(max_performance['perf value']), ";software version: ", int(max_performance['Software version']))
        print("min performance value: ", float(min_performance['perf value']), ";software version: ", int(min_performance['Software version']))
        print("max standard deviation: ", self.standard_deviations[max_std], ";software version: ", max_std)
        print("min standard deviation: ", self.standard_deviations[min_std], ";software version: ", min_std)
        print("differences between standard deviations for software version: ")

        previous_value = self.standard_deviations.values[0]
        for i, v in self.standard_deviations.items():
            diff = v - previous_value
            previous_value = v
            print('software version: ', i, 'std change: ', diff)


if __name__ == "__main__":
    p = DataProcess(data)
    options = "Choose one option to run : --noise, --performance, --observations"
    if len(sys.argv) > 1:
        if sys.argv[1] == '--noise':
            p.data_noise_numeric_description()
        elif sys.argv[1] == '--performance':
            p.calculate_performance_change()
        elif sys.argv[1] == '--observations':
            p.calculate_additional_data()
        else:
            print(options)
    else:
        print(options)

