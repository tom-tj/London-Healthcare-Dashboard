from sklearn.linear_model import LinearRegression
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st


# --------------------------------------------------
# Emergency Admissions Datasets
# --------------------------------------------------
@st.cache
def emergency_admissions_data():
    e_admissions = {}

    e_admissions['df_2003'] = pd.read_csv('Data/Emergencyadmissions/2003-04-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2004'] = pd.read_csv('Data/Emergencyadmissions/2004-05-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2005'] = pd.read_csv('Data/Emergencyadmissions/2005-06-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2006'] = pd.read_csv('Data/Emergencyadmissions/2006-07-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2007'] = pd.read_csv('Data/Emergencyadmissions/2007-08-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2008'] = pd.read_csv('Data/Emergencyadmissions/2008-09-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2009'] = pd.read_csv('Data/Emergencyadmissions/2009-10-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2010'] = pd.read_csv('Data/Emergencyadmissions/2010-11-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2011'] = pd.read_csv('Data/Emergencyadmissions/2011-12-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2012'] = pd.read_csv('Data/Emergencyadmissions/2012-13-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2013'] = pd.read_csv('Data/Emergencyadmissions/2013-14-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2014'] = pd.read_csv('Data/Emergencyadmissions/2014-15-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2015'] = pd.read_csv('Data/Emergencyadmissions/EmergencyAdmissions2015-16.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2016'] = pd.read_csv('Data/Emergencyadmissions/EmergencyAdmissions2016-17.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2017'] = pd.read_csv('Data/Emergencyadmissions/EmergencyAdmissions2017-18.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2018'] = pd.read_csv('Data/Emergencyadmissions/EmergencyAdmissions2018-19.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2019'] = pd.read_csv('Data/Emergencyadmissions/EmergencyAdmissions2019-20.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2020'] = pd.read_csv('Data/Emergencyadmissions/EmergencyAdmissions2020-21.csv', dtype=str, keep_default_na=False)

    london_boroughs = ['City of London', 'Westminster', 'Kensington and Chelsea', 'Hammersmith and Fulham', 'Wandsworth', 
    'Lambeth', 'Southwark', 'Tower Hamlets', 'Hackney', 'Islington', 'Camden', 'Brent', 'Ealing', 'Hounslow', 'Richmond upon Thames', 
    'Kingston upon Thames', 'Merton', 'Sutton', 'Croydon', 'Bromley', 'Lewisham', 'Greenwich', 'Bexley', 'Havering', 
    'Barking and Dagenham', 'Redbridge', 'Newham', 'Waltham Forest', 'Haringey', 'Enfield', 'Barnet', 'Harrow', 'Hillingdon']

    borough_pop_proportions =  {}
    populations_df = pd.read_csv('Data/populations.csv', dtype=str, keep_default_na=False)

    nhs_ccgs = ['NHS CITY AND HACKNEY CCG', 'NHS CENTRAL LONDON (WESTMINSTER) CCG', 'NHS WEST LONDON CCG',
                'NHS HAMMERSMITH AND FULHAM CCG', 'NHS WANDSWORTH CCG', 'NHS LAMBETH CCG', 'NHS SOUTHWARK CCG',
                'NHS TOWER HAMLETS CCG', 'NHS ISLINGTON CCG', 'NHS CAMDEN CCG', 'NHS BRENT CCG', 'NHS EALING CCG',
                'NHS HOUNSLOW CCG', 'NHS RICHMOND CCG', 'NHS KINGSTON CCG', 'NHS MERTON CCG', 'NHS SUTTON CCG',
                'NHS CROYDON CCG', 'NHS BROMLEY CCG', 'NHS LEWISHAM CCG', 'NHS GREENWICH CCG', 'NHS BEXLEY CCG',
                'NHS HAVERING CCG', 'NHS BARKING AND DAGENHAM CCG', 'NHS REDBRIDGE CCG', 'NHS NEWHAM CCG',
                'NHS WALTHAM FOREST CCG', 'NHS HARINGEY CCG', 'NHS ENFIELD CCG', 'NHS BARNET CCG', 'NHS HARROW CCG',
                'NHS HILLINGDON CCG']

    # Mapping of Clinical Commissioning Groups (CCGs) to the London Boroughs they cover
    borough_ccg_mapping = {}
    borough_ccg_mapping['NHS CITY AND HACKNEY CCG']                      = ['City of London', 'Hackney']
    borough_ccg_mapping['NHS CENTRAL LONDON (WESTMINSTER) CCG']          = 'Westminster'
    borough_ccg_mapping['NHS WEST LONDON CCG']                           = 'Kensington and Chelsea'
    borough_ccg_mapping['NHS HAMMERSMITH AND FULHAM CCG']                = 'Hammersmith and Fulham'
    borough_ccg_mapping['NHS WANDSWORTH CCG']                            = 'Wandsworth'
    borough_ccg_mapping['NHS LAMBETH CCG']                               = 'Lambeth'
    borough_ccg_mapping['NHS SOUTHWARK CCG']                             = 'Southwark'
    borough_ccg_mapping['NHS TOWER HAMLETS CCG']                         = 'Tower Hamlets'
    borough_ccg_mapping['NHS ISLINGTON CCG']                             = 'Islington'
    borough_ccg_mapping['NHS CAMDEN CCG']                                = 'Camden'
    borough_ccg_mapping['NHS BRENT CCG']                                 = 'Brent'
    borough_ccg_mapping['NHS EALING CCG']                                = 'Ealing'
    borough_ccg_mapping['NHS HOUNSLOW CCG']                              = 'Hounslow'
    borough_ccg_mapping['NHS RICHMOND CCG']                              = 'Richmond upon Thames'
    borough_ccg_mapping['NHS KINGSTON CCG']                              = 'Kingston upon Thames'
    borough_ccg_mapping['NHS MERTON CCG']                                = 'Merton'
    borough_ccg_mapping['NHS SUTTON CCG']                                = 'Sutton'
    borough_ccg_mapping['NHS CROYDON CCG']                               = 'Croydon'
    borough_ccg_mapping['NHS BROMLEY CCG']                               = 'Bromley'
    borough_ccg_mapping['NHS LEWISHAM CCG']                              = 'Lewisham'
    borough_ccg_mapping['NHS GREENWICH CCG']                             = 'Greenwich'
    borough_ccg_mapping['NHS BEXLEY CCG']                                = 'Bexley'
    borough_ccg_mapping['NHS HAVERING CCG']                              = 'Havering'
    borough_ccg_mapping['NHS BARKING AND DAGENHAM CCG']                  = 'Barking and Dagenham'
    borough_ccg_mapping['NHS REDBRIDGE CCG']                             = 'Redbridge'
    borough_ccg_mapping['NHS NEWHAM CCG']                                = 'Newham'
    borough_ccg_mapping['NHS WALTHAM FOREST CCG']                        = 'Waltham Forest'
    borough_ccg_mapping['NHS HARINGEY CCG']                              = 'Haringey'
    borough_ccg_mapping['NHS ENFIELD CCG']                               = 'Enfield'
    borough_ccg_mapping['NHS BARNET CCG']                                = 'Barnet'
    borough_ccg_mapping['NHS HARROW CCG']                                = 'Harrow'
    borough_ccg_mapping['NHS HILLINGDON CCG']                            = 'Hillingdon'

    # Transform data from 2003-2014
    for i in range(2003,2015):
        df_str = 'df_' + str(i)
        # 2009-2010 formatted differently
        if i == 2009 or i == 2010:
            # Drop unnecessary columns in dataframes for 2009, 2010
            e_admissions[df_str] = e_admissions[df_str].drop(e_admissions[df_str].iloc[:, 15:241], axis=1)
            # Drop empty columns
            e_admissions[df_str] = e_admissions[df_str].drop(e_admissions[df_str].iloc[:, 2:16],axis = 1)
            e_admissions[df_str] = e_admissions[df_str].drop(e_admissions[df_str].iloc[:, 3:11],axis = 1)
            # Drop unnecessary and empty rows
            e_admissions[df_str] = e_admissions[df_str][e_admissions[df_str].Area != '']
            e_admissions[df_str] = e_admissions[df_str].drop(e_admissions[df_str].tail(12).index)
            # Rename Emergency Admissions Column
            e_admissions[df_str] = e_admissions[df_str].rename({'Number of Admission Continuous Inpatient Spells - Numerator.1': 'EmergencyAdmissions'}, axis=1)
        else:
            # Drop unnecessary columns
            e_admissions[df_str] = e_admissions[df_str].drop(e_admissions[df_str].columns[[0,2,4,5,6,7,8,9]], axis=1)
            # Drop unnecessary rows
            e_admissions[df_str].drop(e_admissions[df_str].tail(30).index, inplace=True)
            # Rename Emergency Admissions Column
            e_admissions[df_str] = e_admissions[df_str].rename({'Number of Admission Continuous Inpatient Spells - Numerator': 'EmergencyAdmissions'}, axis=1)
            # Transform 'Area' column values
            e_admissions[df_str] = e_admissions[df_str][e_admissions[df_str].Area != 'Inner London']
            e_admissions[df_str]['Area'].replace('', np.nan, inplace=True)
            e_admissions[df_str].dropna(subset=['Area'], inplace=True)
            # Reformat Emergency Admissions column to integer
            e_admissions[df_str]['EmergencyAdmissions'] = e_admissions[df_str]['EmergencyAdmissions'].apply(lambda x: int(x))

    # Transform data from 2015-2020
    for i in range(2015,2021):
        df_str = 'df_' + str(i)
        # Drop unnecessary columns
        for i in range(len(e_admissions[df_str].columns)):
            if i != 1 and i != 13:
                e_admissions[df_str] = e_admissions[df_str].drop(['Unnamed: ' + str(i)], axis=1)
        # Rename columns for NHS CCG Group and Emergency Admissions
        e_admissions[df_str] = e_admissions[df_str].rename({'Unnamed: 1': 'Area', 'Unnamed: 13': 'EmergencyAdmissions'}, axis='columns')
        # Drop unnecessary and empty rows
        e_admissions[df_str] = e_admissions[df_str].iloc[13:]
        e_admissions[df_str] = e_admissions[df_str][e_admissions[df_str].Area != '']
        # Reformat all NHS CCG Groups to uppercase
        e_admissions[df_str]['Area'] = e_admissions[df_str]['Area'].str.upper()
        # Reformat Emergency Admissions column to integer
        e_admissions[df_str]['EmergencyAdmissions'] = e_admissions[df_str]['EmergencyAdmissions'].str.replace(',', '')
        e_admissions[df_str]['EmergencyAdmissions'] = e_admissions[df_str]['EmergencyAdmissions'].apply(lambda x: int(x))

    # Map CCGs to Boroughs for 2015-2020
    for i in range(2015,2021):
        df_str = 'df_' + str(i)
        for ccg in nhs_ccgs:
            # City and Hackney previously dealt with
            if ccg == 'NHS CITY AND HACKNEY CCG':
                continue
            # In 'Area' column, replace CCGs with the Borough they cover
            e_admissions[df_str].loc[e_admissions[df_str]['Area'] == ccg, 'Area'] = borough_ccg_mapping[ccg]

    # Map City and Hackney CCG to its Boroughs, emergency admissions value split by population proportions
    for i in range(2015,2021):
        df_str = 'df_' + str(i)
        columnstr = 'population_' + str(i)
        # Combined populations of both Boroughs
        total_population = 0.0
        # List of boroughs covered by provider
        boroughs = borough_ccg_mapping['NHS CITY AND HACKNEY CCG']
        for borough in boroughs:
            # Add to total population for its provider
            total_population += int(populations_df.loc[populations_df['laname20'] == borough, columnstr])
            # Add new rows for each borough to current emergency admissions dataframe (to eventually be in place of provider)
            df_temp = e_admissions[df_str].loc[e_admissions[df_str]['Area'] == 'NHS CITY AND HACKNEY CCG']
            df_temp.loc[df_temp['Area'] == 'NHS CITY AND HACKNEY CCG', 'Area'] = borough
            e_admissions[df_str] = pd.concat([e_admissions[df_str],df_temp])
        for borough in boroughs:
            # Get each borough's proportion of combined population
            borough_pop_proportions[borough] = int(populations_df.loc[populations_df['laname20'] == borough, columnstr])/total_population
            # In current emergency admissions dataframe, set row with borough to floor(provider-admissions * population-proportions
            new_admissions = int(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == 'NHS CITY AND HACKNEY CCG', 'EmergencyAdmissions']) * borough_pop_proportions[borough]
            e_admissions[df_str].loc[e_admissions[df_str]['Area'] == borough, 'EmergencyAdmissions'] = int(new_admissions)
        # Drop all original provider rows
        e_admissions[df_str] = e_admissions[df_str][e_admissions[df_str]['Area'].isin(london_boroughs)]
    
    # Reset index for all dataframes
    for i in range(2008,2021):
        df_str = 'df_' + str(i)
        e_admissions[df_str] = e_admissions[df_str].reset_index(drop=True)    

    return e_admissions




