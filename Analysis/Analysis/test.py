# this tab is used just to test some codes here.
# this tab does not interfare with the project
current_month = 6
day = 1
year = 2022
months = current_month + 1

for month in range(1, months):
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        day2 = 31
    else:
        day2 = 30

    if month == 2:
        day2 = 28

    if month == 2 and year % 4 == 0:
        day2 = 29

    start_day = f"{day}-{month}-{year}"
    end_day = f"{day2}-{month}-{year}"

    print(start_day, end_day)