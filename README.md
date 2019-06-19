# Lazy Renter

## Overview
I am really lazy when it comes to looking for apartment. This repo goes into a project to make that process easier. At a high level I will automate pulling apartment ads from Craigslist and set up an alert when one meets my criteria (based on area, price, etc). By storing this data we can also start looking at prices over time, prices of different areas, etc. Yes, this data is sort of publicly available on other sites, but what fun is that? I also rarely see this using a combination of apartments and condos as Craigslist often is.

For fun, let's also see if we can accurately predict the rent of an apartment. The first step of this will be building out a data pipeline that regularly (Cron) pulls data from Craigslist and stores it in S3. Once it is in S3 we can do some exploratory analysis and then see if we can build a model that accurately predicts the price of a rental (vs. what the person actually lists it at)

## Sections
