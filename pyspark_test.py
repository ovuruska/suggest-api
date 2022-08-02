from pyspark.sql import SparkSession
import pymongo
import pandas as pd
from pymongo import MongoClient
from time import time


augments = pd.read_csv("augments.csv")
items = pd.read_csv("items.csv")
champions = pd.read_csv("champions.csv")



if __name__ == "__main__":
    ...


