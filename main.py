import pandas as pd

# save link and load it like dataframe to 'bookings'.
link = 'https://stepik.org/media/attachments/lesson/360344/bookings.csv'
bookings = pd.read_csv(link, sep=';')


# print first 7 bookings and then take a look at columns.
print('\nPrint first 7 bookings and then take a look at columns\n')
print(bookings[:7])
print(bookings.columns)


# function that make columns look better for Python, its deleting spaces and make words lower.
def rename_func(df: pd.DataFrame):
    for i in df.columns:
        a = str(i).lower()
        if ' ' in a:
            a = a.replace(' ', '_')
        df = df.rename(columns={str(i): a})
    return df


# renaming dataframe columns with new function and checking it.
bookings = rename_func(bookings)
print('\nRenaming dataframe columns with new function and checking it\n')
print(bookings.head())
print(bookings.columns)


# create success_country - all uncanceled bookings and make it unique
success_country = bookings[bookings.is_canceled == 0]
success_country = success_country['country'].value_counts()

# print 5 highest cities by success bookings and sum
print('\nPrint 5 highest cities by success bookings and sum\n')
print(success_country.head())
print(success_country.head().sum())


# make df with mean of bookings for different types of hotel
mean_nights_by_hotel = bookings.groupby('hotel', as_index=False) \
                               .aggregate({'stays_total_nights': 'mean'}) \
                               .sort_values('stays_total_nights', ascending=False)

print('\nMake df with all bookings for different types of hotel\n')
print(mean_nights_by_hotel)


# 2 types of grouping by overbooking - assigned_room_type != reserved_room_type
# query and syntax
print('\nGrouping by overbooking - assigned_room_type != reserved_room_type and sum of overbooking\n')
# overbooking = bookings.query("assigned_room_type != reserved_room_type").head()
overbooking = bookings[bookings.assigned_room_type != bookings.reserved_room_type]
print(overbooking.head())
print('sum =', len(overbooking))


# What month is most successful in 2016 and 2017
month_2016 = bookings.query("is_canceled == 0 and arrival_date_year == 2016")\
                     .value_counts('arrival_date_month')
month_2017 = bookings.query("is_canceled == 0 and arrival_date_year == 2017")\
                     .value_counts('arrival_date_month')

print('\nWhat month is most successful in 2016 and 2017\n')
print(month_2016.head(), '\n')
print(month_2017.head())


# most canceled bookings by years by months
year_group = bookings.query("is_canceled == 1 and hotel == 'City Hotel'")\
                     .groupby('arrival_date_year', as_index=False)['arrival_date_month']\
                     .value_counts('arrival_date_month')

print('\nMost canceled bookings by years by months\n')
print(year_group)


# mean of types of people
people_count = bookings[['adults', 'children', 'babies']].mean()
print('\nMean of types of people\n')
print(people_count)


# new column 'total_kids' and sorting df by hotel type, then mean of total kids for each type
bookings['total_kids'] = bookings.children + bookings.babies
df_total_kids_group = bookings.groupby('hotel', as_index=False)\
                              .aggregate({'total_kids': 'mean'})\
                              .sort_values('total_kids', ascending=False).round(2)

print("\nNew column 'total_kids' and sorting df by hotel type, then mean of total kids for each type\n")
print(df_total_kids_group)


# churn rate. cancelled with kids and cancelled without kids
bookings['has_kids'] = bookings.total_kids > 0
print("\nChurn rate. Cancelled with kids and cancelled without kids\n")

percent_cancel_with_kids = bookings.query("has_kids == True and is_canceled == 1").shape[0]
percent_cancel_without_kids = bookings.query("has_kids == False and is_canceled == 1").shape[0]

total_kids_group_count = bookings.query("has_kids == True").shape[0]
total_without_kids_group_count = bookings.query("has_kids == False").shape[0]

percent_cancel_with_kids = percent_cancel_with_kids/(total_kids_group_count/100)
percent_cancel_without_kids = percent_cancel_without_kids/(total_without_kids_group_count/100)

print('canceled with kids is', percent_cancel_with_kids, '%')
print('canceled without kids is', percent_cancel_without_kids, '%')
