from github import Github
import os
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import (
    StructType,
    StructField,
    TimestampType,
    IntegerType,
    StringType
)


def get_repos_traffic():
    # using an access token
    access_token = os.environ["GITHUB_ACCESS_TOKEN"]
    g = Github(access_token)

    user = g.get_user(login="rafaelvp-db")
    repos = user.get_repos()
    print(repos)
    views_list = []
    clones_list = []

    for repo in repos:
        print(repo.name)
        views = repo.get_views_traffic(per = "day")
        clones = repo.get_clones_traffic(per = "day")
        list_views = [
            {
                "repo": repo.name,
                "uniques": view.uniques,
                "count": view.count,
                "timestamp": view.timestamp
            }
            for view in views["views"]
        ]

        list_clones = [
            {
                "repo": repo.name,
                "uniques": clone.uniques,
                "count": clone.count,
                "timestamp": clone.timestamp
            }
            for clone in clones["clones"]
        ]
        views_list.extend(list_views)
        clones_list.extend(list_clones)
    
    schema = StructType([
        StructField("repo", StringType(), False),
        StructField("uniques", IntegerType(), False),
        StructField("count", IntegerType(), False),
        StructField("timestamp", TimestampType(), False),
    ])
    spark = SparkSession.builder.getOrCreate()
    df_views = spark.createDataFrame(views_list, schema = schema)
    df_clones = spark.createDataFrame(clones_list, schema = schema)
    df_views.write.saveAsTable("views")
    df_clones.write.saveAsTable("clones")

if __name__ == "__main__":
    get_repos_traffic()
