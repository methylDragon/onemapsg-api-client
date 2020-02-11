# OneMap API Client

[![PyPI version](https://badge.fury.io/py/onemapsg.svg)](https://badge.fury.io/py/onemapsg)

Python Wrapper Client for the OneMap API

![img](assets/logo.png)



Docs here: https://docs.onemap.sg/

PyPI Link: <https://pypi.org/project/onemapsg/>

Register for an API key here: https://developers.onemap.sg/signup/



This client:

- Authenticates for a valid API token, and refreshes as needed!
- Returns everything as a nice dictionary!



## Example Usage

```python
from onemapsg import OneMapClient

Client = OneMapClient("YOUR_EMAIL", "YOUR_PASSWORD")

Client.search("Dragon View Park")
# Result
'''
{'found': 1,
 'totalNumPages': 1,
 'pageNum': 1,
 'results': [{'SEARCHVAL': 'DRAGON VIEW PARK',
   'BLK_NO': '',
   'ROAD_NAME': 'NIL',
   'BUILDING': 'DRAGON VIEW PARK',
   'ADDRESS': 'DRAGON VIEW PARK SINGAPORE',
   'POSTAL': 'NIL',
   'X': '27415.382888752',
   'Y': '31015.7030415982',
   'LATITUDE': '1.29676950856585',
   'LONGITUDE': '103.828065538017',
   'LONGTITUDE': '103.828065538017'}]}
'''
```



## Installation

```shell
pip install onemapsg
```



## Credits

- The OneMap team for a pretty nice API

- Author: methylDragon



## Support my efforts!

 [![Yeah! Buy the DRAGON a COFFEE!](./assets/COFFEE%20BUTTON%20%E3%83%BE(%C2%B0%E2%88%87%C2%B0%5E).png)](https://www.buymeacoffee.com/methylDragon)

[Or leave a tip! ヾ(°∇°*)](https://www.paypal.me/methylDragon)



## Client Interface

Includes the full API as of February 2019, also supports a general API query in case of client depreciation:

**Client Specific**

- Initialise Client

  - `Client = OneMapClient(email, password)`

    Generates token on init

- Generate New Token

  - `get_token(email=None, password=None)`

    *Returns:*

    token, expiry

- General Query

  - `query_api(endpoint, param_dict)`



## Class Methods

Remember to use them as such! `Client.method()`

**Location Search**

- Search
  - `search(search_val, return_geom=True, get_addr_details=True, page_num=1))`
- Reverse Geocode (SVY21 and WGS84)
  - `reverse_geocode_SVY21(coordinates, buffer=10, address_type="All", other_features=False)`
  - `reverse_geocode_WGS84(coordinates, buffer=10, address_type="All", other_features=False)`

**Coordinate Conversion**

- All converters between WGS84, SVY21, and 3857
  - `WGS84_to_EPSG(coordinates)`
  - `WGS84_to_SVY21(coordinates)`
  - `SVY21_to_EPSG(coordinates)`
  - `SVY21_to_WGS84(coordinates)`
  - `EPSG_to_SVY21(coordinates)`
  - `EPSG_to_WGS84(coordinates)`

**Themes**

- Check Theme Status
  - `check_theme_status(query_name, date_time)`
- Get Theme Info
  - `get_theme_info(query_name)`
- Get all Themes
  - `get_all_themes_info(more_info=False)`
- Retrieve Themes
  - `retrieve_theme(query_name, extents=None)`

**Planning Areas**

- Get all Planning Areas
  - `get_all_planning_areas(year=None)`
- Get Planning Area Names
  - `get_planning_area_names(year=None)`
- Get Planning Area Bounds
  - `get_planning_area_bounds(coordinates, year=None)`

**Population Queries**

- Economic Statuses
  - `get_economic_statuses(year, planning_area, gender=None)`
- Education Attendance
  - `get_education_attendance(year, planning_area)`
- Ethnic Groups
  - `get_ethnic_groups(year, planning_area, gender=None)`
- Work Income For Household (Monthly)
  - `get_household_monthly_work_income(year, planning_area)`
- Household Size Data
  - `get_household_sizes(year, planning_area)`
- Household Structure Data
  - `get_household_structures(year, planning_area)`
- Income from Work Data
  - `get_work_income(year, planning_area)`
- Population of Industries
  - `get_industries(year, planning_area)`
- Language Literacy Data
  - `get_language_literacy(year, planning_area)`
- Marital Status Data
  - `get_marital_statuses(year, planning_area, gender=None)`
- Mode of Transports to School Data
  - `get_modes_of_transport_to_school(year, planning_area)`
- Mode of Transport to Work Data
  - `get_modes_of_transport_to_work(year, planning_area)`
- Occupation Data
  - `get_occupations(year, planning_area)`
- Age Data
  - `get_age_groups(year, planning_area)`
- Religion Data
  - `get_religious_groups(year, planning_area)`
- Spoken Language Data
  - `get_spoken_languages(year, planning_area)`
- Tenancy Data
  - `get_tenancy(year, planning_area)`
- Dwelling Type Household Data
  - `get_dwelling_types(year, planning_area)`
- Dwelling Type Population Data
  - `get_population_by_dwelling_types(year, planning_area)`

**Routing Service**

- Get Route
  - `get_route(start_coordinates, end_coordinates, route_type)`
- Get Public Transport Route
  - `get_public_transport_route(start_coordinates, end_coordinates, date, time, mode, max_walk_distance=None, num_itineraries=1)`

**Static Map Generator**

- Generate Static Map
  - `generate_static_map(layer_chosen, location, zoom, width, height, polygons=None, lines=None, points=None, color=None, fill_color=None)`

