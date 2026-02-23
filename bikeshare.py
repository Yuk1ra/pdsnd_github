import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    # city
    while True:
        city = input("Choose city (chicago, new york city, washington): ").strip().lower()
        if city in valid_cities:
            break
        print("Invalid city. Try again.")

    # month
    while True:
        month = input("Choose month (all, january–june): ").strip().lower()
        if month in valid_months:
            break
        print("Invalid month. Try again.")

    # day
    while True:
        day = input("Choose day (all, monday–sunday): ").strip().lower()
        if day in valid_days:
            break
        print("Invalid day. Try again.")

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

    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    # Convert column 
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all':
        month_num = ['january','february','march','april','may','june'].index(month) + 1
        df = df[df['month'] == month_num]

    # Filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    if df.empty:
        print("No data available for the selected filters.")
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Most Common Month:", df['month'].mode()[0])
    print("Most Common Day of Week:", df['day_of_week'].mode()[0])
    print("Most Common Start Hour:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    if df.empty:
        print("No data available for the selected filters.")
        return

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("Most Common Start Station:", df['Start Station'].mode()[0])
    print("Most Common End Station:", df['End Station'].mode()[0])

    # most frequent trip
    trip_combo = df['Start Station'] + " -> " + df['End Station']
    print("Most Frequent Trip:", trip_combo.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    if df.empty:
        print("No data available for the selected filters.")
        return

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total Travel Time:", df['Trip Duration'].sum())
    print("Mean Travel Time:", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    if df.empty:
        print("No data available for the selected filters.")
        return
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # user types
    print("User Types:\n", df['User Type'].value_counts())

    # gender (if exists)
    if 'Gender' in df.columns:
        print("\nGender Counts:\n", df['Gender'].value_counts())
    else:
        print("\nGender data not available for this city.")

    # birth year (if exists)
    if 'Birth Year' in df.columns:
        print("\nEarliest Birth Year:", int(df['Birth Year'].min()))
        print("Most Recent Birth Year:", int(df['Birth Year'].max()))
        print("Most Common Birth Year:", int(df['Birth Year'].mode()[0]))
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Displays raw data 5 rows at a time upon user request.
    Continues until user enters 'no' or data runs out.
    """

    if df.empty:
        print("No data available to display.\n")
        return

    pd.set_option('display.max_columns', 200)

    i = 0
    total_rows = len(df)

    while True:
        raw = input("\nWould you like to see 5 rows of raw data? (yes/no): ").strip().lower()

        if raw == 'no':
            break

        elif raw == 'yes':
            if i >= total_rows:
                print("\nNo more data to display.")
                break

            print(df.iloc[i:i+5])
            i += 5

        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

# Edit 3
