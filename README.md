# Population_data

## Description

The goal of this lab is to predict the urban population growth. It is modelled with a simple linear regression `population = a * year + b`, where a and b are respectively the slope and the intersect.

## Requirements

The database `mondial.db` can be downloaded here [here](https://github.com/seralf/mondial_sqlite/blob/master/db/mondial.db). It is gitignored in this project because of it's large size, but it is placed at the root of the project.

`Python 3.8.10` is required, might work on previous versions, but hasn't been tested.

Additional requirements:

- sqlite3
- matplotlib
- tkinter (because of `matplotlib.use('TkAgg')`, not necessary if not run in a virtual environment)
- numpy
- sklearn
- scipy

## How to use

```bash
git clone https://github.com/elisakaisa/population_data.git
python3 main.py
```

First create a view from the database, by running the following in the terminal:

```bash
sqlite3 mondial.db
.header on
.mode column

CREATE VIEW PopData AS SELECT year, city as name, citypops.population, citypops.country, longitude, latitude, elevation, agriculture, industry, inflation FROM (CityPops, City) NATURAL JOIN Economy WHERE city = name AND City.Country = CityPops.Country;
```

To verify that the view has been properly created, run the following query.

```bash
SELECT * FROM PopData limit 10;
```

It should return

```bash
Year        name        Population  Country     Longitude   Latitude    Elevation   Agriculture  Industry    Inflation 
----------  ----------  ----------  ----------  ----------  ----------  ----------  -----------  ----------  ----------
1987        Tirana      192000      AL          19.82       41.33       110         19.5         12          1.7       
1990        Tirana      244153      AL          19.82       41.33       110         19.5         12          1.7       
2011        Tirana      418495      AL          19.82       41.33       110         19.5         12          1.7       
1987        Shkodër     62000       AL          19.5        42.07       13          19.5         12          1.7       
2011        Shkodër     77075       AL          19.5        42.07       13          19.5         12          1.7       
1979        Durrës      66200       AL          19.45       41.32       0           19.5         12          1.7       
1989        Durrës      82719       AL          19.45       41.32       0           19.5         12          1.7       
2001        Durrës      99546       AL          19.45       41.32       0           19.5         12          1.7       
2011        Durrës      113249      AL          19.45       41.32       0           19.5         12          1.7       
1987        Vlorë       56000       AL          19.49       40.47       25          19.5         12          1.7 
```

## Credits

The [initial code](https://github.com/elisakaisa/population_data/tree/066d561cc6a14485a4c364e644e6884727e760bf) was provided by Florian Pokorny in the scope of the course DD1334 at KTH in 2022.
