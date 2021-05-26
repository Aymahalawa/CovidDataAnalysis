# Data comes from Johns Hopkins University
# https://github.com/CSSEGISandData/COVID-19
# Thanks to them for making this data set public.
# You can find data beyond cumulative cases there!

from datetime import date, timedelta, datetime
import calendar
from typing import List

import seaborn as sns
import matplotlib.pyplot as plt

COUNTRY_PATH = 'countries/Egypt.txt'


def main():
    # loading the data form txt file into a list
    accum_list = load_file(COUNTRY_PATH)
    # analysing the data to know the first case found and number of days since that
    days_count = 0
    first_case = 0
    for daily in accum_list:
        if daily != 0:
            days_count += 1
        else:
            first_case += 1

    print("It has been", days_count, "days since the first reported case here")
    print("First case was reported on", get_date(first_case))

    # creating a list with the new daily cases only
    daily_list = []

    for i in range(len(accum_list) - 1):
        daily_cases = accum_list[i + 1] - accum_list[i]
        daily_list.append(daily_cases)
    # find out the maximum number of daily cases with the number of days since beginning
    max_daily = 0
    max_counter = 0
    for i in range(len(daily_list)):
        if daily_list[i] > max_daily:
            max_daily = daily_list[i]
            max_counter = i
    print("The maximum number of daily cases was", max_daily)
    print("and it was recorded on", get_date(max_counter))

    # creating a dictionary where keys are dates and new cases are values
    covid_dict = make_dict(daily_list, 'y')
    last_week_dict = {}
    last_month_dict = {}
    last_year_dict = {}

    # creating a shorter dictionary for the last week , the last month and last year
    for index, key in enumerate(covid_dict):
        if index >= (len(covid_dict) - 30):
            last_month_dict[key] = covid_dict[key]
        if index >= (len(covid_dict) - 7):
            last_week_dict[key] = covid_dict[key]
        if index >= (len(covid_dict) - 365):
            last_year_dict[key] = covid_dict[key]

    for key in last_year_dict:
        str_key_list = list(last_year_dict.keys())
        stripped = str(str_key_list).split("-")

    #print(len(str_key_list))
    #print(str_key_list)

    # asking user to choose between last week or last month graph to show
    print("")
    print("")
    print("Which graph do you like to show :")
    print("    1) Last Week Daily graph")
    print("    2) Last Month Daily graph")
    print("    3) Last Year Monthly graph")
    graph = int(input("Please enter your choice (1,2,3) : "))
    while True:
        if graph == 1:
            make_bar_plot(last_week_dict)
            break
        if graph == 2:
            make_bar_plot(last_month_dict)
            break
        if graph == 3:
            make_bar_plot(last_year_dict)
        else:
            print("Invalid Input")
            graph = int(input("Please enter 1 , 2 or 3 : "))


def get_date(days):
    # this function will calculate the date based on elapsed days since fixed start date and return as a readable
    # string
    start_date = date(2020, 1, 22)
    actual_date = start_date + timedelta(days)
    date_lst = list(str(actual_date).strip())
    year = int(date_lst[0] + date_lst[1] + date_lst[2] + date_lst[3])
    month_number = int(date_lst[5] + date_lst[6])
    month = calendar.month_abbr[month_number]
    day = int(date_lst[8] + date_lst[9])
    req_date = str(day) + '-' + month + '-' + str(year)

    return req_date


def date_option(days, freq):
    start_date = date(2020, 1, 22)
    actual_date = start_date + timedelta(days)
    date_lst = list(str(actual_date).strip())
    year = int(date_lst[0] + date_lst[1] + date_lst[2] + date_lst[3])
    month_number = int(date_lst[5] + date_lst[6])
    month = calendar.month_abbr[month_number]
    day = int(date_lst[8] + date_lst[9])
    if freq == 'm':
        return month + '-' + str(year)
    elif freq == 'w':
        return str(day) + '-' + month
    elif freq == 'y':
        return str(day) + '-' + month + '-' + str(year)


def shorten_string(long_date):
    short_list = long_date.split()
    print(short_list)
    return short_list[0] + '-' + short_list[1]


def load_file(txt_file):
    # this function will load txt file and convert it to a list per line
    accum_list = []
    f = open(txt_file)
    for line in f:
        lines = int(line)
        accum_list.append(lines)
    return accum_list


def make_dict(orig_list, freq):
    # this function will convert giving list to a dictionary where it gets the keys from other function
    new_dict = {}
    for i in range(len(orig_list)):
        new_key = date_option(i, freq)
        new_dict[new_key] = orig_list[i]

    return new_dict


def make_bar_plot(covid_dict):
    # this function will draw a bar plot from a given dictionary where its values are integers
    counts = []

    for label in covid_dict:
        counts.append(covid_dict[label])

    data = {
        'x': list(shorten_string(covid_dict.keys())),
        'y': counts
    }
    ax = sns.barplot(x='x', y='y', data=data, palette='icefire')
    ax.set(xlabel='Date', ylabel='New Cases')
    plt.show()


if __name__ == '__main__':
    main()
