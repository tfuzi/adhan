from hijri_converter import convert
import datetime

# Convert a specific date from Gregorian to Hijri
date_now = datetime.datetime.now()
hijri_date = convert.Gregorian(
    day=date_now.day,
    month=date_now.month,
    year=date_now.year
).to_hijri()


# Extract the month and day from the Hijri date
hijri_year = hijri_date.year
hijri_month = hijri_date.month
hijri_day = hijri_date.day


# Get the Hijri month name
hijri_month_name = hijri_date.month_name()

# Format the Hijri date
hijri_date_formatted = f"{hijri_month_name} {hijri_day}, {hijri_year} AH"