# --------------------------------------------------
# ACSC Admissions Datasets
# --------------------------------------------------
@st.cache
def acsc_admissions_data():
    df_acsc = pd.read_csv('Data/ACSC/NHSOF_2.3.i_I00708_D.csv', dtype=str, keep_default_na=False)
    # Drop unnecessary columns
    df_acsc = df_acsc.drop(['Period of coverage', 'Breakdown', 'Level', 'Indicator value', 
        'Lower CI', 'Upper CI', 'Standardised ratio', 'Standardised ratio lower CI', 
        'Standardised ratio upper CI', 'Expected', 'Percent unclassified'], axis=1)
    # Rename column for Borough
    df_acsc = df_acsc.rename({'Level description': 'Area'}, axis='columns')

    # Standardise year values from 'xxxx/xx' format to 'xxxx'
    df_acsc['Year'] = df_acsc['Year'].str[:-3]

    # Cover edge cases where value 0 is indicated by '*'
    df_acsc['Observed'] = df_acsc['Observed'].str.replace('*', '0')

    return df_acsc




# --------------------------------------------------
# Takeaway Datasets
# --------------------------------------------------
@st.cache
def fast_food_data():
    df_fastfood = pd.read_csv('Data/FastFood/Takeaway&Food stands01-20.csv', dtype=str, keep_default_na=False)
    df_restaurants = pd.read_csv('Data/FastFood/LicensedRestaurantsLondonBoroughs20012020.csv', dtype=str, keep_default_na=False)

    # Rename column for Borough
    df_fastfood = df_fastfood.rename({'Unnamed: 1': 'Area'}, axis='columns')
    df_restaurants = df_restaurants.rename({'Unnamed: 1': 'Area'}, axis='columns')

    # Rename column for each year to 'xxxx' format
    for i in range(len(df_fastfood.columns)):
        if i != 0 and i != 1:
            if i < 11:
                df_fastfood = df_fastfood.rename({'Unnamed: ' + str(i): '200'+str(i-1)}, axis='columns')
                df_restaurants = df_restaurants.rename({'Unnamed: ' + str(i): '200'+str(i-1)}, axis='columns')
            else:
                df_fastfood = df_fastfood.rename({'Unnamed: ' + str(i): '20'+str(i-1)}, axis='columns')
                df_restaurants = df_restaurants.rename({'Unnamed: ' + str(i): '20'+str(i-1)}, axis='columns')
    

    return df_fastfood
    



