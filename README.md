# Lazy Renter

## Overview
I am really lazy when it comes to looking for apartment. This repo goes into a project to make that process easier. At a high level I will automate pulling apartment ads from Craigslist and set up an alert when one meets my criteria (based on area, price, etc). By storing this data we can also start looking at prices over time, prices of different areas, etc. Yes, this data is sort of publicly available on other sites, but what fun is that? I also rarely see this using a combination of apartments and condos as Craigslist often is. Also, I have no idea on the timeframes they use. If I read "the average price of a NYC apartment is X" is that up to date? Is it for this year? Last year? It's 2019, we should have this in real time (until Craigslist blocks me for scraping too much)

Once we have this data there will be other cool stuff we can do - data exploration, prediction model to see how much we think an apartment is worth, etc. Another fun concept will be that not all apartments list how many Bedrooms so can we create an NLP model, based on the apartment title, to predict the number of bedrooms. 

## Data Pipeline
This is all within the data_pipeline folder of the repository. This pipeline is created using AWS Lambda. At a high level:

### Lambda Number 1
Once an hour it scrapes data from Craigslist and dumps the JSON to S3

### Lambda Number 2
Triggered by Lambda #1 it will take that data and enrich it with Mapquest data. This includes stuff like postal code, side of the street, distance to the nearest intersection, etc. Once this is done it dumps this enriched JSON to S3

### Lambda Number 3
Triggered by Lambda #2 dumping to S3. This will take that JSON and further enrich it with Walk Score data. For those unaware, Walk Score includes a Walk Score, Bike Score and Transit Score. Basically it tells you how easy it is to get around the city from an address. Once this JSON is enrich it is also dumped to S3.

What this pipeline ends up doing is once an hour we get some spiffy data on NYC apartments going to S3 automatically. We can then process it into Pandas fairly easy with Boto3. Huzzah for fully automated data pipelines without Cron, databases or any other painful data engineering - what a time to be alive!

## Notebooks
Now that our pipeline is pumping out data hourly, let's do some cool stuff with it!

### Data Cleaning
