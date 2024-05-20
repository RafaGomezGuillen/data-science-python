# Pandas

## Import pandas.

```py
import pandas as pd
```

## Read a file.

`df = pd.read_...("file")`

```py
data_frame = pd.read_csv("data.csv")
```

## Creating data frames from NumPy series

```py
my_dict = {'col1': pd.Series([1, 2, 3, 4]),
           'col2': pd.Series([4, 3, 2, 1])}

data_frame = pd.DataFrame(my_dict)
```

## Show the top, random and bottom rows

```py
data_frame.head(10) # top 10 rows. by default 5 rows .head()
data_frame.tail(10) # bottom 10 rows. by default 5 rows .tail()
data_frame.sample() # random
```

## Information of the data frame

```py
data_frame.info()
```

## Describe (count, mean, std, min, 25%, 50%, 75%, max)

```py
data_frame.describe()
```

## Acceding an especific index or various indexes

```py
data_frame.loc[123, "Duration"] # Acceding the 123 index of the column Duration

data_frame.loc[[89, 125, 111, 3, 156]] # Acceding multiple indexes

# Size column to "0" where is equal to "Varies with device"
data_frame.loc[data_frame["Size"] == "Varies with device", "Size"] = "0"
```

## Where (loc)

`df.loc[(CONDITIONS FOR INDEX), (COLUMNS)]`

```py
data_frame.loc[data_frame["Maxpulse"] == 182]

data_frame.loc[
  (data_frame["Duration"] == 60) &
  (data_frame["Calories"] == 479)
]

data_frame.loc[data_frame["Legendary"] == True, "Type 1"].value_counts() # Counting Type 1 column when pokemons are legendary

# isin(array)
data_frame.loc[data_frame['Age'].isin([41, 42, 43, 44]), ["Age"]].value_counts() # Counting values where age is in [41, 42, 43, 44]
```

## Where (where)

`df.where(dataset['Age'] == 41)`

```py
data_frame["Age"].where(data_frame["Age"].isin([41, 42, 43, 44])).value_counts()
```

## Where (iloc)

`df.iloc[index, [columns]]`

```py
data_frame.iloc[0, [0, 1, 2]] # At index 0 shows column 0, 1 and 2
```

## Slicing

```py
data_frame.loc[1:3] # Showing rows among 1 and 3
data_frame.loc[3:] # Showing rows starting at 3 to the end
data_frame.loc[:3] # Showing rows starting at 3 to the beginning
```

## Sorting values

```py
data_frame.sort_values(by = ["Maxpulse"], ascending = False).head(10) # head shows the top 10 values

data_frame.sort_values(by = ["Defense", "Attack"], ascending = [False, True]).head(1)  # Order by Defense and attack but Defense in ascending mode and Attack not

# Sorting by Attack when generation is lower than 3 and Type 1 column is equal to Water or Fire
data_frame.sort_values(by = "Attack", ascending = False).loc[
  (data_frame["Generation"] < 3) &
  (data_frame["Type 1"].isin(["Water", "Fire"]))].head(2)
```

## Queries

```py
data_frame.query("Attack > 150").head(3)
data_frame.query('City == "Dallas" and Age == 41')
data_frame.query('Age in (41, 42)')
data_frame.query('index < 3') # index is a reserved word

city = "Dallas"

data_frame.query(f'City == "{city}"')
```

## Delete columns

```py
del data_frame["Generation"]
```

## Insert columns

```py
data_frame.insert(0, 'name_column', pd.Series(np.random.randint(0, 20, 4))) # insert(index, column, values)
```

## Max / min of an column or the entire data frame. Missing data

```py
data_frame["Calories"].max()

data_frame.loc[data_frame["Duration"] == 60].min()

data_frame.isna().sum() 
```

## Playing with string methods

```py
data_frame["Price"] = data_frame["Price"].str.replace("$", "")
```

## Common values and average values

```py
# common values
data_frame["Calories"].mode()

average = (data_frame["home_goals"] + data_frame["away_goals"]).mean()
```

## Counting values