# --------------------------------------------------
# Air Pollution Datasets
# --------------------------------------------------
@st.cache
def air_pollution_data():
    air_pollution = {}

    air_pollution['df_2008'] = pd.read_csv('Data/AirPollution/Road 2008 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2008_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2008.csv', dtype=str, keep_default_na=False)
    # Rename columns for Area(Borough), PM25 value
    air_pollution['df_2008'] = air_pollution['df_2008'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2008_other'] = air_pollution['df_2008_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2008_other'].drop(air_pollution['df_2008_other'].tail(3).index, inplace = True)
    # Remove rows not related to Boroughs
    air_pollution['df_2008'].drop(air_pollution['df_2008'].index[1:52], inplace = True)
    air_pollution['df_2008'].drop(air_pollution['df_2008'].tail(22).index, inplace = True)
    # Remove all rows except for Borough totals
    air_pollution['df_2008'] = air_pollution['df_2008'][air_pollution['df_2008']['Area'].str.contains("Total") == True]
    # Format Borough names to standard
    air_pollution['df_2008']['Area'] = air_pollution['df_2008']['Area'].str.replace(' Total', '')
    air_pollution['df_2008']['Area'] = air_pollution['df_2008']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # Reset dataframe index
    air_pollution['df_2008'].reset_index(drop=True, inplace=True)
    # Add total column to 'NRMM/Agriculture/Other' total column
    air_pollution['df_2008']['PM25'] = air_pollution['df_2008']['PM25'].astype(float) + air_pollution['df_2008_other']['PM25'].astype(float)
    # Reformat outlier Borough names
    air_pollution['df_2008'].loc[air_pollution['df_2008']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2008'].loc[air_pollution['df_2008']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2008'].loc[air_pollution['df_2008']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2008'].loc[air_pollution['df_2008']['Area'] == 'City', 'Area'] = 'City of London'

    air_pollution['df_2010'] = pd.read_csv('Data/AirPollution/Road 2010 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2010_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2010.csv', dtype=str, keep_default_na=False)
    # Rename columns for Area(Borough), PM25 value
    air_pollution['df_2010'] = air_pollution['df_2010'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2010_other'] = air_pollution['df_2010_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2010_other'].drop(air_pollution['df_2010_other'].tail(3).index, inplace = True)
    # Remove rows not related to Boroughs
    air_pollution['df_2010'].drop(air_pollution['df_2010'].index[1:52], inplace = True)
    air_pollution['df_2010'].drop(air_pollution['df_2010'].tail(22).index, inplace = True)
    # Remove all rows except for Borough totals
    air_pollution['df_2010'] = air_pollution['df_2010'][air_pollution['df_2010']['Area'].str.contains("Total") == True]
    # Format Borough names to standard
    air_pollution['df_2010']['Area'] = air_pollution['df_2010']['Area'].str.replace(' Total', '')
    air_pollution['df_2010']['Area'] = air_pollution['df_2010']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # Reset dataframe index
    air_pollution['df_2010'].reset_index(drop=True, inplace=True)
    # Add total column to 'NRMM/Agriculture/Other' total column
    air_pollution['df_2010']['PM25'] = air_pollution['df_2010']['PM25'].astype(float) + air_pollution['df_2010_other']['PM25'].astype(float)
    # Reformat outlier Borough names
    air_pollution['df_2010'].loc[air_pollution['df_2010']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2010'].loc[air_pollution['df_2010']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2010'].loc[air_pollution['df_2010']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2010'].loc[air_pollution['df_2010']['Area'] == 'City', 'Area'] = 'City of London'

    air_pollution['df_2012'] = pd.read_csv('Data/AirPollution/Road 2012 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2012_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2012.csv', dtype=str, keep_default_na=False)
    # Rename columns for Area(Borough), PM25 value
    air_pollution['df_2012'] = air_pollution['df_2012'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2012_other'] = air_pollution['df_2012_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2012_other'].drop(air_pollution['df_2012_other'].tail(3).index, inplace = True)
    # Remove rows not related to boroughs
    air_pollution['df_2012'].drop(air_pollution['df_2012'].index[1:52], inplace = True)
    air_pollution['df_2012'].drop(air_pollution['df_2012'].tail(22).index, inplace = True)
    # Remove all rows except for borough totals
    air_pollution['df_2012'] = air_pollution['df_2012'][air_pollution['df_2012']['Area'].str.contains("Total") == True]
    # Format Borough names to standard
    air_pollution['df_2012']['Area'] = air_pollution['df_2012']['Area'].str.replace(' Total', '')
    air_pollution['df_2012']['Area'] = air_pollution['df_2012']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # Reset dataframe index
    air_pollution['df_2012'].reset_index(drop=True, inplace=True)
    # Add total column to 'NRMM/Agriculture/Other' total column
    air_pollution['df_2012']['PM25'] = air_pollution['df_2012']['PM25'].astype(float) + air_pollution['df_2012_other']['PM25'].astype(float)
    # Reformat outlier Borough names
    air_pollution['df_2012'].loc[air_pollution['df_2012']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2012'].loc[air_pollution['df_2012']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2012'].loc[air_pollution['df_2012']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2012'].loc[air_pollution['df_2012']['Area'] == 'City', 'Area'] = 'City of London'

    air_pollution['df_2013'] = pd.read_csv('Data/AirPollution/PM2.5 Totals by Borough2013.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2013'] = air_pollution['df_2013'].rename({'PM2.5 Pivot Table by Borough': 'Area', 'Unnamed: 13': 'PM25'}, axis='columns')
    air_pollution['df_2013']['PM25'] = air_pollution['df_2013']['PM25'].str.replace('\t', '')
    # Reformat outlier Borough names
    air_pollution['df_2013'].loc[air_pollution['df_2013']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2013'].loc[air_pollution['df_2013']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2013'].loc[air_pollution['df_2013']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2013'].loc[air_pollution['df_2013']['Area'] == 'City', 'Area'] = 'City of London'

    air_pollution['df_2015'] = pd.read_csv('Data/AirPollution/Road 2015 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2015_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2015.csv', dtype=str, keep_default_na=False)
    # Rename columns for Area(Borough), PM25 value
    air_pollution['df_2015'] = air_pollution['df_2015'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2015_other'] = air_pollution['df_2015_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2015_other'].drop(air_pollution['df_2015_other'].tail(3).index, inplace = True)
    # Remove rows not related to boroughs
    air_pollution['df_2015'].drop(air_pollution['df_2015'].index[1:52], inplace = True)
    air_pollution['df_2015'].drop(air_pollution['df_2015'].tail(22).index, inplace = True)
    # Remove all rows except for borough totals
    air_pollution['df_2015'] = air_pollution['df_2015'][air_pollution['df_2015']['Area'].str.contains("Total") == True]
    # Format Borough names to standard
    air_pollution['df_2015']['Area'] = air_pollution['df_2015']['Area'].str.replace(' Total', '')
    air_pollution['df_2015']['Area'] = air_pollution['df_2015']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # Reset dataframe index
    air_pollution['df_2015'].reset_index(drop=True, inplace=True)
    # Add total column to 'NRMM/Agriculture/Other' total column
    air_pollution['df_2015']['PM25'] = air_pollution['df_2015']['PM25'].astype(float) + air_pollution['df_2015_other']['PM25'].astype(float)
    # Reformat outlier Borough names
    air_pollution['df_2015'].loc[air_pollution['df_2015']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2015'].loc[air_pollution['df_2015']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2015'].loc[air_pollution['df_2015']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2015'].loc[air_pollution['df_2015']['Area'] == 'City', 'Area'] = 'City of London'

    air_pollution['df_2016'] = pd.read_csv('Data/AirPollution/PM2.5 Summary2016.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2016'] = air_pollution['df_2016'].transpose()
    air_pollution['df_2016'] = air_pollution['df_2016'].rename({6: 'Area', 68: 'PM25'}, axis='columns')
    air_pollution['df_2016']['PM25'] = air_pollution['df_2016']['PM25'].str.replace('\t', '')
    # Reformat outlier Borough names
    air_pollution['df_2016'].loc[air_pollution['df_2016']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2016'].loc[air_pollution['df_2016']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2016'].loc[air_pollution['df_2016']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2016'].loc[air_pollution['df_2016']['Area'] == 'City', 'Area'] = 'City of London'

    air_pollution['df_2019'] = pd.read_csv('Data/AirPollution/PM2.5 Summary2019.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2019'] = air_pollution['df_2019'].transpose()
    air_pollution['df_2019'] = air_pollution['df_2019'].rename({6: 'Area', 71: 'PM25'}, axis='columns')
    air_pollution['df_2019']['PM25'] = air_pollution['df_2019']['PM25'].str.replace('\t', '')
    # Reformat outlier Borough names
    air_pollution['df_2019'].loc[air_pollution['df_2019']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2019'].loc[air_pollution['df_2019']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2019'].loc[air_pollution['df_2019']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2019'].loc[air_pollution['df_2019']['Area'] == 'City', 'Area'] = 'City of London'

    air_pollution['df_2020'] = pd.read_csv('Data/AirPollution/Road 2020 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2020_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2020.csv', dtype=str, keep_default_na=False)
    # Rename columns for Area(Borough), PM25 value
    air_pollution['df_2020'] = air_pollution['df_2020'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2020_other'] = air_pollution['df_2020_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2020_other'].drop(air_pollution['df_2020_other'].tail(3).index, inplace = True)
    # Remove rows not related to boroughs
    air_pollution['df_2020'].drop(air_pollution['df_2020'].index[1:52], inplace = True)
    air_pollution['df_2020'].drop(air_pollution['df_2020'].tail(22).index, inplace = True)
    # Remove all rows except for borough totals
    air_pollution['df_2020'] = air_pollution['df_2020'][air_pollution['df_2020']['Area'].str.contains("Total") == True]
    # Format Borough names to standard
    air_pollution['df_2020']['Area'] = air_pollution['df_2020']['Area'].str.replace(' Total', '')
    air_pollution['df_2020']['Area'] = air_pollution['df_2020']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # Reset dataframe index
    air_pollution['df_2020'].reset_index(drop=True, inplace=True)
    # Add total column to 'NRMM/Agriculture/Other' total column
    air_pollution['df_2020']['PM25'] = air_pollution['df_2020']['PM25'].astype(float) + air_pollution['df_2020_other']['PM25'].astype(float)
    # Reformat outlier Borough names
    air_pollution['df_2020'].loc[air_pollution['df_2020']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2020'].loc[air_pollution['df_2020']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2020'].loc[air_pollution['df_2020']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2020'].loc[air_pollution['df_2020']['Area'] == 'City', 'Area'] = 'City of London'



    return air_pollution




# --------------------------------------------------
# Dashboard
# --------------------------------------------------

def intro():
    st.title('London Healthcare Dashboard')

    # Get transformed dataframes from streamlit cache
    e_admissions = emergency_admissions_data()
    df_acsc = acsc_admissions_data()
    df_fastfood = fast_food_data()
    air_pollution = air_pollution_data()

    # Remove whitespace from the top of the page and sidebar
    st.markdown("""
            <style>
                .css-18e3th9 {
                        padding-top: 1rem;
                        padding-bottom: 10rem;
                        padding-left: 4rem;
                        padding-right: 4rem;
                    }
                .css-1d391kg {
                        padding-top: 1.5rem;
                        padding-right: 1rem;
                        padding-bottom: 3.5rem;
                        padding-left: 1rem;
                    }
            </style>
            """, unsafe_allow_html=True)

    # Read in London Boroughs geographical data (borough boundaries) using geopandas
    london_df = gpd.read_file('Data/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp')

    # Date slider widget
    year = st.slider('Select a range of values', 2003, 2020, 2003)
    df_str = 'df_' + str(year)

    if str(year) == '2020':
        st.write('*Note: from 2020 onwards NHS "Hospital Admitted Patient Care Activity" groups CCG data for many boroughs together, therefore the data is incomplete at an individual borough level*')

    # Merge geographic information for boroughs with emergency admissions data
    if year < 2015:
        merged = london_df.set_index('NAME').join(e_admissions[df_str].set_index('Area'))
    else:
        merged = london_df.set_index('NAME').join(e_admissions[df_str].set_index('Area'))
        # new df -> convert provider to borough
        # merge new df

    # Create choropleth map of London Boroughs using merged df for the year selected
    vmin,vmax=merged['EmergencyAdmissions'].min(),merged['EmergencyAdmissions'].max()
    fig,ax=plt.subplots(1,figsize=(12,7.5))
    merged.plot(column='EmergencyAdmissions',cmap='PuBu',ax=ax)
    merged.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=0.1)
    ax.axis('off')
    plt.title('Emergency Hospital Admissions',{'fontsize': '14',
    'fontweight' :'100'})
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)

    # Set webpage columns
    fig_col1, fig_col2 = st.columns((2,4), gap="large")

    with fig_col1:
        # Plot ordered bar chart of emergency admissions by Borough for the year selected
        new_df = e_admissions[df_str][['Area', 'EmergencyAdmissions']]
        bars = alt.Chart(new_df).mark_bar(size=16).encode(
            x=alt.X('EmergencyAdmissions:Q', title=''),
            y=alt.Y('Area', sort='-x', title='')
        ).properties(
            # width=alt.Step(50),
            width=500,
            height=850
        ).configure_axis(
            grid=False,
            labelFontSize=16,
        ).configure_view(
            strokeWidth=0
        )
        st.altair_chart(bars)

    with fig_col2:
        # Plot choropleth map
        st.pyplot(fig)




# --------------------------------------------------
# Borough Data Suite
# --------------------------------------------------

def individual_data_suite(borough):
    # Set page title to borough being viewed
    st.title(str(borough))

    # Remove whitespace from the top of the page and sidebar
    st.markdown("""
            <style>
                .css-18e3th9 {
                        padding-top: 1rem;
                        padding-bottom: 10rem;
                        padding-left: 4rem;
                        padding-right: 4rem;
                    }
                .css-1d391kg {
                        padding-top: 1.5rem;
                        padding-right: 1rem;
                        padding-bottom: 3.5rem;
                        padding-left: 1rem;
                    }
            </style>
            """, unsafe_allow_html=True)

    # Get transformed dataframes from streamlit cache
    e_admissions = emergency_admissions_data()
    df_acsc = acsc_admissions_data()
    df_fastfood = fast_food_data()
    air_pollution = air_pollution_data()

    tab1, tab2 = st.tabs(["Time Series", "Attribute Correlations"])

    with tab1:
        # Date slider widget from 2003-2020
        dates = st.slider('Select a range of values',2003, 2020, (2003, 2020))
        # Attributes option select
        options = st.multiselect('Select attributes', ['Emergency Admissions', 'Ambulatory Care Sensitive Condition Admissions', 'Fast Food Prevalence', 'Particulate Emissions'], default=['Emergency Admissions', 'Ambulatory Care Sensitive Condition Admissions', 'Fast Food Prevalence', 'Particulate Emissions'])

        # Rename attributes for later line graphing
        if 'Emergency Admissions' in options:
            options = list(map(lambda x: x.replace('Emergency Admissions', 'Emergency Admissions/100'), options))
        if 'Ambulatory Care Sensitive Condition Admissions' in options:
            options = list(map(lambda x: x.replace('Ambulatory Care Sensitive Condition Admissions', 'ACSC Admissions/10'), options))
        if 'Fast Food Prevalence' in options:
            options = list(map(lambda x: x.replace('Fast Food Prevalence', 'Number of Takeaways'), options))
        if 'Particulate Emissions' in options:
            options = list(map(lambda x: x.replace('Particulate Emissions', 'PM2.5 Particulate Emissions (tonnes/year)'), options))
        
        # Add 'Date' in order to create 'Date' column in dataframe
        options.insert(0, 'Date')
        # Use list of attributes to create df
        borough_df = pd.DataFrame(columns=options)

        # List of years for which there is no air pollution data available
        no_air_vals = [2003,2004,2005,2006,2007,2009,2011,2014,2017,2018]

        # Create rows with attribute values for each year in range
        for i in range(dates[0], dates[1]+1):
            year_vals = [str(i)]
            df_str = 'df_' + str(i)
            if 'Emergency Admissions/100' in options:
                # NHS data incomplete for 2020
                if i == 2020:
                    if borough not in ['Ealing', 'Brent', 'Newham', 'Waltham Forest', 'Hounslow', 'Hillingdon', 'Havering', 'Redbridge', 'Tower Hamlets', 'Harrow', 'Hackney', 'Barking and Dagenham', 'Kensington and Chelsea', 'Hammersmith and Fulham', 'Westminster', 'City of London']:
                        year_vals.append(np.nan)
                    else:
                        year_vals.append(float(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == str(borough), 'EmergencyAdmissions'])/100)
                else:
                    year_vals.append(float(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == str(borough), 'EmergencyAdmissions'])/100)
            if 'ACSC Admissions/10' in options:
                df_str = str(i)
                year_vals.append(float(df_acsc.loc[(df_acsc['Year'] == df_str) & (df_acsc['Area'] == str(borough)) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed'])/10)
            if 'Number of Takeaways' in options:
                df_str = str(i)
                year_vals.append(float(df_fastfood.loc[(df_fastfood['Area'] == str(borough))].head(1)[df_str]))
            if 'PM2.5 Particulate Emissions (tonnes/year)' in options:
                df_str = 'df_' + str(i)
                if i in no_air_vals:
                    year_vals.append(np.nan)
                else:
                    year_vals.append(float(air_pollution[df_str].loc[(air_pollution[df_str]['Area'] == str(borough))]['PM25']))
            
            # Add row created to end of df
            borough_df.loc[len(borough_df)] = year_vals


        fig_col1, fig_col2 = st.columns((11,3),gap='medium')

        with fig_col1:
            st.markdown('##')
            # Line Graph of Attributes selected over time period selected
            st.markdown("### Time Series")
            # Convert df from wide to long format, drop empty rows
            borough_long_df = borough_df.melt('Date').dropna()
            line = alt.Chart(borough_long_df).mark_line().encode(
                x=alt.X('Date', scale=alt.Scale(zero=False)),
                y=alt.Y('value', axis=alt.Axis(labels=False)),
                color='variable',
            ).properties(
                width=1400,
                height=600
            ).configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            )
            line_plot = st.altair_chart(line, use_container_width=True)

            # Animate line chart, redraw whenever page reloaded
            # Loop to plot an extra row of the df each iteration
            for i in range(1, borough_long_df.shape[0]+1):
                temp_df = borough_long_df.iloc[0:i]
                line = alt.Chart(temp_df).mark_line().encode(
                    x=alt.X('Date', scale=alt.Scale(zero=False)),
                    y=alt.Y('value', axis=alt.Axis(labels=False)),
                    color='variable',
                ).properties(
                    width=1400,
                    height=600
                ).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )
                line_plot = line_plot.altair_chart(line, use_container_width=True)

        with fig_col2:
            df_str = 'df_' + str(dates[1])

            st.markdown(
                """
            <style>
            [data-testid="metric-container"] {
                background-color: rgba(28, 131, 150, 0.1);
                border: 1px solid rgba(28, 131, 150, 0.1);
                padding: 5% 5% 5% 10%;
                border-radius: 5px;
                color: rgb(30, 103, 119);
                overflow-wrap: break-word;
            }
            [data-testid="stMetricLabel"] {
                overflow-wrap: break-word;
                white-space: break-spaces;
                font-size: 20px;
            }
            [data-testid="stMetricValue"] {
                font-size: 40px;
            }
            [data-testid="stMetricDelta"] {
                font-size: 25px;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )

            if df_str != 'df_2020':
                fig_col2.metric(
                    label="Emergency Admissions vs 2003",
                    value=int(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == borough, 'EmergencyAdmissions']),
                    delta=str(round((int(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == borough, 'EmergencyAdmissions']) / int(e_admissions['df_2003'].loc[e_admissions['df_2003']['Area'] == borough, 'EmergencyAdmissions'])) * 100 - 100)) + '%'
                )

            fig_col2.metric(
                label="ACSC admissions vs 2003",
                value=int(df_acsc.loc[(df_acsc['Year'] == str(dates[1])) & (df_acsc['Area'] == borough) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed']),
                delta=str(round((int(df_acsc.loc[(df_acsc['Year'] == str(dates[1])) & (df_acsc['Area'] == borough) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed']) / int(df_acsc.loc[(df_acsc['Year'] == '2003') & (df_acsc['Area'] == borough) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed']))*100-100))+'%',
            )

            fig_col2.metric(
                label="Takeaways vs 2003",
                value=int(df_fastfood.loc[(df_fastfood['Area'] == borough)].head(1)[str(dates[1])]),
                delta=str(round((int(df_fastfood.loc[(df_fastfood['Area'] == borough)].head(1)[str(dates[1])]) / int(df_fastfood.loc[(df_fastfood['Area'] == borough)].head(1)['2003']))*100-100))+'%',
            )

            if int(dates[1]) > 2008:
                if int(dates[1]) not in no_air_vals:
                    fig_col2.metric(
                        label="PM25 emmissions (tonnes) vs 2008",
                        value=round(float(air_pollution[df_str].loc[(air_pollution[df_str]['Area'] == str(borough))]['PM25']),1),
                        delta=str(round((float(air_pollution[df_str].loc[air_pollution[df_str]['Area'] == str(borough)]['PM25']) / float(air_pollution['df_2008'].loc[air_pollution['df_2008']['Area'] == str(borough)]['PM25']))*100-100))+'%',
                    )


    with tab2:
        # Multiple Linear Regression
        # Get values for all attributes 2003-2019
        regression_df = borough_df.iloc[0:17]

        # Air Pollution values incomplete (contain nan values), calculate regression coefficient separately
        # Get Air Pollution independant variable
        regression_airp_x_df = regression_df.drop(['Date', 'Emergency Admissions/100', 'ACSC Admissions/10', 'Number of Takeaways'], axis=1)
        # Drop rows with nan values
        regression_airp_x_df = regression_airp_x_df.drop([0,1,2,3,4,6,8,11,14,15], axis=0)
        # Convert dataframe to numpy array
        airp_x = regression_airp_x_df.to_numpy()

        # Each element in y is e_admissions value for a year
        # Get dependent emergency admission variable
        regression_airp_y_df = regression_df.filter(['Emergency Admissions/100'], axis=1)
        # Drop rows with nan values
        regression_airp_y_df = regression_airp_y_df.drop([0,1,2,3,4,6,8,11,14,15], axis=0)
        # Convert dataframe to numpy array
        airp_y = regression_airp_y_df.to_numpy()

        # Fit model
        airp_model = LinearRegression().fit(airp_x, airp_y)
        # Use model to look at relationships between independent variables and emergency admissions
        # model.coef_ to get variable weights
        airp_coefficient = airp_model.coef_.tolist()
        airp_weight = 0
        for x in airp_coefficient:
            for y in x:
                airp_weight = y

        # Each element in x is the values of the independent variables for a year (all variables except date, emergency admissions and air pollution)
        # Get independent variables by borough_df
        regression_x_df = regression_df.drop(['Date', 'Emergency Admissions/100', 'PM2.5 Particulate Emissions (tonnes/year)'], axis=1)
        # Convert dataframe to numpy array
        x = regression_x_df.to_numpy()

        # Each element in y is e_admissions value for a year
        # Get dependent emergency admission variable
        regression_y_df = regression_df.filter(['Emergency Admissions/100'], axis=1)
        # Convert dataframe to numpy array
        y = regression_y_df.to_numpy()

        # Fit model
        model = LinearRegression().fit(x, y)

        # Use model to look at relationships between independent variables and emergency admissions
        # model.coef_ to get variable weights
        coefficients = model.coef_.tolist()
        weights = []
        for x in coefficients:
            for y in x:
                weights.append(y)
        weights.append(airp_weight)

        radar_df = pd.DataFrame(dict(
            r=weights,
            theta=['ACSC Admissions', 'Fast Food Prevalence', 'Air Pollution']))
        fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[0,1], width=800, height=600)
        fig.update_traces(fill='toself')
        fig.update_polars(bgcolor='white')
        fig.update_layout(polar_angularaxis_gridcolor="black")
        fig.update_layout(
            font=dict(
                family="Arial",
                size=22,
            )
        )
        st.markdown('##')
        st.markdown("### Linear Regression Relationship Weights")
        st.markdown('##')
        st.plotly_chart(fig, theme="None", use_container_width=True)



def main():
    london_boroughs = ['-', 'City of London', 'Westminster', 'Kensington and Chelsea', 'Hammersmith and Fulham', 
            'Wandsworth', 'Lambeth', 'Southwark', 'Tower Hamlets', 'Hackney', 'Islington', 'Camden', 'Brent', 'Ealing', 'Hounslow', 
            'Richmond upon Thames', 'Kingston upon Thames', 'Merton', 'Sutton', 'Croydon', 'Bromley', 'Lewisham', 'Greenwich', 'Bexley', 'Havering', 
            'Barking and Dagenham', 'Redbridge', 'Newham', 'Waltham Forest', 'Haringey', 'Enfield', 'Barnet', 'Harrow', 'Hillingdon']

    # Set webpage to a wide format to use width of screen, set sidebar be collapsed initially, set webpage title
    st.set_page_config(
        page_title='London Healthcare Dashboard',
        layout='wide',
        initial_sidebar_state='collapsed',
    )

    # Set sidebar to contain a selectbox where user can select a borough
    borough = st.sidebar.selectbox('Select Borough', london_boroughs)

    # If option selected is '-', display choropleth map, else display the individual data suite for the selected borough
    if len(str(borough)) == 1:
        intro()
    else:
        individual_data_suite(borough)




if __name__ == "__main__":
    main()