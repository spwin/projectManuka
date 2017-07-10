# Project Manuka

This Python3.5 code collect the data starting from 2010-01-01 from **https://www.investing.com/economic-calendar** 
and stores the data in sqlite3 database. <br/><br/>
All the cookies and headers are already set and ready to use. Each script run iterates over the `last_parsed` date through `last_parsed + 1 month` for each day
### Runnign the script
To run the script just execute:
```
python3.5 start.py
```
The script will create database file `economic_calendar.db` in your project root directory.

#### Database
Structure of the database:
```
`id`            # DB record id
`event_id`      # investing.com local id
`actual`        # Table row 'Actual' value
`actual_title`  # Worse or Better than expected
`previous`      # Table row 'Previous' value
`previous_title`# Worse or Better than expected 
`currency`      # Currency symbol
`importance`    # Event importance
`forecast`      # Event forecast
`country`       # Country
`event`         # Event name
`time`          # Event time
`updated_at`    # Time when it was parsed
```