```py
# normalize = True. Shows porcentage
# dropna = True. Remove nan values
data_frame["Calories"].value_counts().head(10) # counting the top 10 values of the calories column

# it is the same method
(data_frame["Sp. Def"] <= 25).sum()
(data_frame["Sp. Def"] <= 25).value_counts()

(
  (data_frame["Type 1"] == "Fire") |
  (data_frame["Type 2"] == "Flying")
).sum()

data_frame.isna().sum() # counting NaN values
```

## Cut values

```py
pd.cut(data_frame["bedrooms"], bins = [-1, 3, 8, 10], labels = ["lower than 3", "beween 3 and 8", "greater than 10"])

price_grp = pd.qcut(data_frame['price'], q = 5, labels = np.arange(5))
```

## Per cent of a column

```py
bottom_5 = data_frame["Speed"].quantile(.05) # 5%
top_5 = data_frame["Speed"].quantile(.95) # 95%

data_frame.loc[(data_frame["Speed"] > top_5) | (data_frame["Speed"] < bottom_5)]
```

## Convert a column to...

```py
data_frame["Installs"] = pd.to_numeric(data_frame["Installs"])

data_frame["abbrev"] = data_frame["abbrev"].astype(str) # Covert a column to str

data_frame.loc[data_frame["Size"].str.contains("k"), "Size"] = (
  pd.to_numeric(
  data_frame.loc[data_frame["Size"].str.contains("k"), "Size"].str.replace("k", "")
) * 1024).astype(str)
```

## Duplicated values

```py
data_frame.loc[
  (data_frame.duplicated(subset = ["App"], keep = False)) &
  (~data_frame.duplicated(keep = False)) # Duplicated by App column but different in other columns
].sort_values(by = "App", ascending = True)

# Drop duplicated values by keeping ones with the greatest number of...
# subset: column
# keep: determine the column to keep
# inplace: if true modify de data frame instead of creating a new one
data_frame.drop_duplicates(subset=["App"], keep="last", inplace=True)
```

## Create a new data frame by other

```py
water_flying_df = data_frame.loc[
  (data_frame["Type 1"] == "Water") &
  (data_frame["Type 2"] == "Flying")]


# creating a data frame selecting the columns
legendary_fire_df = data_frame.loc[
    (data_frame["Type 1"] == "Fire") & (data_frame["Legendary"] == True),
    ["Name", "Attack", "Generation"] # column selection
  ]

data_frame = df[["Name", "Pos", "Age", "Collage", "Birthdate"]]

# My way
data_frame["Distribution"] = "Free"
data_frame.loc[data_frame["Price"] != 0, "Distribution"] = "Paid"

# Good way
data_frame["Distribution"] = data_frame["Price"].apply(lambda p: "Free" if p > 0 else "Paid")
```

## Groupby, Aggregations and Join / Merge data

```py
# What is the team with most away wins?
# Way 1
data_frame.loc[data_frame["result"] == "A"].groupby("away_team")["result"].size().sort_values(ascending=False).head(1)
# Way 2
data_frame.groupby("away_team").apply(lambda rows: (rows["result"] == "A").sum()).sort_values(ascending=False).head(1)

# What is the team with the most goals scored at home?
data_frame.groupby("home_team")["home_goals"].sum().sort_values(ascending=False).head(1)

# What is the team that recieved the least amount of goals while playing at home?
data_frame.groupby("home_team")["away_goals"].sum().sort_values().head(1)

# What is the team with most goals scored playing as a visitor?
data_frame.groupby("away_team")["away_goals"].sum().sort_values(ascending=False).head(1)

# By condition and waterfront calcule the mean price of it
df = data_frame.groupby(['condition', 'waterfront'])['price'].mean().round(2)
df = df.to_frame()

data_frame.where(data_frame['price'] > 0).groupby('condition').agg({
    'price' : ['min', 'max']
})

# ---------------------------------------------------------
df1 = data_frame.loc[0:10, ['city', 'price', 'bedrooms']]
df2 = data_frame.loc[0:10, ['city', 'statezip', 'country']]

# Join by column. In this case by the column 'city'
df = df1.merge(df2, how = 'left', left_on = 'city', right_on = 'city')
# Join by row. We apply a suffix to the 'city' column
df = df1.join(df2, lsuffix = '_x', rsuffix = '_y')
```

