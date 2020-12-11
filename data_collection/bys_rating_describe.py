"""
title: bys_rating_describe.py
author: Chengyu Wu (chengyu2)
data: 05-DEC-20
description: Create histogram of both Bayesian and non-Bayesian rating.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def hist_graph():
    df = pd.read_csv('../data_collection/listings_clean_copy.csv', index_col=0)
    ratings = df[['id', 'avgRating', 'bysAvgRating']]
    print(ratings.head(6))
    plt.hist(x=ratings.avgRating, bins=90,
             color='steelblue',
             normed=False,
             alpha=0.4,
             label='Original Rating')
    plt.hist(x=ratings.bysAvgRating, bins=50,
             color='#FC4A56',
             normed=False,
             alpha=0.5,
             label='Bayesian Average Rating')
    plt.legend()
    plt.title('Comparison of Bayesian and Non-bayesian Rating')
    plt.xlabel('Rating (0~5 stars)')
    plt.ylabel('Number of Listings')
    plt.xlim(4, 5)
    plt.grid(True, alpha=0.5)
    plt.show()


if __name__ == '__main__':
    hist_graph()