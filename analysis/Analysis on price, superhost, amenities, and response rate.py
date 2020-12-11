#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Analysis on price, superhost, amenities, and response rate
Description: Topcode extreme value of price and plot histogram and scatter plot against Bayesian average rating.
Boxplot on superhost and amenities.
Scatterplot on response rate. Correlation heatmap on attributes
@author: HuZhexin
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def desc_price():
    df = pd.read_csv('../data_collection/listings_clean_copy.csv', index_col=0)
    rating_price = df[['bysAvgRating', 'priceString']]
    print(rating_price.head(), '\n')
    print(rating_price.info(), '\n')
    print(rating_price.describe(), '\n')

    # Top-code extreme values outside of mean +- 2 * std
    price_mean = rating_price['priceString'].mean()
    price_std = rating_price['priceString'].std()
    upper = price_mean + 2 * price_std
    # lower = price_mean - 2 * price_std   # price would not be lower than (or even equal to) 0
    print('Upper Bound = ', upper)
    print('Lower Bound = ', 0)

    upper_replace = rating_price.priceString[rating_price.priceString < upper].max()
    lower_replace = rating_price.priceString[rating_price.priceString > 0].min()

    rating_price.priceString[rating_price.priceString > upper] = upper_replace
    rating_price.priceString[rating_price.priceString == 0] = lower_replace
    print(rating_price.describe())

    # Histogram / KDE Graph

    plt.hist(x=rating_price.priceString, bins=100,
             color='#FC4A56', density=True, alpha=0.5)
    rating_price.priceString.plot(kind='kde', color='#FC4A56')
    plt.xlim(0, 300)
    plt.xlabel('Price ($/night)')
    plt.title('Price Distribution and Kernel Density Estimation')
    plt.grid(True, alpha=0.5)
    plt.show()

    # Scatter Plot
    plt.scatter(rating_price.priceString, rating_price.bysAvgRating, c='#FC4A56', alpha=0.05)
    plt.title('Price-to-Rating Scatter Plot')
    plt.xlabel('Price ($/night)')
    plt.ylabel('Bayesian Average Rating (0 ~ 5)')
    plt.ylim(3.75, 5.1)
    plt.show()

def superhost_amenity_response():
    listings = pd.read_csv('../data_collection/listings_clean_copy.csv', index_col=0)
    attribute = listings[['bysAvgRating','neighborhood','isSuperhost','Wifi', 'Kitchen', \
                          'Heating', 'Air conditioning', 'host_response_rate', \
                              'host_acceptance_rate','manipulated_bath','bedrooms',\
                                  'beds','personCapacity','priceString']]
    
    # turn separate amenities to the total number of amenity
    amenity = []
    for index in attribute.index:
        num_amenity=int(attribute.iloc[index]['Wifi'])+int(attribute.iloc[index]['Kitchen'])+int(attribute.iloc[index]['Heating'])+int(attribute.iloc[index]['Air conditioning'])
        amenity.append(num_amenity)
    attribute['Amenity']=amenity
    
    # convert to float
    attribute['host_response_rate'] = attribute['host_response_rate'].str.rstrip('%').astype(float)/100
    attribute['host_acceptance_rate'] = attribute['host_acceptance_rate'].str.rstrip('%').astype(float)/100
    
    # convert isSuperhost from integer to string
    superhost_yn = []
    for index in attribute.index:
        if attribute.iloc[index]['isSuperhost'] == 1:
            superhost_yn.append('Yes')
        else:
            superhost_yn.append('No')
    attribute['Superhost']=superhost_yn
            
    #boxplot of listings with different number of amenities
    sns.boxplot(x=attribute['Amenity'], y=attribute['bysAvgRating'], palette = 'Set3').set(
        xlabel='Number of Amenities', 
        ylabel='Bayesian Average Rating (0 ~ 5)')
    plt.title('Amenities-to-Rating Boxplot')
    #boxplot of listings with different number of amenities and grouped by superhost or not #superhost label
    sns.boxplot(x=attribute['Amenity'], y=attribute['bysAvgRating'], hue=attribute['Superhost'], palette = 'Set2').set(
        xlabel='Number of Amenities', 
        ylabel='Bayesian Average Rating (0 ~ 5)')
    plt.title('Amenities-to-Rating with Superhost Boxplot')
    #boxplot of superhost
    sns.boxplot(x=attribute['Superhost'], y=attribute['bysAvgRating'], palette = 'Set2').set(
        xlabel='Superhost or Not', 
        ylabel='Bayesian Average Rating (0 ~ 5)')
    plt.title('Superhost-to-Rating Boxplot')
    

    # drop nan in response rate 
    attri_resp = attribute.copy()
    attri_resp.dropna(subset=['host_response_rate'],inplace=True)
    # scatterplot of response rate   
    sns.lmplot(x='host_response_rate', y='bysAvgRating', data=attri_resp, fit_reg=False, \
               hue='Superhost', legend=True, scatter_kws={'s': 4,'alpha': 0.8}, palette = 'Set2')
    plt.title('ResponseRate-to-Rating Scatter Plot')
    plt.xlabel('Host Response Rate')
    plt.ylabel('Bayesian Average Rating (0 ~ 5)')
    
    #correlation heatmap of attributes
    heatmap = attribute[['bysAvgRating','priceString','isSuperhost','Amenity', 'host_response_rate', \
                              'host_acceptance_rate','manipulated_bath','bedrooms',\
                                  'personCapacity']]
    heatmap.dropna(inplace=True)
    heatmap=heatmap.corr()
    heatmap_x=(['Rating','Price','Superhost','Amenity', 'Response', \
                              'Acceptance','#Bathroom','#Bedroom',\
                                  '#Guest'])
    sns.heatmap(heatmap, annot=True, annot_kws={"size": 8},xticklabels=heatmap_x,yticklabels=heatmap_x)
    plt.xticks(rotation=30) 
    plt.title('Attributes Correlation Heatmap')

if __name__ == '__main__':
    desc_price()
    superhost_amenity_response()











