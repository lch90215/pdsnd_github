import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june','all']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). We use a while loop to handle invalid inputs
    while True:
            userinput1 = input("Enter a city name among these three options: 'New York City, Chicago, Washington' ")
            userinput1=userinput1.lower()
            if userinput1 in CITY_DATA.keys() and bool((type(userinput1) is str)) == True:
                city = str(userinput1)
                break
            else:
                print("Incorrect type. That's not an string or not from the list!")
    while True:
            userinput2 = input("Enter a month name from January till June(inclusive), or 'all' if you don't want filter via month: ")
            userinput2=userinput2.lower()
            if userinput2 in months and bool((type(userinput2) is str)) == True:
                month = str(userinput2)
                break
            else:
                print("Incorrect type. That's not an string or not from our list!")

    while True:
            userinput3 = input("Enter a date name or 'all' if you don't want filter via date: ")
            userinput3=userinput3.lower()
            if userinput3 in days and bool((type(userinput3) is str)) == True:
                day = str(userinput3)
                break
            else:
                print("Incorrect type. That's not an string or proper date name!")
    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month']==month]

    if day != 'all':
        df = df[df['day_of_week']==day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    monthnumber=df['month'].mode()[0]
    monthname = months[monthnumber-1].title()
    # TO DO: display the most common month
    print("\nThe most common month is: {}" .format(monthname))
    # TO DO: display the most common day of week
    print("\nThe most common day is:{}" .format(df['day_of_week'].mode()[0]))
    # TO DO: display the most common start hour
    print("\nThe most common hour is:{}:00" .format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print("\nThe most commonly used start station is: {}" .format(df['Start Station'].mode()[0]))
    print("\nThe most commonly used end station is: {}" .format(df['End Station'].mode()[0]))
    # TO DO: display most frequent combination of start station and end station trip
    df2= df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print("\nThe most frequent station combination is:{}" .format(df2.index[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    df3=df['Trip Duration'].sum()
    totaltime=int(df3/60)
    print("\nThe total travel time of this period is {} minutes.".format(totaltime))

    # TO DO: display mean travel time
    df4=df['Trip Duration'].mean()
    avgtime=int(df4/60)
    print("\nThe average travel time of this period is {} minutes.".format(avgtime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    # TO DO: Display counts of user types
    print("\nThis is the user type statistics:\n{}".format(user_types))

    # TO DO: Display counts of gender
    user_gender = df['Gender'].value_counts()
    print("\nThis is the user gender statistics:\n{}".format(user_gender))
    # TO DO: Display earliest, most recent, and most common year of birth
    df5=int(df['Birth Year'].max())
    df6=int(df['Birth Year'].min())
    df7=int(df['Birth Year'].mode())
    print("\nThe earliest year of birth for this group of users is year {},\nthe most recent year of birth for this group of users is year {},\nthe most common year of birth for this group of users is year {}.".format(df6,df5,df7))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_age_duration_correlation(df):
    """showe each bike user's age, with subscriber data only, since we don't have regular customer's personal info """
    df=df.dropna(axis=0)
    df['User Age']=2020-df['Birth Year']
    df=df.drop(columns=['Start Time', 'End Time','Start Station','End Station','User Type','Gender','month','hour','Birth Year','Unnamed: 0'])
    print('\nBelow is the correlation between user age and bike ride duration:\n')
    print(df.corr())


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        raw=input('\nWould you like to start descriptive analysis section?pls type yes or no\n').lower()

        time_stats(df)
        if raw=='no':
            break
        raw=input('\nWould you like to see next descriptive analysis section?pls type yes or no\n').lower()

        station_stats(df)
        if raw=='no':
            break
        raw=input('\nWould you like to see next descriptive analysis section?pls type yes or no\n').lower()

        trip_duration_stats(df)
        if raw=='no':
            break
        raw=input('\nWould you like to see next descriptive analysis section?pls type yes or no\n').lower()

        user_stats(df)
        if raw=='no':
            break
        raw=input('\nWould you like to see next descriptive analysis section?pls type yes or no\n').lower()

        user_age_duration_correlation(df)
        if raw=='no':
            break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
