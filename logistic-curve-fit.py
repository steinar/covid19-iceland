#!/usr/bin/env python3
"""
Usage: ./logistic-curve-fit.py iceland.csv
"""
import csv
import datetime
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def read_csv(filename):
    l = []
    with open(filename, 'r') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            l.append((row['Date'], (int(float(row['Count']))) if row['Count'] != "" else None))
    return l


"""
Logistic function
"""


def fsigmoid(x, l, k, x0):
    return l / (1.0 + np.exp(-k * (x - x0)))


"""
Non-linear least squares fit for growth rate and sigmoid's midpoint
"""


def logistic_curve_fit(total_infected, actual_data):
    def f(x, k, x0):
        return fsigmoid(x, total_infected, k, x0)

    popt, _ = curve_fit(
        f,
        list(range(0, len(actual_data))),
        actual_data,
        bounds=([0.05, 0.3], [15.0, 50.0])
    )
    return popt


def convert_date_string(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d").strftime("%d.%m")


if __name__ == '__main__':
    input_data = read_csv(sys.argv[1])
    ydata_cumulative_actual = [x[1] for x in input_data if x[1] is not None]
    labels = [convert_date_string(x[0]) for x in input_data]
    num_days_actual = len(ydata_cumulative_actual)

    # This controls the number of days included in the plot
    num_days_total = len(labels)

    fig, ax = plt.subplots()

    # Day counter for logistic functions
    xdata_day_counter = list(range(0, num_days_total))

    # Calculate and plot predictions
    for (style, color, maxVal, label) in [
        ('-', 'green', 2000, '2000 total cases (covid.hi.is most probable)'),
        ('-', 'blue', 6000, '6000 total cases (covid.hi.is worst case)'),
        ('--', 'grey', 4000, '4000 total cases'),
    ]:
        ax.plot(xdata_day_counter, fsigmoid(xdata_day_counter, maxVal, *logistic_curve_fit(maxVal, ydata_cumulative_actual)), style,
                label=label, color=color)

    # Plot actual numbers
    ax.plot(list(range(0, num_days_actual)), ydata_cumulative_actual, 'r-', label='Actual', marker='+', markersize=10)

    # Label every 5 days
    plt.xticks(list(range(0, num_days_total, 2)), [labels[i] for i in range(0, num_days_total, 2)], rotation=90)

    # Place legent at top
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1), ncol=2)

    ax.grid(True)

    plt.show(block=True)
