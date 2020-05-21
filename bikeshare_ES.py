import time
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
list(CITY_DATA.keys())
months = ['all','january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday' ,'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some 2017 US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nEnter a city to be analized(chicago, new york city or washington):\n').lower()
    while city not in list(CITY_DATA.keys()):
        print('\nOops! thats not a valid city name, please try again. Look out for spelling!\n')
        city = input('Enter a city to be analized(chicago, new york city or washington):\n').lower()


    # get user input for month (all, january, february, ... , june)
    month = input('\nChoose a a month to be analyzed (all, january, february, march, april, may, or june):\n').lower()
    while month not in months:
        print('\nOops! thats not a valid option for month, please try again\n')
        month = input('Choose a a month to be analyzed (all, january, february, march, april, may, or june):\n').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nEnter a day of the week to be analized (all, monday, tuesday, wednesday, thursday, friday, saturday or sunday):\n').lower()
    while day not in days:
        print('\nOops! thats not a valid option for day, please try again')
        day = input('Enter a day of the week to be analized (all, monday, tuesday, wednesday, thursday, friday, saturday or sunday):\n').lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable. Algo add additional columns for specific analysis.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_DATA[city]
    df = pd.read_csv('/Users/ebselman/Desktop/UDACITY/PYTHON/bikeshare/{}'.format(filename))
    days = ['monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday' ,'sunday']
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['day_of_week_name'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour
    df['date'] = df['Start Time'].dt.date
    df['Start - End Stations'] = df['Start Station'] + ' - ' + df['End Station']
    df['Trip Duration (mins)'] = round(df['Trip Duration']/60, 0)

    if city != 'washington':
        df['Age'] = 2017 - df['Birth Year']

    if month != 'all':

        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':

        day = days.index(day)

        df = df[df['day_of_week'] == day]

    return df


def time_stats(city, month, day, df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month onlye if city == all
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = df['month'].mode()[0]

    if month == 'all':
        print('MONTH STATS\n')
        print('The months with the most rides is: ', months[most_common_month - 1].title())

    # Ask if User wants to see the total rides by month
        more_info_month = input('\nDo you want to see the evolution of trip by month? (yes o no):\n').lower()
        while more_info_month not in ['yes', 'no']:
            print('Sorry, not a valid answer, retry')
            more_info_month = input('Do you want to see the evolution of trip by month? (yes o no):\n').lower()

    # groupby and then plot
        if more_info_month == 'yes':
            print('\nprinting graph...\n')
            month_rides = df.groupby(['month'])['Start Time'].count()

            plt.plot(month_rides, 'b-o')
            plt.ylabel('Total Trips)')
            plt.xlabel('Month')
            plt.title('Trips per Month', fontsize = 14, color='black' )
            plt.grid(True)
            plt.xlim([1,6])
            print(plt.show())


    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    days = ['monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday' ,'sunday']
    if day == 'all':
        print('\n')
        print('DAY STATS\n')

        print('The day with the most rides is: ', days[most_common_day].title())

        # Ask if they want to see more information per day
        more_info_day = input('\nDo you want to see how many rides there are in each day of the week? (yes o no):\n').lower()
        while more_info_day not in ('yes', 'no'):
            print('\norry, not a valid answer, retry\n')
            more_info_day = input('Do you want to see how many rides there are in each day of the week? (yes o no):\n').lower()


        # Group by day_of_week and show graph
        if more_info_day == 'yes':
            print('\nprinting graph...\n')
            day_rides = df.groupby(['day_of_week_name'])['Start Time'].count().loc[[i.title() for i in days]]

            plt.plot(day_rides, 'b-o')
            plt.ylabel('Total Trips)')
            plt.xlabel('Day of the Week')
            plt.title('Trips per Day of the Week', fontsize = 14, color='black' )
            plt.xlim([0,6])
            plt.grid(True)
            plt.show()



    # display the most common start hour
    print('\n')
    print('TIME STATS:\n')
    most_common_hour = df['start_hour'].mode()[0]

    print("the most common hour for starting a trip is {} o'clock: ".format(most_common_hour))


# Ask if they want to see more information per hour
    more_info_hour = input('\nDo you want to see how many rides started at each hour? (yes o no):\n').lower()
    while more_info_hour not in ['yes', 'no']:
        print('\nSorry, not a valid answer, retry\n')
        more_info_hour = input('Do you want to see how many rides started at each hour? (yes o no):\n').lower()

    # Group by day_of_week and show graph
    if more_info_hour == 'yes':
        print('\nprinting graph...\n')
        hour_rides = df.groupby(['start_hour'])['Start Time'].count()

        plt.plot(hour_rides, 'b-o')
        plt.ylabel('Total Trips')
        plt.xlabel('Hour')
        plt.title('Trips per Hour of the Day', fontsize = 14, color='black' )
        plt.grid(True)
        plt.xlim([0,23])
        plt.ylim([0, hour_rides.max()+500])
        plt.xticks(hour_rides.index)
        plt.show()

    # Ask if they want to graph of evolution by day in the complete period:
    if month == 'all' and day == 'all':

        print('\n')
        print('COMPLETE TIME SERIES STATS\n')
        more_info_date = input('\nDo you want to see the complete evolution of rides by day in the whole time frame? (yes o no):\n').lower()
        while more_info_date not in ['yes', 'no']:
            print('\nSorry, not a valid answer, retry\n')
            more_info_date = input('Do you want to see the complete evolution of rides by day in the whole time frame? (yes o no):\n').lower()

        months = mdates.MonthLocator()  # every month
        days = mdates.DayLocator()
        months_fmt = mdates.DateFormatter('%m')


        if more_info_date == 'yes': # Show Graph if Yes
            data = df.groupby(['date'])['Trip Duration'].count() # NOTE: group by date(day)
            fig, ax = plt.subplots() # NOTE: create pyplot
            ax.plot(data)

            # format the ticks
            ax.xaxis.set_major_formatter(months_fmt)
            ax.xaxis.set_minor_locator(months)
            ax.xaxis.set_minor_locator(days)

            # format the coords message box
            ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
            ax.format_ydata = lambda x: '$%1.2f' % x  # format the price.
            ax.grid(True)

            # Format the Plot
            fig.autofmt_xdate()
            plt.ylabel('Total Trips')
            plt.xlabel('Month')
            plt.title('Evolution of Trip by Day', fontsize = 14, color='black')
            plt.show()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(city, month, day, df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nMOST COMMON START STATION\n')

    most_common_start = df['Start Station'].mode()[0]
    print('The most common start station is: ', most_common_start)

    # display most commonly used end station
    print('\nMOST COMMON END STATION\n')
    most_common_end = df['End Station'].mode()[0]
    print('The most common end stations is: ', most_common_end)

    # Input and show bar graph of most common start and end stations
    more_info_stations = input('\nDo you wish to see a graph with the most common start and end stations (yes o no):\n').lower()
    while more_info_stations not in ['yes', 'no']:
        print('\nSorry, not a valid answer, retry\n')
        more_info_stations = input('Do you wish to see a graph with the most common start and end stations (yes o no):\n').lower()

    if more_info_stations == 'yes':
        print('\nprinting graph...\n')
        most_common_start_df = df.groupby(['Start Station'])['Start Time'].count().sort_values(ascending=False)[:10]
        most_common_end_df = df.groupby(['End Station'])['Start Time'].count().sort_values(ascending=False)[:10]

        plt.rcParams.update({'figure.autolayout': True})
        fig, axs = plt.subplots(2, 1, figsize=(10, 7))

        axs[0].barh(list(most_common_start_df.index), list(most_common_start_df.values))
        axs[1].barh(list(most_common_end_df.index), list(most_common_end_df.values))
        labels = axs[0].get_xticklabels()
        labels = axs[1].get_xticklabels()
        axs[0].set(xlim=[most_common_start_df.values.min(), most_common_start_df.values.max()+5], xlabel='Total Rides', ylabel='Station', title='Top 10 Start Stations')
        axs[1].set(xlim=[most_common_end_df.values.min(), most_common_end_df.values.max()+5], xlabel='Total Rides', ylabel='Station', title='Top 10 End Stations',)
        plt.show()



    # display most frequent combination of start station and end station trip
    print('\nMOST COMMON START-END TRIP\n')

    most_frequent_combo = df['Start - End Stations'].mode()[0]
    print('The most frequent combination of start and end stations is: ', most_frequent_combo)

    more_info_start_end = input('\nDo you wish to visualize a graph with the top 10 start-end station combos? (yes o no):\n').lower()
    while more_info_start_end not in ['yes', 'no']:

        print('\nSorry, not a valid answer, retry\n')
        more_info_start_end = input('Do you wish to visualize a graph with the top 10 start-end station combos? (yes o no):\n').lower()


    if more_info_start_end == 'yes':
        print('\nprinting graph...\n')
        most_common_start_end_df = df.groupby(['Start - End Stations'])['Start Time'].count().sort_values(ascending=False)[:10]

        plt.rcParams.update({'figure.autolayout': True})


        fig, ax = plt.subplots(1, 1, figsize=(10, 7))
        ax.barh(list(most_common_start_end_df.index), list(most_common_start_end_df.values))
        labels = ax.get_xticklabels()
        ax.set(xlim=[most_common_start_end_df.values.min(), most_common_start_end_df.values.max()+5], xlabel='Total Rides', ylabel='Start - End Stations', title='Top 10 Start - End Combinations')
        plt.show()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(city, month, day, df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTRIP DURATION GENERAL STATS\n')


    travel_time = round(df['Trip Duration (mins)'].sum(), 2)
    print('The total travel time is {} minutes'.format(travel_time))

    mode_travel_time = round(df['Trip Duration (mins)'].mode()[0], 0)
    print('The most common travel time is {} minutes'.format(mode_travel_time))

    # display mean travel time
    mean_travel_time = round(df['Trip Duration (mins)'].mean(), 2)
    print('The mean travel time is {} minutes'.format(mean_travel_time))

    # display median travel time
    median_travel_time = round(df['Trip Duration (mins)'].median(), 2)
    print('The median travel time is {} minutes'.format(median_travel_time))

    # display standard deviation of travel time
    std_dev_travel_time = round(df['Trip Duration (mins)'].std(), 2)
    print('The standard deviation of travel time is {} minutes'.format(std_dev_travel_time))

    more_info_travel_time = input('\nDo you wish to see a histogram with travel time distributions? (yes or no):\n')
    while more_info_travel_time not in ['yes' , 'no']:
        print('\nOops thats not a valid answer! retry please\n')
        more_info_travel_time = input('Do you wish to see a histogram with travel time distributions? (yes or no):\n')

    #Display histogram of travel time
    if more_info_travel_time == 'yes':
        print('\nprinting graph...\n')

        x = df['Trip Duration (mins)']
        x_low_lim = 0
        x_upp_lim = median_travel_time + std_dev_travel_time

        fig, ax = plt.subplots(1, 1, figsize=(10, 7))
        ax.hist(x, bins = range(int(x_low_lim), int(x_upp_lim)))
        ax.minorticks_on()
        ax.grid()
        ax.set(xlim=[x_low_lim, x_upp_lim], xlabel='Travel Time (minutes)', ylabel='Total Trips', title='Trip Duration Distribution')
        plt.show()

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)





def user_stats(city, month, day, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('\nTRIPS BY USER TYPE\n')
    user_type_count = df.groupby(['User Type'])['Start Time'].count()
    print(user_type_count)

    # Display counts of gender unless city is washington
    if city != 'washington':

        print('\nTRIPS BY GENDER\n')
        user_gender_count = df.groupby(['Gender'])['Start Time'].count()
        print(user_gender_count)

    more_info_user = input('\n Do you want see this data in a pie chart? (yes or no):\n').lower()
    while more_info_user not in ['yes', 'no']:
        print('\nOops not a valid answer! please retry\n')
        more_info_user = input('Do you want see this data in a pie chart? (yes or no):\n').lower()

    if more_info_user == "yes":
        if city != 'washington':
            print('\nprinting graph...\n')
            fig1, axs1 = plt.subplots(2, 1, figsize=(7, 8))
            axs1[0].pie(user_gender_count, labels= ['Female', 'Male'] , autopct='%1.1f%%',
                        shadow=True, startangle=90)
            axs1[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            axs1[1].pie(user_type_count, labels= list(user_type_count.index), autopct='%1.1f%%',
                        shadow=True, startangle=90)
            axs1[0].set_title('Trips by Gender')
            axs1[1].set_title('Trips by User Type')
            plt.show()

        else:
            print('\nprinting graph...\n')
            plt.pie(user_type_count, labels= list(user_type_count.index), autopct='%1.1f%%',
                        shadow=True, startangle=90)
            plt.title('Trips by User Type')
            plt.show()

    #Display usage by age and plot unless city is washington
    if city != 'washington':
        print('\nTRIPS BY AGE\n')
        usage_by_age = df.groupby(['Age'])['Start Time'].count()
        print(usage_by_age.head())

        more_info_age = input('\n Do you want see this total trips by age? (yes or no):\n').lower()
        while more_info_age not in ['yes', 'no']:
            print('\nOops not a valid answer! please retry\n')
            more_info_age = input('Do you want see this total trips by age? (yes or no):\n').lower()

        if more_info_age == 'yes':
            max_age = usage_by_age.index[list(usage_by_age.values).index(usage_by_age.max())]

            fig2, ax2 = plt.subplots(1, 1, figsize=(10, 7))
            ax2.plot(usage_by_age, linewidth=2.0)
            labels = ax2.get_xticklabels()
            ax2.set(xlim=[10, 90], ylim = [0, usage_by_age.max()+1000], xlabel='Age (rounded down)',
                    ylabel='Total Trips', title='Trips By Age')
            ax2.annotate('MAX: AGE ({})'.format(int(max_age)), xy=(max_age, usage_by_age.max()), xytext=(max_age + 20, usage_by_age.max()+5),
                         arrowprops=dict(facecolor='black', shrink=0.05),
                         )

            ax2.grid(True)
            plt.show()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def choose_visualization(city, month, day):

    """Creates a menu to choose type of stats to analyze"""

    print('\nCURRENT FILTER:\nCity : {}\nMonth: {}\nDay: {}\n'.format(city, month, day))

    while True:
        try:
            choose = int(input('What Analysis do you wish to visualize? (Enter options 1-7) \n1. Time Stats\n2. Station Stats\n3. Trip Duration Stats\n4. User Data\n5. Back to Filter\n6. Quit:\n'))
            break
        except ValueError:
            print('\nOops! Thats not a valid option. Retry\n')

    return choose

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        choose = choose_visualization(city, month, day)
        while choose != 6 or choose != 5:
            if choose == 1:
                time_stats(city, month, day, df)
                choose = choose_visualization(city, month, day)
            elif choose == 2:
                station_stats(city, month, day, df)
                choose = choose_visualization(city, month, day)
            elif choose == 3:
                trip_duration_stats(city, month, day, df)
                choose = choose_visualization(city, month, day)
            elif choose == 4:
                user_stats(city, month, day, df)
                choose = choose_visualization(city, month, day)
            elif choose == 5:
                main()
            elif choose == 6:
                exit()
            else:
                print('\nOops! Thats not a valid option. Retry\n')
                choose = choose_visualization(city, month, day)
        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
