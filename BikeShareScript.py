#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 13:14:49 2018

@author: bostjan
"""

import time
import pandas as pd
import numpy as np
import json

from input_util import get_user_input

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITIES = ['chicago', 'new york', 'washington']
CityErrorMessage = "Please enter a correct city name."

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
MonthErrorMessage = "Please enter a correct month name as given in the list."

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
        'saturday']
DaysErrorMessage = "Please enter a correct weekday name as given in the list."


YES_NO = ['yes', 'no']
YesNoErrorMessage = "Wrong input!!! Please answer either yes or no."


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply"
        no month filter
        (str) day - name of the day of week to filter by, or "all" to apply
        no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!")

    # get user input for city (chicago, new york city, washington).

    city = get_user_input("Which city do you want to explore? \nPlease choose"
                          " Chicago, New York or Washington. \n> ",
                          CITIES, CityErrorMessage)

    # get user input for month (all, january, february, ... , june)

    month = get_user_input("All right! now it\'s time to decide about the "
                           "month you want to see data for. You can also just "
                           "write \'all\' to apply no month filter. \n"
                           "(e.g. all, january, february, march, april, "
                           "may, june)>",
                           MONTHS, MonthErrorMessage)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = get_user_input("One last thing. Please enter a week day you want "
                         "to analyze. You can also just type \'all\' to "
                         "apply no day filter. \n"
                         "(e.g. all, monday, tuesday, wednesday, thursday, "
                         "friday, saturday, sunday) \n>",
                         DAYS, DaysErrorMessage)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
        no month filter
        (str) day - name of the day of week to filter by, or "all" to apply
        no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create
    # new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics about the most frequent times of travel."""

    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode().loc[0]
    print("The most common month is :", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode().loc[0]
    print("The most common day of the week is :", most_common_day_of_week)

    # display the most common start hour

    most_common_start_hour = df['hour'].mode().loc[0]
    print("The most common hour of the day is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays stations and trip statistics."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode().loc[0]
    print("The most commonly used start station :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode().loc[0]
    print("The most commonly used end station :", most_common_end_station)

    # display most frequent combination of start station and end station trip

    most_common_start_end_station = df.groupby(['Start Station',
                                                'End Station']).size().idxmax()

    print("The most commonly used start/end station combination : {}, {}"
          .format(most_common_start_end_station[0],
                  most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays total/average trip duration statistics."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display avg travel time
    avg_travel = df['Trip Duration'].mean()
    print("Average travel time :", avg_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()

    # iteratively print out the total numbers of user types
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    print()

    if 'Gender' in df.columns:
        user_stats_gender(df)

    if 'Birth Year' in df.columns:
        user_stats_birth(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats_gender(df):
    """Displays gender statistics/analysis of bikeshare users."""

    # Display counts of gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    # iteratively print out the total numbers of genders
    for index, gender_count in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))

    print()


def user_stats_birth(df):
    """Displays birthdata statistics/analysis of bikeshare users."""

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # the most common birth year
    most_common_year = birth_year.mode().loc[0]
    print("The most common birth year:", most_common_year)
    # the most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)
    # the most earliest birth year
    earliest_year = birth_year.min()
    print("The earliest birth year:", earliest_year)


def display_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):

        yes = get_user_input("\nWould you like to see 5 lines of raw data?"
                             "Type \'yes\' or \'no\'\n> ",
                             YES_NO, YesNoErrorMessage)

        # retrieve and convert data to json format
        # split each json row data
        if yes != 'yes':
            break
        row_data = df.iloc[i: i + 5].to_json(orient='records',
                                             lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = get_user_input("\nWould you like to restart? "
                                 "Enter yes or no.\n",
                                 YES_NO, YesNoErrorMessage)
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()