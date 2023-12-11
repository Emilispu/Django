import pandas as pd
import requests
from sktime.forecasting.compose import make_reduction
from sktime.forecasting.model_selection import temporal_train_test_split

# Eurostat API Fixed part parameters
base_url = "https://ec.europa.eu/eurostat/api/dissemination"
service = "statistics"
version = "1.0"
response_type = "data"

# Eurostat API Dynamic part parameters

datasetCode = "hlth_hlye"
format = "format=JSON"
lang = "lang=EN"

# Eurostat API Dynamic parts filter parameters
filters = ""
time = [
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2015",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
]
unit = "YR"
geo = ["DE"]
# geo= ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE', 'IS', 'NO', 'CH']
indic_he = ["HLY_0", "LE_0", "HLY_50", "LE_50", "HLY_65", "LE_65"]
sex = "T"
lang = "en"
filters = f"indic_he='LE_0'&unit={unit}&sex={sex}&lang={lang}"
for el in geo:
    filters += f"&geo={el}"
for el in time:
    filters += f"&time={el}"

# Constructing the API query URL
url = f"{base_url}/{service}/{version}/{response_type}/{datasetCode}?{format}&{filters}"

# Making the API request
response = requests.get(url)
print(url)

if response.status_code == 200:
    data = response.json()
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

# Get info from dataset.

values = data["value"]
countries = data["dimension"]["geo"]["category"]["label"]
date_year = data["dimension"]["time"]["category"]["label"]

# Create DataFrame
column_name = list(countries)
row_name = list(date_year)
df = pd.DataFrame(index=pd.to_datetime(row_name, format="%Y"), columns=column_name)
for i, row in enumerate(row_name):
    for j, col in enumerate(column_name):
        x = str(i * len(column_name) + j)
        if x in list(values):
            df.at[row, col] = values[x]
            part = values[x]
        else:
            df.at[row, col] = part

# Make plot Table with data

df = df.astype(float)

df.index = df.index.to_period("A")

y_train, y_test = temporal_train_test_split(df, test_size=8)

from sktime.forecasting.base import ForecastingHorizon

fh = ForecastingHorizon(y_test.index, is_relative=False)

window_length = len(y_train) // 2

from sklearn.linear_model import LinearRegression

regressor = LinearRegression()


forecaster = make_reduction(
    regressor, window_length=window_length, strategy="recursive"
)
forecaster.fit(y_train)

y_pred = forecaster.predict(fh)

from sktime.performance_metrics.forecasting import mean_absolute_percentage_error

print(mean_absolute_percentage_error(y_test, y_pred))
