#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 7 00:45:09 2020

@author: yanglingqin
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


listing_file = "./listings_nearby.csv"


def main():
    data = pd.read_csv(listing_file, sep = ',')
    data = data[data['avgRating'].notna()]
    subway = data[["avgRating", "subway"]].copy()
    tour = data[["avgRating", "tourist_attraction"]].copy()
    
    
    
    
    #subway_box = sns.boxplot(x=subway["subway"], y=subway["avgRating"])
    tour_box = sns.boxplot(x=tour["tourist_attraction"], y=tour["avgRating"])
    plt.ylim(ymin=4, ymax=5)
    plt.show()





if __name__ == "__main__":
    # execute only if run as a script
    main()

