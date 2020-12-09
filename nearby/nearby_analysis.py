#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 7 00:45:09 2020

@author: yanglingqin

Description: o	Read from the listings csv file of rating, subway and tourist attractions data.
             o	Plot box plot of rating~subway and rating~tourist attraction.

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


listing_file = "../data_collection/listings_nearby.csv"


def main():
    data = pd.read_csv(listing_file, sep = ',')
    data = data[data['bysAvgRating'].notna()]
    subway = data[["bysAvgRating", "subway"]].copy()
    tour = data[["bysAvgRating", "tourist_attraction"]].copy()
    
    
    
    
    subway_box = sns.boxplot(x=subway["subway"], y=subway["bysAvgRating"])
    #tour_box = sns.boxplot(x=tour["tourist_attraction"], y=tour["bysAvgRating"])
    plt.ylim(ymin=4, ymax=5)
    plt.show()





if __name__ == "__main__":
    # execute only if run as a script
    main()

