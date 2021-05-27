# Data comes from Johns Hopkins University
# https://github.com/CSSEGISandData/COVID-19
# Thanks to them for making this data set public.
# You can find data beyond cumulative cases there!

import calendar
from datetime import date, timedelta
import matplotlib.pyplot as plt
import pandas as pd

print("")
print("This program analyze the Covid-19 data for any specific country")
print("")
country_req = input("Enter the country name you want to analyze : ")

COUNTRY_PATH = "countries/" + country_req + ".txt"


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
    print("It has been", days_count, "days since the first reported case")
    print("First case was reported on", get_date(first_case))

    # creating a list with the new daily cases only
    daily_list = [accum_list[0]]
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
    covid_dict = make_dict(daily_list)

    # creating a shorter dictionary for the last week , the last month and last year
    last_week_temp = {}
    last_month_temp = {}
    last_year_temp = {}
    for index, key in enumerate(covid_dict):
        if index >= (len(covid_dict) - 30):
            last_month_temp[key] = covid_dict[key]
        if index >= (len(covid_dict) - 7):
            last_week_temp[key] = covid_dict[key]
        if index >= (len(covid_dict) - 365):
            last_year_temp[key] = covid_dict[key]

    # modifying the dictionaries to make the date displayed correctly whenever required
    last_week_dict = new_dict(last_week_temp, 'w')
    last_month_dict = new_dict(last_month_temp, 'w')
    last_year_dict = new_dict(last_year_temp, 'y')

    # converting last year daily data to monthly data using pandas
    last_year_pd = pd.Series(last_year_dict, name='Cases')
    last_year_pd.index.name = 'Date'
    last_year_pd.index = pd.to_datetime(last_year_pd.index)
    monthly_df = last_year_pd.resample('MS').sum()

    # asking user to choose which graph to show
    print("")
    print("")
    print("Which graph do you like to show :")
    print("    1) Last Week Daily graph")
    print("    2) Last Month Daily graph")
    print("    3) Last Year Monthly graph")
    graph = int(input("Please enter your choice (1,2,3) : "))
    while True:
        if graph == 1:
            make_plot(to_pd(last_week_dict), 'bar')
            break
        if graph == 2:
            make_plot(to_pd(last_month_dict), 'bar')
            break
        if graph == 3:
            make_plot(monthly_df, 'line')
            break
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


def new_dict(old_dict, freq):
    # modifying the given dictionary by formatting the keys into requested format using other function
    correct_dict = {}
    for key in old_dict:
        new_dict_key = date_option(key, freq)
        correct_dict[new_dict_key] = old_dict[key]

    return correct_dict


def date_option(days, freq):
    # giving more option to show more date format
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
        return actual_date


def load_file(txt_file):
    # this function will load txt file and convert it to a list per line
    accum_list = []
    f = open(txt_file)
    for line in f:
        lines = int(line)
        accum_list.append(lines)
    return accum_list


def make_dict(orig_list):
    # this function will convert giving list to a dictionary
    temp_dict = {}
    for i in range(len(orig_list)):
        new_key = i
        temp_dict[new_key] = orig_list[i]

    return temp_dict


def make_plot(df, plot_type):
    # make a plot using DataFrame file and the type of the plot
    df.plot(x='Date', y='Cases', kind=plot_type)
    plt.show()


def to_pd(old_dict):
    # convert dictionary to DataFrame file
    df = pd.Series(old_dict, name='Cases')
    df.index.name = 'Date'
    return df


if __name__ == '__main__':
    main()

