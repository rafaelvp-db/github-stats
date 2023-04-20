# Databricks notebook source
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

# COMMAND ----------

views_df = pd.DataFrame.from_dict(views, orient = "columns")
views_df["timestamp"] = pd.to_datetime(views_df["timestamp"])
display(views_df)

# COMMAND ----------

clones_df = pd.DataFrame.from_dict(clones, orient = "columns")
clones_df["timestamp"] = pd.to_datetime(clones_df["timestamp"])
display(clones_df)

# COMMAND ----------