### Aggregations
```py
# Gropy by condition and calclule to price the mean, to bathrooms the median, etc...
data_frame.groupby('condition').agg({
    'price' : 'mean',
    'bathrooms' : 'median',
    'waterfront' : 'max',
    'floors' : 'min'
})
```

## Random sample of a data frame

```py
# this would be the 15% of the data frame
random_sample = data_frame.sample(frac = 0.15)
```

## MultiIndex

```py
tuples = [('unimportant_columns', 'Number'),
          ('important_columns', 'City'),
          ('unimportant_columns', 'Gender'),
          ('important_columns', 'Age'),
          ('important_columns', 'Income'),
          ('unimportant_columns', 'Illness')
         ]

multi_index = pd.MultiIndex.from_tuples(tuples)

data_frame.columns = multi_index

# unimportant_columns | important_columns |unimportant_columns | important_columns | unimportant_columns
# Number | City | Gender | Age | Income | Illness

data_frame["important_columns"] # Watching City, Age and Income
data_frame["important_columns"]["City"] # Check City

data_frame.columns.levels # Check levels
```

### Order columns by index (Preferably in dataframes with multi index)

```py
# inplace = True. Modify the data frame
data_frame.sort_index(level = 0, axis = 1, inplace = True)
```

### The transpose of the DataFrame

```py
data_frame.head().T
```

## Timeseries and Timestamp

`pd.Timestamp(year, month, day)`

`pd.Timestamp('year-month-day')`

`pd.date_range('2020-01-01', periods=5, freq='D')`

```py
# The "Timestamp" data type is the most basic type associated with time series. Its constructor allows us several inputs
time_stamp = pd.Timestamp(2020, 1, 1)
time_stamp = pd.Timestamp('2020-01-01')

# We can create a time series by adding several timestamps
# dayfirst = True. Set date format to day/month/year
date_time = pd.to_datetime(['01/01/2020', np.datetime64('2020-01-02'), datetime.datetime(2020, 1, 3)], dayfirst = True)

# We can also create time intervals
# freq parameter: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
# D: Day
# M: Month
# Y: Yea
# W: Week
# H: Hours
date_time_int = pd.date_range('2020-01-01', periods = 5, freq = 'D')
date_time_int = pd.date_range(start = '2020-01-01', end = '2020-01-10', freq = 'D')

week_mask = "Mon Tue Wed"
date_time_int = pd.bdate_range('2020-01-01', '2020-01-30', freq = 'C', weekmask = week_mask)

date_time_int.isocalendar() # Display columns as: Year | Week | Day

# Display dates
date_time_int.dt.year
date_time_int.dt.month
date_time_int.dt.day
date_time_int.dt.hour
date_time_int.dt.dayofyear
date_time_int.dt.dayofweek
date_time_int.dt.day_name()
```

## Missing data (NaN)

```py
data_frame.isna().sum() # Count missing data
data_frame['bedrooms'].fillna(value = 0, inplace = True) # Fill NaN data with value 0 and modifying data frame
# axis = 'columns'. Drop NaN data from columns
data_frame.dropna(axis = 'index', how = 'any', inplace = True) # Drop NaN data from rows
```

## Data frame Union

```py
df1 = data_frame.iloc[0:10] # first 10 rows
df2 = data_frame.iloc[-10:] # last 10 rows
df = pd.concat([df1, df2], axis = 'index', keys = ['head', 'tail'])


df1 = data_frame.loc[0:10, ['price', 'bedrooms']]
df2 = data_frame.loc[0:10, ['city', 'statezip', 'country']]
df = pd.concat([df1, df2], axis = 'columns', keys = ['head', 'tail'])
```

## Writing data frames to...

```py
data_frame_json.to_csv("dataset.csv")
data_frame_json.to_csv("dataset.csv", sep=",", header=False, index=False)
```
