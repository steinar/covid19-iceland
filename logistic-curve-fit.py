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


def fsigmoid(x, l, k, x0):
    """
    Logistic function

    :param x: x-value
    :param l: Max value
    :param k: Growth rate
    :param x0: midpoint (x-shift)
    :return: y-value
    """
    return l / (1.0 + np.exp(-k * (x - x0)))


def logistic_curve_fit(total_infected, actual_data):
    """
    Non-linear least squares fit for growth rate and sigmoid's midpoint

    :param total_infected: Assumed total number of infections
    :param actual_data: Ordered actual actual data
    :return: k and x0 value of the logistic function
    """

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


def plot_graph(ax, totalCases, ydata_predictions, ydata_actual, show_legend=False):
    # Calculate and plot predictions
    colors = ["green", "grey", "blue"]

    for (maxVal, ydata, color) in zip(totalCases, ydata_predictions, colors):
        ax.plot(xdata_day_counter, ydata, label="%s total cases" % maxVal, color=color)

    # Plot actual numbers
    ax.plot(list(range(0, len(ydata_actual))), ydata_actual, 'r', linestyle='', label='Actual', marker='+',
            markersize=10)

    # Rotate labels
    plt.sca(ax)
    plt.xticks(rotation=90)

    if show_legend:
        # Place legent at top
        ax.legend(loc='lower left', bbox_to_anchor=(0, 1), ncol=2)

    ax.grid(True)


if __name__ == '__main__':
    input_data = read_csv(sys.argv[1])
    ydata_cumulative_actual = [x[1] for x in input_data if x[1] is not None]
    ydata_new_actual = [0] + [
        ydata_cumulative_actual[i] - ydata_cumulative_actual[i - 1]
        for i
        in range(1, len(ydata_cumulative_actual))
    ]
    labels = [convert_date_string(x[0]) for x in input_data]

    # This controls the number of days included in the plot
    num_days_total = len(labels)

    # Day counter for logistic functions
    xdata_day_counter = list(range(0, num_days_total))

    # Most probable/worst case from Covid.hi.is
    case_totals = [1500, 1900, 2300]

    # Y-axis data for cumulative cases
    prediction_cumulative = [
        fsigmoid(xdata_day_counter, maxVal, *logistic_curve_fit(maxVal, ydata_cumulative_actual))
        for maxVal in case_totals
    ]

    # Y-axis data for new cases
    prediction_new = [
        [0] + [ydata[i] - ydata[i - 1]
               for i
               in range(1, len(ydata))
               ]
        for ydata
        in prediction_cumulative
    ]

    # Columns
    print(*map(lambda s: s.rjust(9), ["day"] + [str(x) for sl in zip(case_totals, case_totals) for x in sl]))

    # Print data table
    for i in range(0, num_days_total):
        sys.stdout.write("%s".rjust(10) % labels[i])
        for (maxVal, day_cumulative, day_new) in zip(case_totals,
                                                     map(lambda ydata: ydata[i], prediction_cumulative),
                                                     map(lambda ydata: ydata[i], prediction_new)):
            sys.stdout.write((" %.2f" % day_cumulative).rjust(10))
            sys.stdout.write((" %.2f" % day_new).rjust(10))
        sys.stdout.write("\n")

    fig, ax = plt.subplots(2)
    plt.setp(ax, xticks=list(range(0, len(labels), 1)), xticklabels=[labels[i] for i in range(0, len(labels), 1)])

    # Plot cumulative cases
    plot_graph(ax[0], case_totals, prediction_cumulative, ydata_cumulative_actual, True)

    # Plot new cases
    plot_graph(ax[1], case_totals, prediction_new, ydata_new_actual)

    plt.show(block=True)
