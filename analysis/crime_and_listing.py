def crime_clean_and_merge():
    import pandas as pd
    #read crime data
    crime = pd.read_csv('NYPD_Complaint_Data_Current__Year_To_Date_.csv')
    # read airbnb data
    cleaned_listing = pd.read_csv('data_collection/listings_clean_copy.csv')
    # read insideairbnb data to update borough
    inside_airbnb = pd.read_csv('listings_insideairbnb.csv')
    inside_airbnb = inside_airbnb[['id', 'neighbourhood_group_cleansed']]
    airbnb = pd.merge(cleaned_listing, inside_airbnb,
                              how="left", on='id')
    #select desired columns
    crime = crime [['BORO_NM', 'CMPLNT_FR_DT', 'LAW_CAT_CD', 'OFNS_DESC','Latitude','Longitude']]
    crime.columns = ['borough', 'date', 'crimelv', 'crimecat', 'lat', 'long']

    #convert data type
    crime.loc[:,'date']=pd.to_datetime(crime['date'],format='%m/%d/%Y', errors = 'coerce') #date
    crime.loc[:,'crimelv'] = crime['crimelv'].astype('category')
    crime.loc[:,'crimecat'] = crime['crimecat'].astype('category')

    #filter 2019 - 2020 crime data
    crime = crime[(crime['date'] > '2019-01-01 00:00:00') & (crime['date'] < '2020-01-01 00:00:00') ]
    #remove NAs
    crime.dropna(inplace=True)

    #add population column
    crime.loc[crime['borough'] == 'BRONX', 'population'] = '1418207'
    crime.loc[crime['borough'] == 'BROOKLYN', 'population'] = '2559903'
    crime.loc[crime['borough'] == 'MANHATTAN', 'population'] = '1628706'
    crime.loc[crime['borough'] == 'QUEENS', 'population'] = '2253858'
    crime.loc[crime['borough'] == 'STATEN ISLAND', 'population'] = '476143'
    #population extracted from : https://www.citypopulation.de/en/usa/newyorkcity/

    crime = crime.astype({'population': int})

    #compute crime rate
    crime.loc[:,'crime_count'] = crime.groupby('borough')['borough'].transform("count")
    #crime rate computation source: https://oag.ca.gov/sites/all/files/agweb/pdfs/cjsc/prof10/formulas.pdf



    #create the crime dataset for merging
    crime_merge = crime.groupby('borough').size().reset_index(name='counts')
    crime_merge.loc[crime_merge['borough'] == 'BRONX', 'population'] = '1418207'
    crime_merge.loc[crime_merge['borough'] == 'BROOKLYN', 'population'] = '2559903'
    crime_merge.loc[crime_merge['borough'] == 'MANHATTAN', 'population'] = '1628706'
    crime_merge.loc[crime_merge['borough'] == 'QUEENS', 'population'] = '2253858'
    crime_merge.loc[crime_merge['borough'] == 'STATEN ISLAND', 'population'] = '476143'
    crime_merge = crime_merge.astype({'population': int})
    crime_merge['crime_rate'] = round(100000 * crime_merge['counts'] / crime_merge['population'],2)

    #remove NAs
    airbnb.dropna(inplace=True)

    #merge crime and airbnb
    airbnb.rename(columns={'neighbourhood_group_cleansed':'borough'}, inplace = True)
    airbnb_cleaned = airbnb[['id','neighborhood','bathrooms','manipulated_bath','bathroomLabel','bedrooms','bedroomLabel','beds',
                                     'guestLabel','personCapacity','roomType','isSuperhost','priceString','bysAvgRating','borough']]
    airbnb_cleaned.loc[:,'borough'] = airbnb_cleaned['borough'].str.upper()
    #
    df = pd.merge(airbnb_cleaned, crime_merge,
                             how="left", on='borough')
    print(df.describe(include='all'))
    return(df)

