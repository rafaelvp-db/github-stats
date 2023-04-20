### Usage

In this notebook, we fetch and parse Github repo stats into Pandas Dataframes for further visualization in a Databricks workspace, e.g.:

```python

import requests
import json
import pandas as pd


BASE_URL = "https://github.com/rafaelvp-db/github-stats/raw/master/stats/{}.json"


def get_stats(stats: str):

  response = requests.get(BASE_URL.format(stats))
  output = json.loads(response.text.replace("][", ","))

  return output

views = get_stats("views")
clones = get_stats("clones")

# Parse into Pandas DataFrames

views_df = pd.DataFrame.from_dict(views, orient = "columns")
views_df["timestamp"] = pd.to_datetime(views_df["timestamp"])

clones_df = pd.DataFrame.from_dict(clones, orient = "columns")
clones_df["timestamp"] = pd.to_datetime(clones_df["timestamp"])
```


