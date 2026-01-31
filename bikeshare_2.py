# This project was made to compelete the course "Programming for Data Science with Python" on Udacity
import time
import pandas as pd
import numpy as np
import os

# Enable ANSI colors on Windows terminals
if os.name == 'nt':
    os.system('')

# ANSI Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Additional colors
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_CYAN = '\033[96m'

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def print_header(text):
    """Print a colorful header"""
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}{'='*60}{Colors.ENDC}\n")

def print_section(text):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_BLUE}▶ {text}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'─'*50}{Colors.ENDC}")

def print_stat(label, value, emoji="📊"):
    """Print a statistic with color"""
    print(f"{emoji} {Colors.BOLD}{Colors.YELLOW}{label}:{Colors.ENDC} {Colors.BRIGHT_GREEN}{value}{Colors.ENDC}")

def print_error(text):
    """Print an error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_success(text):
    """Print a success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) City - name of the city to analyze
        (str) Month - name of the month to filter by, or "all" to apply no month filter
        (str) Day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print_header("🚴 US BIKESHARE DATA EXPLORER 🚴")
    print(f"{Colors.BRIGHT_CYAN}Hello! Let's explore some US bikeshare data!{Colors.ENDC}\n")
    
    # get user input for city
    cities = ['chicago', 'new york city', 'washington']
    while True:
        print(f"{Colors.BOLD}{Colors.PURPLE}🏙️  Which city would you like to explore?{Colors.ENDC}")
        print(f"{Colors.CYAN}   Options: Chicago, New York City, Washington{Colors.ENDC}")
        city = input(f"{Colors.BRIGHT_YELLOW}➜ {Colors.ENDC}").lower()
        if city in cities:
            print_success(f"Selected: {city.title()}")
            break
        else:
            print_error('Invalid input! Please enter Chicago, New York City, or Washington.')

    # Ask user about filtering preference
    filter_options = ['month', 'day', 'both', 'none']
    while True:
        print(f"\n{Colors.BOLD}{Colors.PURPLE}🔍 Filter Options{Colors.ENDC}")
        print(f"{Colors.CYAN}   Would you like to filter the data by:{Colors.ENDC}")
        print(f"{Colors.CYAN}   • month  • day  • both  • none{Colors.ENDC}")
        filter_choice = input(f"{Colors.BRIGHT_YELLOW}➜ {Colors.ENDC}").lower()
        if filter_choice in filter_options:
            print_success(f"Filter mode: {filter_choice}")
            break
        else:
            print_error('Invalid input! Please enter month, day, both, or none.')

    # Initialize month and day
    month = 'all'
    day = 'all'

    # get user input for month if needed
    if filter_choice in ['month', 'both']:
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        while True:
            print(f"\n{Colors.BOLD}{Colors.PURPLE}📅 Month Selection{Colors.ENDC}")
            print(f"{Colors.CYAN}   Options: all, January, February, March, April, May, June{Colors.ENDC}")
            month = input(f"{Colors.BRIGHT_YELLOW}➜ {Colors.ENDC}").lower()
            if month in months:
                print_success(f"Selected month: {month.title()}")
                break
            else:
                print_error('Invalid input! Please enter a valid month or "all".')

    # get user input for day of week if needed
    if filter_choice in ['day', 'both']:
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while True:
            print(f"\n{Colors.BOLD}{Colors.PURPLE}📆 Day Selection{Colors.ENDC}")
            print(f"{Colors.CYAN}   Options: all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday{Colors.ENDC}")
            day = input(f"{Colors.BRIGHT_YELLOW}➜ {Colors.ENDC}").lower()
            if day in days:
                print_success(f"Selected day: {day.title()}")
                break
            else:
                print_error('Invalid input! Please enter a valid day or "all".')

    print(f"\n{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
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
    print(f"\n{Colors.BRIGHT_CYAN}⏳ Loading data for {city.title()}...{Colors.ENDC}")
    
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print_success(f"Data loaded successfully! {len(df)} trips found.")
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print_section('⏰ MOST FREQUENT TIMES OF TRAVEL')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print_stat('Most Common Month', months[popular_month - 1], '📅')

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print_stat('Most Common Day of Week', popular_day, '📆')

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print_stat('Most Common Start Hour', f'{popular_hour}:00 ({popular_hour % 12 or 12} {"PM" if popular_hour >= 12 else "AM"})', '🕐')

    print(f"\n{Colors.OKCYAN}⚡ Computed in {time.time() - start_time:.4f} seconds{Colors.ENDC}")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print_section('🚉 MOST POPULAR STATIONS AND TRIPS')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    start_station_count = df['Start Station'].value_counts()[popular_start_station]
    print_stat('Most Common Start Station', popular_start_station, '🚉')
    print(f"   {Colors.BRIGHT_CYAN}↳ Number of trips: {Colors.BRIGHT_GREEN}{start_station_count:,}{Colors.ENDC}")

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    end_station_count = df['End Station'].value_counts()[popular_end_station]
    print_stat('Most Common End Station', popular_end_station, '🏁')
    print(f"   {Colors.BRIGHT_CYAN}↳ Number of trips: {Colors.BRIGHT_GREEN}{end_station_count:,}{Colors.ENDC}")

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' → ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    trip_count = df['Trip'].value_counts()[popular_trip]
    print_stat('Most Common Trip', popular_trip, '🔁')
    print(f"   {Colors.BRIGHT_CYAN}↳ Number of trips: {Colors.BRIGHT_GREEN}{trip_count:,}{Colors.ENDC}")

    print(f"\n{Colors.OKCYAN}⚡ Computed in {time.time() - start_time:.4f} seconds{Colors.ENDC}")


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print_section('⏱️  TRIP DURATION STATISTICS')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    trip_count = len(df)
    # Convert to hours, minutes, seconds
    hours = int(total_travel_time // 3600)
    minutes = int((total_travel_time % 3600) // 60)
    seconds = int(total_travel_time % 60)
    print_stat('Total Travel Time', f'{hours:,} hours, {minutes} minutes, {seconds} seconds ({trip_count:,} trips)', '⏱️')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    minutes = int(mean_travel_time // 60)
    seconds = int(mean_travel_time % 60)
    print_stat('Average Travel Time', f'{minutes} minutes, {seconds} seconds', '⏰')

    print(f"\n{Colors.OKCYAN}⚡ Computed in {time.time() - start_time:.4f} seconds{Colors.ENDC}")


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print_section('👥 USER STATISTICS')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"\n{Colors.BOLD}{Colors.YELLOW}👤 User Types:{Colors.ENDC}")
    for user_type, count in user_types.items():
        print(f"   {Colors.BRIGHT_CYAN}• {user_type}:{Colors.ENDC} {Colors.BRIGHT_GREEN}{count:,}{Colors.ENDC}")

    # Display counts of gender (not available for Washington)
    if 'Gender' in df.columns:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚧ Gender Distribution:{Colors.ENDC}")
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            print(f"   {Colors.BRIGHT_CYAN}• {gender}:{Colors.ENDC} {Colors.BRIGHT_GREEN}{count:,}{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}⚠️  Gender data not available for this city.{Colors.ENDC}")

    # Display earliest, most recent, and most common year of birth (not available for Washington)
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\n{Colors.BOLD}{Colors.YELLOW}🎂 Birth Year Statistics:{Colors.ENDC}")
        print_stat('Earliest Birth Year', f'{earliest_year} (oldest user)', '👴')
        print_stat('Most Recent Birth Year', f'{most_recent_year} (youngest user)', '👶')
        print_stat('Most Common Birth Year', most_common_year, '📊')
    else:
        print(f"\n{Colors.WARNING}⚠️  Birth year data not available for this city.{Colors.ENDC}")

    print(f"\n{Colors.OKCYAN}⚡ Computed in {time.time() - start_time:.4f} seconds{Colors.ENDC}")


def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request, formatted as cards."""
    
    row_index = 0
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.PURPLE}📋 Would you like to view 5 rows of raw data?{Colors.ENDC}")
        print(f"{Colors.CYAN}   Enter 'yes' to view or 'no' to skip{Colors.ENDC}")
        view_data = input(f"{Colors.BRIGHT_YELLOW}➜ {Colors.ENDC}").lower()
        if view_data != 'yes':
            break
        
        # Display 5 rows as cards
        for i in range(row_index, min(row_index + 5, len(df))):
            print(f"\n{Colors.BRIGHT_CYAN}{'='*80}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.BRIGHT_GREEN}🚴 TRIP #{i + 1}{Colors.ENDC}")
            print(f"{Colors.BRIGHT_CYAN}{'='*80}{Colors.ENDC}")
            
            # Display each column and its value
            for column in df.columns:
                value = df.iloc[i][column]
                print(f"{Colors.YELLOW}{column:.<30}{Colors.ENDC} {Colors.BRIGHT_GREEN}{value}{Colors.ENDC}")
            
        row_index += 5
        
        # Check if we've reached the end of the dataframe
        if row_index >= len(df):
            print(f"\n{Colors.WARNING}📭 No more data to display.{Colors.ENDC}")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        print(f"\n{Colors.BOLD}{Colors.PURPLE}🔄 Would you like to restart?{Colors.ENDC}")
        print(f"{Colors.CYAN}   Enter 'yes' to analyze again or 'no' to exit{Colors.ENDC}")
        restart = input(f"{Colors.BRIGHT_YELLOW}➜ {Colors.ENDC}").lower()
        if restart != 'yes':
            print_header("👋 THANK YOU FOR USING BIKESHARE EXPLORER!")
            print(f"{Colors.BRIGHT_GREEN}Have a great day! 🚴‍♂️🚴‍♀️{Colors.ENDC}\n")
            break


if __name__ == "__main__":
	main()