def Analysis_on_crime_roomtype_and_roomno():
    import pandas as pd
    df = crime_clean_and_merge()
    df['bysAvgRating'] = pd.to_numeric(df['bysAvgRating'])

    # library & dataset
    import seaborn as sns
    import matplotlib.pyplot as plt
    #relation between crime and review
    df['crime_rate'] = df['crime_rate'].astype('category')
    crime_rating = sns.boxplot(x="crime_rate", y="bysAvgRating", hue='borough', data=df,palette="Set2", width=1)
    plt.title('Relationship between Ratings and Crime Rate')
    plt.xlabel('Crime Rate')
    plt.ylabel('Bayesian Average Rating (0~5)')
    plt.ylim(4, 5)
    plt.show()
    #number of airbnb distribution by location
    airbnb_count_borough=df.groupby('borough').size().reset_index(name='counts')
    plt.bar(x="borough", height="counts", data=airbnb_count_borough, alpha=0.5, color='#EE3224')
    plt.title('Distribution of Airbnb by Location')
    plt.xlabel('Borough')
    plt.ylabel('Number of Airbnb')
    plt.ylim(0, 7000)
    plt.show()

    #review by location
    #number of review distribution by location
    df['neighborhood'] = df['neighborhood'].astype('category')
    airbnb_review_neighborhood=df.groupby('neighborhood')['bysAvgRating'].mean().reset_index(name='mean').sort_values(by='mean',ascending=0)[:10]
    print(airbnb_review_neighborhood.head())
    plt.barh(y="neighborhood", width="mean", data=airbnb_review_neighborhood, alpha=0.5, color='#EE3224')
    plt.title('Distribution of Airbnb Ratings by Location')
    plt.xlabel('Average Ratings')
    plt.ylabel('neighborhood')
    plt.show()

    #price by location
    df['priceString'] = df['priceString'].astype('int64')
    airbnb_price_borough=df.groupby('borough')['priceString'].mean().reset_index(name='mean_price')
    print(airbnb_price_borough.head())
    plt.bar(x="borough", height="mean_price", data=airbnb_price_borough, alpha=0.5, color='#EE3224')
    plt.title('Distribution of Airbnb Price by Location')
    plt.xlabel('Borough')
    plt.ylabel('Price of Airbnb')
    plt.ylim(0, 200)
    plt.show()
    #relation between roomtype and review
    roomtype_review = sns.boxplot(x="roomType", y="bysAvgRating", data=df,palette="Set2")
    plt.title('Relationship between Ratings and Room Type')
    plt.xlabel('Room Type')
    plt.ylabel('Bayesian Average Rating (0~5)')
    plt.show()
    #relation between roomtype and review by borough
    roomtype_review_borough = sns.boxplot(x="borough", y="bysAvgRating", hue="roomType", data=df, palette="Set2")
    plt.title('Relationship between Ratings and Room Type By Location')
    plt.xlabel('Borough')
    plt.ylabel('Bayesian Average Rating (0~5)')
    plt.show()
    #types of bedroom by location
    #relation between types of bedroom and review - boxplot
    roomtype_review = sns.boxplot(x="bedroomLabel", y="bysAvgRating", data=df,palette="Set2")
    plt.title('Relationship between Ratings and Number of Bedroom')
    plt.xlabel('Number of Bedroom')
    plt.ylabel('Bayesian Average Rating (0~5)')
    plt.show()
    # use the function regplot to make a scatterplot
    sns.regplot(x="bedrooms", y="bysAvgRating", data=df,scatter_kws={"color":'#EE3224',"alpha":0.2,"s":10} )
    plt.title('Relationship between Ratings and Number of Bedroom')
    plt.xlabel('Number of Bedroom')
    plt.ylabel('Bayesian Average Rating (0~5)')
    plt.show()

    #types of bathroom by location
    #relation between types of bathroom and review - boxplot
    #treating bathroom type as categorical
    roomtype_review = sns.boxplot(x="manipulated_bath", y="bysAvgRating", data=df,palette="Set2")
    plt.show()
    #treating bathroom type as numeric
    sns.regplot(x="manipulated_bath", y="bysAvgRating", data=df,scatter_kws={"color":'#EE3224',"alpha":0.2,"s":10} )
    plt.show()

def main():
    print(Analysis_on_crime_roomtype_and_roomno())

if __name__ == '__main__':
    main()
