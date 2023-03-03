from sklearn.linear_model import LinearRegression
from scipy import stats
from streamlit_folium import st_folium
from statsmodels.tsa.seasonal import seasonal_decompose
import folium
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
            # Reformat Emergency Admissions column to integer
            e_admissions[df_str]['EmergencyAdmissions'] = e_admissions[df_str]['EmergencyAdmissions'].apply(lambda x: int(x))
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
# Monthly Emergency Admissions Datasets
# --------------------------------------------------
@st.cache
def monthly_emergency_admissions_data():
    monthly_admissions = {}
    monthly_admissions['df_JANUARY_2009'] = pd.read_csv('Data/MonthlyE-Admissions/January2009.csv')
    monthly_admissions['df_JANUARY_2010'] = pd.read_csv('Data/MonthlyE-Admissions/January2010.csv')
    monthly_admissions['df_JANUARY_2011'] = pd.read_csv('Data/MonthlyE-Admissions/January2011.csv')
    monthly_admissions['df_JANUARY_2012'] = pd.read_csv('Data/MonthlyE-Admissions/January2012.csv')
    monthly_admissions['df_JANUARY_2013'] = pd.read_csv('Data/MonthlyE-Admissions/January2013.csv')
    monthly_admissions['df_JANUARY_2020'] = pd.read_csv('Data/MonthlyE-Admissions/January2020.csv')
    monthly_admissions['df_JANUARY_2021'] = pd.read_csv('Data/MonthlyE-Admissions/January2021.csv')
    monthly_admissions['df_JANUARY_2022'] = pd.read_csv('Data/MonthlyE-Admissions/January2022.csv')
    monthly_admissions['df_JANUARY_2023'] = pd.read_csv('Data/MonthlyE-Admissions/January2023.csv')

    monthly_admissions['df_FEBRUARY_2009'] = pd.read_csv('Data/MonthlyE-Admissions/February2009.csv')
    monthly_admissions['df_FEBRUARY_2010'] = pd.read_csv('Data/MonthlyE-Admissions/February2010.csv')
    monthly_admissions['df_FEBRUARY_2011'] = pd.read_csv('Data/MonthlyE-Admissions/February2011.csv')
    monthly_admissions['df_FEBRUARY_2012'] = pd.read_csv('Data/MonthlyE-Admissions/February2012.csv')
    monthly_admissions['df_FEBRUARY_2013'] = pd.read_csv('Data/MonthlyE-Admissions/February2013.csv')
    monthly_admissions['df_FEBRUARY_2020'] = pd.read_csv('Data/MonthlyE-Admissions/February2020.csv')
    monthly_admissions['df_FEBRUARY_2021'] = pd.read_csv('Data/MonthlyE-Admissions/February2021.csv')
    monthly_admissions['df_FEBRUARY_2022'] = pd.read_csv('Data/MonthlyE-Admissions/February2022.csv')

    monthly_admissions['df_MARCH_2009'] = pd.read_csv('Data/MonthlyE-Admissions/March2009.csv')
    monthly_admissions['df_MARCH_2010'] = pd.read_csv('Data/MonthlyE-Admissions/March2010.csv')
    monthly_admissions['df_MARCH_2011'] = pd.read_csv('Data/MonthlyE-Admissions/March2011.csv')
    monthly_admissions['df_MARCH_2012'] = pd.read_csv('Data/MonthlyE-Admissions/March2012.csv')
    monthly_admissions['df_MARCH_2013'] = pd.read_csv('Data/MonthlyE-Admissions/March2013.csv')
    monthly_admissions['df_MARCH_2020'] = pd.read_csv('Data/MonthlyE-Admissions/March2020.csv')
    monthly_admissions['df_MARCH_2021'] = pd.read_csv('Data/MonthlyE-Admissions/March2021.csv')
    monthly_admissions['df_MARCH_2022'] = pd.read_csv('Data/MonthlyE-Admissions/March2022.csv')

    monthly_admissions['df_APRIL_2008'] = pd.read_csv('Data/MonthlyE-Admissions/April2008.csv')
    monthly_admissions['df_APRIL_2009'] = pd.read_csv('Data/MonthlyE-Admissions/April2009.csv')
    monthly_admissions['df_APRIL_2010'] = pd.read_csv('Data/MonthlyE-Admissions/April2010.csv')
    monthly_admissions['df_APRIL_2011'] = pd.read_csv('Data/MonthlyE-Admissions/April2011.csv')
    monthly_admissions['df_APRIL_2012'] = pd.read_csv('Data/MonthlyE-Admissions/April2012.csv')
    monthly_admissions['df_APRIL_2020'] = pd.read_csv('Data/MonthlyE-Admissions/April2020.csv')
    monthly_admissions['df_APRIL_2021'] = pd.read_csv('Data/MonthlyE-Admissions/April2021.csv')
    monthly_admissions['df_APRIL_2022'] = pd.read_csv('Data/MonthlyE-Admissions/April2022.csv')

    monthly_admissions['df_MAY_2008'] = pd.read_csv('Data/MonthlyE-Admissions/May2008.csv')
    monthly_admissions['df_MAY_2009'] = pd.read_csv('Data/MonthlyE-Admissions/May2009.csv')
    monthly_admissions['df_MAY_2010'] = pd.read_csv('Data/MonthlyE-Admissions/May2010.csv')
    monthly_admissions['df_MAY_2011'] = pd.read_csv('Data/MonthlyE-Admissions/May2011.csv')
    monthly_admissions['df_MAY_2012'] = pd.read_csv('Data/MonthlyE-Admissions/May2012.csv')
    monthly_admissions['df_MAY_2020'] = pd.read_csv('Data/MonthlyE-Admissions/May2020.csv')
    monthly_admissions['df_MAY_2021'] = pd.read_csv('Data/MonthlyE-Admissions/May2021.csv')
    monthly_admissions['df_MAY_2022'] = pd.read_csv('Data/MonthlyE-Admissions/May2022.csv')

    monthly_admissions['df_JUNE_2008'] = pd.read_csv('Data/MonthlyE-Admissions/June2008.csv')
    monthly_admissions['df_JUNE_2009'] = pd.read_csv('Data/MonthlyE-Admissions/June2009.csv')
    monthly_admissions['df_JUNE_2010'] = pd.read_csv('Data/MonthlyE-Admissions/June2010.csv')
    monthly_admissions['df_JUNE_2011'] = pd.read_csv('Data/MonthlyE-Admissions/June2011.csv')
    monthly_admissions['df_JUNE_2012'] = pd.read_csv('Data/MonthlyE-Admissions/June2012.csv')
    monthly_admissions['df_JUNE_2020'] = pd.read_csv('Data/MonthlyE-Admissions/June2020.csv')
    monthly_admissions['df_JUNE_2021'] = pd.read_csv('Data/MonthlyE-Admissions/June2021.csv')
    monthly_admissions['df_JUNE_2022'] = pd.read_csv('Data/MonthlyE-Admissions/June2022.csv')

    monthly_admissions['df_JULY_2008'] = pd.read_csv('Data/MonthlyE-Admissions/July2008.csv')
    monthly_admissions['df_JULY_2009'] = pd.read_csv('Data/MonthlyE-Admissions/July2009.csv')
    monthly_admissions['df_JULY_2010'] = pd.read_csv('Data/MonthlyE-Admissions/July2010.csv')
    monthly_admissions['df_JULY_2011'] = pd.read_csv('Data/MonthlyE-Admissions/July2011.csv')
    monthly_admissions['df_JULY_2012'] = pd.read_csv('Data/MonthlyE-Admissions/July2012.csv')
    monthly_admissions['df_JULY_2020'] = pd.read_csv('Data/MonthlyE-Admissions/July2020.csv')
    monthly_admissions['df_JULY_2021'] = pd.read_csv('Data/MonthlyE-Admissions/July2021.csv')
    monthly_admissions['df_JULY_2022'] = pd.read_csv('Data/MonthlyE-Admissions/July2022.csv')

    monthly_admissions['df_AUGUST_2008'] = pd.read_csv('Data/MonthlyE-Admissions/August2008.csv')
    monthly_admissions['df_AUGUST_2009'] = pd.read_csv('Data/MonthlyE-Admissions/August2009.csv')
    monthly_admissions['df_AUGUST_2010'] = pd.read_csv('Data/MonthlyE-Admissions/August2010.csv')
    monthly_admissions['df_AUGUST_2011'] = pd.read_csv('Data/MonthlyE-Admissions/August2011.csv')
    monthly_admissions['df_AUGUST_2012'] = pd.read_csv('Data/MonthlyE-Admissions/August2012.csv')
    monthly_admissions['df_AUGUST_2020'] = pd.read_csv('Data/MonthlyE-Admissions/August2020.csv')
    monthly_admissions['df_AUGUST_2021'] = pd.read_csv('Data/MonthlyE-Admissions/August2021.csv')
    monthly_admissions['df_AUGUST_2022'] = pd.read_csv('Data/MonthlyE-Admissions/August2022.csv')

    monthly_admissions['df_SEPTEMBER_2008'] = pd.read_csv('Data/MonthlyE-Admissions/September2008.csv')
    monthly_admissions['df_SEPTEMBER_2009'] = pd.read_csv('Data/MonthlyE-Admissions/September2009.csv')
    monthly_admissions['df_SEPTEMBER_2010'] = pd.read_csv('Data/MonthlyE-Admissions/September2010.csv')
    monthly_admissions['df_SEPTEMBER_2011'] = pd.read_csv('Data/MonthlyE-Admissions/September2011.csv')
    monthly_admissions['df_SEPTEMBER_2012'] = pd.read_csv('Data/MonthlyE-Admissions/September2012.csv')
    monthly_admissions['df_SEPTEMBER_2020'] = pd.read_csv('Data/MonthlyE-Admissions/September2020.csv')
    monthly_admissions['df_SEPTEMBER_2021'] = pd.read_csv('Data/MonthlyE-Admissions/September2021.csv')
    monthly_admissions['df_SEPTEMBER_2022'] = pd.read_csv('Data/MonthlyE-Admissions/September2022.csv')

    monthly_admissions['df_OCTOBER_2008'] = pd.read_csv('Data/MonthlyE-Admissions/October2008.csv')
    monthly_admissions['df_OCTOBER_2009'] = pd.read_csv('Data/MonthlyE-Admissions/October2009.csv')
    monthly_admissions['df_OCTOBER_2010'] = pd.read_csv('Data/MonthlyE-Admissions/October2010.csv')
    monthly_admissions['df_OCTOBER_2011'] = pd.read_csv('Data/MonthlyE-Admissions/October2011.csv')
    monthly_admissions['df_OCTOBER_2012'] = pd.read_csv('Data/MonthlyE-Admissions/October2012.csv')
    monthly_admissions['df_OCTOBER_2020'] = pd.read_csv('Data/MonthlyE-Admissions/October2020.csv')
    monthly_admissions['df_OCTOBER_2021'] = pd.read_csv('Data/MonthlyE-Admissions/October2021.csv')
    monthly_admissions['df_OCTOBER_2022'] = pd.read_csv('Data/MonthlyE-Admissions/October2022.csv')

    monthly_admissions['df_NOVEMBER_2008'] = pd.read_csv('Data/MonthlyE-Admissions/November2008.csv')
    monthly_admissions['df_NOVEMBER_2009'] = pd.read_csv('Data/MonthlyE-Admissions/November2009.csv')
    monthly_admissions['df_NOVEMBER_2010'] = pd.read_csv('Data/MonthlyE-Admissions/November2010.csv')
    monthly_admissions['df_NOVEMBER_2011'] = pd.read_csv('Data/MonthlyE-Admissions/November2011.csv')
    monthly_admissions['df_NOVEMBER_2012'] = pd.read_csv('Data/MonthlyE-Admissions/November2012.csv')
    monthly_admissions['df_NOVEMBER_2020'] = pd.read_csv('Data/MonthlyE-Admissions/November2020.csv')
    monthly_admissions['df_NOVEMBER_2021'] = pd.read_csv('Data/MonthlyE-Admissions/November2021.csv')
    monthly_admissions['df_NOVEMBER_2022'] = pd.read_csv('Data/MonthlyE-Admissions/November2022.csv')

    monthly_admissions['df_DECEMBER_2008'] = pd.read_csv('Data/MonthlyE-Admissions/December2008.csv')
    monthly_admissions['df_DECEMBER_2009'] = pd.read_csv('Data/MonthlyE-Admissions/December2009.csv')
    monthly_admissions['df_DECEMBER_2010'] = pd.read_csv('Data/MonthlyE-Admissions/December2010.csv')
    monthly_admissions['df_DECEMBER_2011'] = pd.read_csv('Data/MonthlyE-Admissions/December2011.csv')
    monthly_admissions['df_DECEMBER_2012'] = pd.read_csv('Data/MonthlyE-Admissions/December2012.csv')
    monthly_admissions['df_DECEMBER_2020'] = pd.read_csv('Data/MonthlyE-Admissions/December2020.csv')
    monthly_admissions['df_DECEMBER_2021'] = pd.read_csv('Data/MonthlyE-Admissions/December2021.csv')
    monthly_admissions['df_DECEMBER_2022'] = pd.read_csv('Data/MonthlyE-Admissions/December2022.csv')

    monthly_admissions['df_2013'] = pd.read_csv('Data/MonthlyE-Admissions/2013.csv')
    monthly_admissions['df_2014'] = pd.read_csv('Data/MonthlyE-Admissions/2014.csv')
    monthly_admissions['df_2015'] = pd.read_csv('Data/MonthlyE-Admissions/2015.csv')
    monthly_admissions['df_2016'] = pd.read_csv('Data/MonthlyE-Admissions/2016.csv')
    monthly_admissions['df_2017'] = pd.read_csv('Data/MonthlyE-Admissions/2017.csv')
    monthly_admissions['df_2018'] = pd.read_csv('Data/MonthlyE-Admissions/2018.csv')
    monthly_admissions['df_2019'] = pd.read_csv('Data/MonthlyE-Admissions/2019.csv')

    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

    # Transform 2013-2015 dataframes
    for i in range(2013,2016):
        df_str = 'df_' + str(i)
        # Drop all rows not under London Commissioning Region
        monthly_admissions[df_str] = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Commissioner Parent Name'] == 'LONDON COMMISSIONING REGION']
        # Drop unnecessary columns
        monthly_admissions[df_str] = monthly_admissions[df_str].drop(['Yearnumber', 'Provider Parent org code', 'Provider Org code', 'Provider Org name', 'Commissioner Parent Org Code', 'Commissioner Parent Name', 'Commissioner Org Code', 'A209 Ip Elect Ord SUM', 'A209 Ip Elect Day SUM', 'A209 Ip Elect Total SUM', 'A209 Ip Elecord Planned SUM', 'A209 Ip Elecday Planned SUM', 'A209 Ip Electotal Planned SUM', 'A209 Ip Elect Total Tc SUM', 'A262 Op Gprefsmade M SUM', 'A262 Op Gprefsseen M SUM', 'A262 Op Gprefsmade Ga M SUM', 'A262 Op Gprefsseen Ga M SUM', 'A262 Op Otherrefsmade Ga M SUM', 'A262 Op 1statt Ga M SUM', 'Description'], axis=1)
        monthly_admissions[df_str] = monthly_admissions[df_str].drop(monthly_admissions[df_str].columns[1], axis = 1)
        # Rename column headers
        monthly_admissions[df_str] = monthly_admissions[df_str].rename(columns={'Periodname': 'Period', 'Commissioner Org Name': 'Commissioner', 'A209 Ip Nonelect SUM': 'EmergencyAdmissions'})
        # Reformat 'Period' column to uppercase
        monthly_admissions[df_str]['Period'] = monthly_admissions[df_str]['Period'].str.upper()
        # Reformat 'Period' column to format 'month-year'
        monthly_admissions[df_str]['Period'] = monthly_admissions[df_str]['Period'] + '-' + str(i)
        monthly_admissions[df_str].loc[monthly_admissions[df_str]['Period'] == ('JANUARY' + '-' + str(i)), 'Period'] = ('JANUARY' + '-'+ str(i+1))
        monthly_admissions[df_str].loc[monthly_admissions[df_str]['Period'] == ('FEBRUARY' + '-' + str(i)), 'Period'] = ('FEBRUARY' + '-'+ str(i+1))
        monthly_admissions[df_str].loc[monthly_admissions[df_str]['Period'] == ('MARCH' + '-' + str(i)), 'Period'] = ('MARCH' + '-'+ str(i+1))

    # Transform 2016 dataframe
    # Drop all rows not under London Commissioning Region
    monthly_admissions['df_2016'] = monthly_admissions['df_2016'].loc[monthly_admissions['df_2016']['Commissioner Parent Org Code'] == 'Q71']
    # Drop unnecessary columns
    monthly_admissions['df_2016'] = monthly_admissions['df_2016'].drop(['Yearnumber', 'Provider Parent org code', 'Provider Org code', 'Provider Org name', 'Commissioner Parent Org Code', 'Commissioner Parent Name', 'Commissioner Org Code', 'Ip Elect Ord', 'Ip Elect Day', 'Ip Elect Total', 'Ip Elecord Planned', 'Ip Elecday Planned', 'Ip Electotal Planned', 'Ip Elect Total Tc', 'Op Gprefsmade M', 'Op Gprefsseen M', 'Op Gprefsmade Ga M', 'Op Gprefsseen Ga M', 'Op Otherrefsmade Ga M', 'Op 1statt Ga M'], axis=1)
    monthly_admissions['df_2016'] = monthly_admissions['df_2016'].drop(monthly_admissions['df_2016'].columns[1], axis = 1)
    # Rename column headers
    monthly_admissions['df_2016'] = monthly_admissions['df_2016'].rename(columns={'Periodname': 'Period', 'Commissioner Org Name': 'Commissioner', 'Ip Nonelect': 'EmergencyAdmissions'})
    # Reformat 'Period' column to uppercase
    monthly_admissions['df_2016']['Period'] = monthly_admissions['df_2016']['Period'].str.upper()
    # Reformat 'Period' column to format 'month-year'
    monthly_admissions['df_2016']['Period'] = monthly_admissions['df_2016']['Period'] + '-2016'
    monthly_admissions['df_2016'].loc[monthly_admissions['df_2016']['Period'] == ('JANUARY' + '-2016'), 'Period'] = ('JANUARY' + '-2017')
    monthly_admissions['df_2016'].loc[monthly_admissions['df_2016']['Period'] == ('FEBRUARY' + '-2016'), 'Period'] = ('FEBRUARY' + '-2017')
    monthly_admissions['df_2016'].loc[monthly_admissions['df_2016']['Period'] == ('MARCH' + '-2016'), 'Period'] = ('MARCH' + '-2017')

    # Transform 2017-2019 dataframes
    for i in range(2017,2020):
        df_str = 'df_' + str(i)
        # Drop all rows not under London Commissioning Region
        monthly_admissions[df_str] = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Commissioner Parent Org Code'] == 'Q71']
        # Drop unnecessary columns
        monthly_admissions[df_str] = monthly_admissions[df_str].drop(['Provider Parent org code', 'Provider Org code', 'Provider Org name', 'Commissioner Parent Org Code', 'Commissioner Org Code', 'Ip Elect Ord', 'Ip Elect Day', 'Ip Elect Total', 'Ip Elecord Planned', 'Ip Elecday Planned', 'Ip Electotal Planned', 'Ip Elect Total Tc', 'Op Gprefsmade M', 'Op Gprefsseen M', 'Op Gprefsmade Ga M', 'Op Gprefsseen Ga M', 'Op Otherrefsmade Ga M', 'Op 1statt Ga M'], axis=1)
        monthly_admissions[df_str] = monthly_admissions[df_str].drop(monthly_admissions[df_str].columns[1], axis = 1)
        # Rename column headers
        monthly_admissions[df_str] = monthly_admissions[df_str].rename(columns={'Periodname': 'Period', 'Commissioner Org Name': 'Commissioner', 'Ip Nonelect': 'EmergencyAdmissions'})
        # Reformat 'Period' column to uppercase
        monthly_admissions[df_str]['Period'] = monthly_admissions[df_str]['Period'].str.upper()
        # Reformat 'Period' column to format 'month-year'
        monthly_admissions[df_str]['Period'] = monthly_admissions[df_str]['Period'].str[4:]

    # Transform 2020-2023 dataframes
    for i in range(2020, 2024):
        for month in months:
            # No more data past Jan 2023
            if i == 2023 and month != 'JANUARY':
                break
            df_str = 'df_' + str(month) + '_' + str(i)
            # Combine/sum column values for 'Emergency admissions via A&E - Type 1', 'Emergency admissions via A&E - Type 2', 'Emergency admissions via A&E - Other A&E department', 'Other emergency admissions' columns
            monthly_admissions[df_str]['Other emergency admissions'] = monthly_admissions[df_str]['Other emergency admissions'] + monthly_admissions[df_str]['Emergency admissions via A&E - Type 1'] + monthly_admissions[df_str]['Emergency admissions via A&E - Type 2'] + monthly_admissions[df_str]['Emergency admissions via A&E - Other A&E department']
            # Drop unnecessary columns
            monthly_admissions[df_str] = monthly_admissions[df_str].drop(monthly_admissions[df_str].columns[[1,3,4,5,6,7,8,9,10,11,12,13,14]], axis=1)
            # Rename column headers
            monthly_admissions[df_str] = monthly_admissions[df_str].rename(columns={'Other emergency admissions': 'EmergencyAdmissions'})

    # Create new dataframe holding dates and total admissions
    newdf = pd.DataFrame(columns=['Date', 'EmergencyAdmissions'])

    # Add monthly admissions from 2008
    for month in months:
        if month == 'JANUARY' or month == 'FEBRUARY' or month == 'MARCH':
            continue
        df_str = 'df_' + str(month) + '_2008'
        date_str = str(month) + '-2008'
        london_admissions = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Org Name'] == 'LONDON STRATEGIC HEALTH AUTHORITY', 'Total Non-elective G&A Admissions (FFCEs)'].sum()
        newdf.loc[len(newdf)] = [date_str, london_admissions]

    # Add monthly admissions from 2009-2011
    for year in range(2009,2012):
        for month in months:
            df_str = 'df_' + str(month) + '_' + str(year)
            date_str = str(month) + '-' + str(year)
            london_admissions = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Org Name'] == 'LONDON STRATEGIC HEALTH AUTHORITY', 'Total Non-elective G&A Admissions (FFCEs)'].sum()
            newdf.loc[len(newdf)] = [date_str, london_admissions]

    # Add monthly admissions for Jan 2012 - Mar 2012
    for month in months:
        if month == 'JANUARY' or month == 'FEBRUARY' or month == 'MARCH':
            df_str = 'df_' + str(month) + '_2012'
            date_str = str(month) + '-2012'
            london_admissions = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Org Name'] == 'LONDON STRATEGIC HEALTH AUTHORITY', 'Total Non-elective G&A Admissions (FFCEs)'].sum()
            newdf.loc[len(newdf)] = [date_str, london_admissions]

    # Add monthly admissions for Apr 2012 - Mar 2013
    for month in months:
        if month == 'JANUARY' or month == 'FEBRUARY' or month == 'MARCH':
            df_str = 'df_' + str(month) + '_2013'
            date_str = str(month) + '-2013'
        else:
            df_str = 'df_' + str(month) + '_2012'
            date_str = str(month) + '-2012'
        london_admissions = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Unnamed: 4'] == 'LONDON STRATEGIC HEALTH AUTHORITY', 'Unnamed: 12'].sum()
        newdf.loc[len(newdf)] = [date_str, london_admissions]

    # Add monthly admissions from 2013-2015
    for i in range (2013,2016):
        df_str = 'df_' + str(i)
        for month in months:
            if month == 'JANUARY' or month == 'FEBRUARY' or month == 'MARCH':
                month_str = month + '-' + str(i+1)
            else:
                month_str = month + '-' + str(i)
            london_admissions = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Period'] == month_str, 'EmergencyAdmissions'].sum()
            newdf.loc[len(newdf)] = [month_str, london_admissions]

    # Add monthly admissions from 2016
    for month in months:
        if month == 'JANUARY' or month == 'FEBRUARY' or month == 'MARCH':
            month_str = month + '-2017'
        else:
            month_str = month + '-2016'
        london_admissions = monthly_admissions['df_2016'].loc[monthly_admissions['df_2016']['Period'] == month_str, 'EmergencyAdmissions'].sum()
        newdf.loc[len(newdf)] = [month_str, london_admissions]

    # Add monthly admissions from 2017-2019
    for i in range (2017,2020):
        df_str = 'df_' + str(i)
        for month in months:
            if month == 'JANUARY' or month == 'FEBRUARY' or month == 'MARCH':
                month_str = month + '-' + str(i+1)
            else:
                month_str = month + '-' + str(i)
            london_admissions = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Period'] == month_str, 'EmergencyAdmissions'].sum()
            newdf.loc[len(newdf)] = [month_str, london_admissions]

    # Add monthly admissions from 2020-2023
    for year in range(2020,2024):
        for month in months:
            # No more data past Jan 2023
            if year == 2023 and month != 'JANUARY':
                break
            df_str = 'df_' + str(month) + '_' + str(year)
            date_str = str(month) + '-' + str(year)
            london_admissions = monthly_admissions[df_str].loc[monthly_admissions[df_str]['Parent Org'] == 'NHS ENGLAND LONDON', 'EmergencyAdmissions'].sum()
            newdf.loc[len(newdf)] = [date_str, london_admissions]


    # Reformat 'Date' column to 'datetime'
    newdf['Date'] = pd.to_datetime(newdf['Date'])
    # Sort dataframe by 'Date
    newdf = newdf.sort_values(by=['Date'])
    # Reformat 'EmergencyAdmissions' column to integer
    newdf = newdf.replace(',', '', regex=True)
    # Remove rows for which value is 0 (empty rows)
    newdf = newdf[newdf.EmergencyAdmissions != 0]
    newdf['EmergencyAdmissions'] = newdf['EmergencyAdmissions'].apply(lambda x: int(x))
    # Reset dataframe index
    newdf = newdf.reset_index(drop=True)


    return newdf




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
    # drop unnecessary columns
    air_pollution['df_2008'] = air_pollution['df_2008'][['Area', 'PM25']]

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
    # drop unnecessary columns
    air_pollution['df_2010'] = air_pollution['df_2010'][['Area', 'PM25']]

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
    # drop unnecessary columns
    air_pollution['df_2012'] = air_pollution['df_2012'][['Area', 'PM25']]

    air_pollution['df_2013'] = pd.read_csv('Data/AirPollution/PM2.5 Totals by Borough2013.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2013'] = air_pollution['df_2013'].rename({'PM2.5 Pivot Table by Borough': 'Area', 'Unnamed: 13': 'PM25'}, axis='columns')
    air_pollution['df_2013']['PM25'] = air_pollution['df_2013']['PM25'].str.replace('\t', '')
    # Reformat outlier Borough names
    air_pollution['df_2013'].loc[air_pollution['df_2013']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2013'].loc[air_pollution['df_2013']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2013'].loc[air_pollution['df_2013']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2013'].loc[air_pollution['df_2013']['Area'] == 'City', 'Area'] = 'City of London'
    # drop unnecessary columns
    air_pollution['df_2013'] = air_pollution['df_2013'][['Area', 'PM25']]

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
    # drop unnecessary columns
    air_pollution['df_2015'] = air_pollution['df_2015'][['Area', 'PM25']]

    air_pollution['df_2016'] = pd.read_csv('Data/AirPollution/PM2.5 Summary2016.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2016'] = air_pollution['df_2016'].transpose()
    air_pollution['df_2016'] = air_pollution['df_2016'].rename({6: 'Area', 68: 'PM25'}, axis='columns')
    air_pollution['df_2016']['PM25'] = air_pollution['df_2016']['PM25'].str.replace('\t', '')
    # Reformat outlier Borough names
    air_pollution['df_2016'].loc[air_pollution['df_2016']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2016'].loc[air_pollution['df_2016']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2016'].loc[air_pollution['df_2016']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2016'].loc[air_pollution['df_2016']['Area'] == 'City', 'Area'] = 'City of London'
    # drop unnecessary columns
    air_pollution['df_2016'] = air_pollution['df_2016'][['Area', 'PM25']]

    air_pollution['df_2019'] = pd.read_csv('Data/AirPollution/PM2.5 Summary2019.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2019'] = air_pollution['df_2019'].transpose()
    air_pollution['df_2019'] = air_pollution['df_2019'].rename({6: 'Area', 71: 'PM25'}, axis='columns')
    air_pollution['df_2019']['PM25'] = air_pollution['df_2019']['PM25'].str.replace('\t', '')
    # Reformat outlier Borough names
    air_pollution['df_2019'].loc[air_pollution['df_2019']['Area'] == 'City of Westminster', 'Area'] = 'Westminster'
    air_pollution['df_2019'].loc[air_pollution['df_2019']['Area'] == 'Richmond', 'Area'] = 'Richmond upon Thames'
    air_pollution['df_2019'].loc[air_pollution['df_2019']['Area'] == 'Kingston', 'Area'] = 'Kingston upon Thames'
    air_pollution['df_2019'].loc[air_pollution['df_2019']['Area'] == 'City', 'Area'] = 'City of London'
    # drop unnecessary columns
    air_pollution['df_2019'] = air_pollution['df_2019'][['Area', 'PM25']]

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
    # drop unnecessary columns
    air_pollution['df_2020'] = air_pollution['df_2020'][['Area', 'PM25']]


    return air_pollution




# --------------------------------------------------
# Dashboard
# --------------------------------------------------

def intro():
    st.title('London Healthcare Dashboard')

    # Get transformed dataframes from streamlit cache
    e_admissions = emergency_admissions_data()
    monthly_admissions = monthly_emergency_admissions_data()

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

    tab1, tab2 = st.tabs(["Geographical", "Time Series"])

    with tab1:
        # Date slider widget
        year = st.slider('Select a range of values', 2003, 2020, 2003)
        df_str = 'df_' + str(year)

        if str(year) == '2020':
            st.write('*Note: from 2020 onwards NHS "Hospital Admitted Patient Care Activity" groups CCG data for many boroughs together, therefore the data is incomplete at an individual borough level*')

        map_df = e_admissions[df_str].copy()
        columnsused = ['Area', 'EmergencyAdmissions']

        fig_col1, fig_col2 = st.columns((5,9), gap='large')

        with fig_col1:
            new_df = e_admissions[df_str][['Area', 'EmergencyAdmissions']]
            bars = alt.Chart(new_df).mark_bar(size=16).encode(
                x=alt.X('EmergencyAdmissions:Q', scale=alt.Scale(domain=(0, 45000)),title=''),
                y=alt.Y('Area', sort='-x', title='')
            ).properties(
                width=900,
                height=850
            ).configure_axis(
                grid=False,
                labelFontSize=16,
            ).configure_view(
                strokeWidth=0
            )
            st.altair_chart(bars, use_container_width=True)

        with fig_col2:
            map = folium.Map(location=[51.5, 0], zoom_start=10, tiles='cartodbpositron')
            choropleth = folium.Choropleth(
                geo_data = 'Data/london_boroughs.json',
                data = map_df,
                columns = columnsused,
                key_on = 'feature.properties.name',
                fill_color="PuBu",
                fill_opacity=0.8,
                line_opacity = 0.7,
                highlight=True
            )
            choropleth.geojson.add_to(map)

            for feature in choropleth.geojson.data['features']:
                borough = feature['properties']['name']
                try:
                    feature['properties']['area_hectares'] = 'Emergency Admissions: ' + str(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == borough, 'EmergencyAdmissions'].iloc[0])
                except:
                    feature['properties']['area_hectares'] = 'Emergency Admissions: n/a'
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(fields=['name', 'area_hectares'], labels=False)
            )
            st_map = st_folium(map, width=1200, height=750)

            # borough_selected = ''
            # if st_map['last_active_drawing']:
            #     borough_selected = st_map['last_active_drawing']['properties']['name']
            #     # individual_data_suite(borough_selected)

    with tab2:
        st.markdown('### London Monthly Time Series-Emergency Admissions')

        line = alt.Chart(monthly_admissions.reset_index()).mark_line().encode(
            x=alt.X('Date',scale=alt.Scale(zero=False)),
            y=alt.Y('EmergencyAdmissions',scale=alt.Scale(zero=False)),
        )
        rule = alt.Chart(
            pd.DataFrame({
                'Date': ['2020-02-01'],
                'color': ['red'],
                'event': ['Beginning of Covid Epidemic UK']
            })
        ).mark_rule(
            strokeWidth=2,
            strokeDash=[10, 8]
        ).encode(
            x='Date:T',
            color=alt.Color('color:N', scale=None),
            tooltip=['event'],
        )
        
        line = alt.layer(
            line, rule
        ).properties(
            height=800
        ).configure_axis(
            grid=False
        )
        line_plot = st.altair_chart(line, use_container_width=True)


        st.markdown('###')
        st.markdown('### Emergency Admissions Seasonality')
        st.markdown('###')
        fig_col1, fig_col2 = st.columns((5,3), gap='large')

        with fig_col1:
            seasonal = monthly_admissions.copy()
            seasonal.set_index('Date', inplace=True)
            result = seasonal_decompose(seasonal, model='additive', period=12)
            result = result.plot()
            st.pyplot(result)
        with fig_col2:
            st.write('"Trend" reflects overall trend of data')
            st.write('"Seasonal" reflects seasonality of data')
            st.write('"Residual" reflects noise/random variation in data')




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

    tab1, tab2 = st.tabs(["Time Series", "Regressions/Correlations"])

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
        fig_col1, fig_col2 = st.columns((1,1),gap='medium')
        # Get values for all attributes 2003-2019
        regression_df = pd.DataFrame(columns=['Date', 'Emergency Admissions', 'Ambulatory Care Sensitive Condition Admissions', 'Fast Food Prevalence', 'Particulate Emissions'])
        # Create rows with attribute values for each year
        for i in range(2003, 2020):
            year_vals = [str(i)]
            df_str = 'df_' + str(i)
            year_vals.append(float(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == str(borough), 'EmergencyAdmissions']))
            df_str = str(i)
            year_vals.append(float(df_acsc.loc[(df_acsc['Year'] == df_str) & (df_acsc['Area'] == str(borough)) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed']))
            year_vals.append(float(df_fastfood.loc[(df_fastfood['Area'] == str(borough))].head(1)[df_str]))
            df_str = 'df_' + str(i)
            if i in no_air_vals:
                year_vals.append(np.nan)
            else:
                year_vals.append(float(air_pollution[df_str].loc[(air_pollution[df_str]['Area'] == str(borough))]['PM25']))
            # Add row created to end of df
            regression_df.loc[len(regression_df)] = year_vals

        with fig_col1:
            st.markdown('###')
            st.write('Linear Regression Weights give the steepness of the relationship between variables')
            st.write('How Strong is the effect of the relationship')
            # Multiple Linear Regression

            # Air Pollution values incomplete (contain nan values), calculate regression coefficient separately
            # Get Air Pollution independant variable
            regression_airp_x_df = regression_df.drop(['Date', 'Emergency Admissions', 'Ambulatory Care Sensitive Condition Admissions', 'Fast Food Prevalence'], axis=1)
            # Drop rows with nan values
            regression_airp_x_df = regression_airp_x_df.drop([0,1,2,3,4,6,8,11,14,15], axis=0)
            # Convert dataframe to numpy array
            airp_x = regression_airp_x_df.to_numpy()

            # Each element in y is e_admissions value for a year
            # Get dependent emergency admission variable
            regression_airp_y_df = regression_df.filter(['Emergency Admissions'], axis=1)
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
            regression_x_df = regression_df.drop(['Date', 'Emergency Admissions', 'Particulate Emissions'], axis=1)
            # Convert dataframe to numpy array
            x = regression_x_df.to_numpy()

            # Each element in y is e_admissions value for a year
            # Get dependent emergency admission variable
            regression_y_df = regression_df.filter(['Emergency Admissions'], axis=1)
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
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, width=800, height=600)
            # fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[0,1], width=800, height=600)
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

        with fig_col2:
            st.markdown('###')
            st.write('Pearson correlation coefficient measures strength and direction of two variables\' linear relationship')
            st.write('How strong is the relationship itself')
            # Pearson Correlation Coefficients

            correlations = []
            correlations.append(stats.pearsonr(regression_df['Emergency Admissions'], regression_df['Ambulatory Care Sensitive Condition Admissions'])[0])
            correlations.append(stats.pearsonr(regression_df['Emergency Admissions'], regression_df['Fast Food Prevalence'])[0])

            air_pollution_corr = regression_df.drop([0,1,2,3,4,6,8,11,14,15], axis=0)
            correlations.append(stats.pearsonr(air_pollution_corr['Emergency Admissions'], air_pollution_corr['Particulate Emissions'])[0])

            radar_df = pd.DataFrame(dict(
                r=correlations,
                theta=['ACSC Admissions', 'Fast Food Prevalence', 'Air Pollution']))
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, width=800, height=600)
            # fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[0,1], width=800, height=600)
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
            st.markdown("### Pearson Correlation Coefficients")
            st.markdown('##')
            st.plotly_chart(fig, theme="None", use_container_width=True)




# --------------------------------------------------
# Borough Cluster Data Suite
# --------------------------------------------------

def cluster_data_suite(cluster):
    # Set page title to borough being viewed
    st.title(str(cluster))

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

    boroughs = cluster.split(', ')

    tab1, tab2 = st.tabs(["Time Series", "Regressions/Correlations"])

    with tab1:
        # Date slider widget from 2003-2020
        dates = st.slider('Select a range of values',2003, 2020, (2003, 2020))
        # Attributes option select
        attribute = st.selectbox('Select attributes', ['Emergency Admissions', 'Ambulatory Care Sensitive Condition Admissions', 'Fast Food Prevalence', 'Particulate Emissions'])
        
        # Add 'Date' in order to create 'Date' column in dataframe
        headers = boroughs.copy()
        headers.insert(0, 'Date')
        # Use 'date' and list of boroughs in cluster to create df
        cluster_df = pd.DataFrame(columns=headers)

        # List of years for which there is no air pollution data available
        no_air_vals = [2003,2004,2005,2006,2007,2009,2011,2014,2017,2018]

        # Create rows with attribute values for each year in range
        for i in range(dates[0], dates[1]+1):
            year_vals = [str(i)]
            df_str = 'df_' + str(i)
            if str(attribute) == 'Emergency Admissions':
                # NHS data incomplete for 2020
                if i == 2020 and cluster not in ['Barking and Dagenham, Havering, Redbridge']:
                    for borough in boroughs:
                        year_vals.append(np.nan)
                else:
                    for borough in boroughs:
                        year_vals.append(float(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == str(borough), 'EmergencyAdmissions'])/100)
            elif str(attribute) == 'Ambulatory Care Sensitive Condition Admissions':
                df_str = str(i)
                for borough in boroughs:
                    year_vals.append(float(df_acsc.loc[(df_acsc['Year'] == df_str) & (df_acsc['Area'] == str(borough)) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed'])/10)
            elif str(attribute) == 'Fast Food Prevalence':
                df_str = str(i)
                for borough in boroughs:
                    year_vals.append(float(df_fastfood.loc[(df_fastfood['Area'] == str(borough))].head(1)[df_str]))
            elif str(attribute) == 'Particulate Emissions':
                df_str = 'df_' + str(i)
                if i in no_air_vals:
                    for borough in boroughs:
                        year_vals.append(np.nan)
                else:
                    total = 0
                    for borough in boroughs:
                        year_vals.append(float(air_pollution[df_str].loc[(air_pollution[df_str]['Area'] == str(borough))]['PM25']))
            
            # Add row created to end of df
            cluster_df.loc[len(cluster_df)] = year_vals


        fig_col1, fig_col2 = st.columns((11,3),gap='medium')

        with fig_col1:
            st.markdown('##')
            # Line Graph of Attributes selected over time period selected
            st.markdown("### Time Series")
            # Convert df from wide to long format, drop empty rows
            cluster_long_df = cluster_df.melt('Date').dropna()
            line = alt.Chart(cluster_long_df).mark_line().encode(
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
            for i in range(1, cluster_long_df.shape[0]+1):
                temp_df = cluster_long_df.iloc[0:i]
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
            st.markdown('##')

            for borough in boroughs:
                if str(attribute) == 'Emergency Admissions':
                    if df_str != 'df_2020':
                        fig_col2.metric(
                            label=str(borough) + ' vs 2003',
                            value=int(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == borough, 'EmergencyAdmissions']),
                            delta=str(round((int(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == borough, 'EmergencyAdmissions']) / int(e_admissions['df_2003'].loc[e_admissions['df_2003']['Area'] == borough, 'EmergencyAdmissions']))*100-100)) + '%'
                        )
                        st.markdown('###')
                elif str(attribute) == 'Ambulatory Care Sensitive Admissions':
                    fig_col2.metric(
                        label=str(borough) + ' vs 2003',
                        value=int(df_acsc.loc[(df_acsc['Year'] == str(dates[1])) & (df_acsc['Area'] == borough) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed']),
                        delta=str(round((int(df_acsc.loc[(df_acsc['Year'] == str(dates[1])) & (df_acsc['Area'] == borough) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed']) / int(df_acsc.loc[(df_acsc['Year'] == '2003') & (df_acsc['Area'] == borough) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed']))*100-100)) + '%',
                    )
                    st.markdown('###')
                elif str(attribute) == 'Particulate Emissions':
                    if int(dates[1]) not in no_air_vals:
                        fig_col2.metric(
                            label=str(borough) + ' vs 2008',
                            value=str(round(float(air_pollution[df_str].loc[(air_pollution[df_str]['Area'] == str(borough))]['PM25']),1)) + ' tonnes',
                            delta=str(round((round(float(air_pollution[df_str].loc[(air_pollution[df_str]['Area'] == str(borough))]['PM25']),1) / float(air_pollution['df_2008'].loc[air_pollution['df_2008']['Area'] == str(borough)]['PM25']))*100-100)) + '%',
                        )
                        st.markdown('###')
                elif str(attribute) == 'Fast Food Prevalence':
                    fig_col2.metric(
                        label=str(borough) + ' vs 2003',
                        value=int(df_fastfood.loc[(df_fastfood['Area'] == borough)].head(1)[str(dates[1])]),
                        delta=str(round((int(df_fastfood.loc[(df_fastfood['Area'] == borough)].head(1)[str(dates[1])]) / int(df_fastfood.loc[(df_fastfood['Area'] == borough)].head(1)['2003']))*100-100)) + '%',
                    )
                    st.markdown('###')


    with tab2:
        fig_col1, fig_col2 = st.columns((1,1),gap='medium')
        # Get total cluster values for all attributes 2003-2019
        regression_df = pd.DataFrame(columns=['Date', 'Emergency Admissions', 'Ambulatory Care Sensitive Condition Admissions', 'Fast Food Prevalence', 'Particulate Emissions'])
        # Create rows with attribute values for each year
        for i in range(2003, 2020):
            year_vals = [str(i)]
            df_str = 'df_' + str(i)
            total = 0
            for borough in boroughs:
                total += float(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == str(borough), 'EmergencyAdmissions'])/100
            year_vals.append(total)
            df_str = str(i)
            total = 0
            for borough in boroughs:
                total += float(df_acsc.loc[(df_acsc['Year'] == df_str) & (df_acsc['Area'] == str(borough)) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed'])
            year_vals.append(total)
            total = 0
            for borough in boroughs:
                total += float(df_fastfood.loc[(df_fastfood['Area'] == str(borough))].head(1)[df_str])
            year_vals.append(total)
            df_str = 'df_' + str(i)
            if i in no_air_vals:
                year_vals.append(np.nan)
            else:
                total = 0
                for borough in boroughs:
                    total += float(air_pollution[df_str].loc[(air_pollution[df_str]['Area'] == str(borough))]['PM25'])
                year_vals.append(total)
            # Add row created to end of df
            regression_df.loc[len(regression_df)] = year_vals

        with fig_col1:
            st.markdown('###')
            st.write('Linear Regression Weights give the steepness of the relationship between variables')
            st.write('How Strong is the effect of the relationship')
            # Multiple Linear Regression

            # Air Pollution values incomplete (contain nan values), calculate regression coefficient separately
            # Get Air Pollution independant variable
            regression_airp_x_df = regression_df.drop(['Date', 'Emergency Admissions', 'Ambulatory Care Sensitive Condition Admissions', 'Fast Food Prevalence'], axis=1)
            # Drop rows with nan values
            regression_airp_x_df = regression_airp_x_df.drop([0,1,2,3,4,6,8,11,14,15], axis=0)
            # Convert dataframe to numpy array
            airp_x = regression_airp_x_df.to_numpy()

            # Each element in y is e_admissions value for a year
            # Get dependent emergency admission variable
            regression_airp_y_df = regression_df.filter(['Emergency Admissions'], axis=1)
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
            regression_x_df = regression_df.drop(['Date', 'Emergency Admissions', 'Particulate Emissions'], axis=1)
            # Convert dataframe to numpy array
            x = regression_x_df.to_numpy()

            # Each element in y is e_admissions value for a year
            # Get dependent emergency admission variable
            regression_y_df = regression_df.filter(['Emergency Admissions'], axis=1)
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
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, width=800, height=600)
            # fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[0,1], width=800, height=600)
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

        with fig_col2:
            st.markdown('###')
            st.write('Pearson correlation coefficient measures strength and direction of two variables\' linear relationship')
            st.write('How strong is the relationship itself')
            # Pearson Correlation Coefficients

            correlations = []
            correlations.append(stats.pearsonr(regression_df['Emergency Admissions'], regression_df['Ambulatory Care Sensitive Condition Admissions'])[0])
            correlations.append(stats.pearsonr(regression_df['Emergency Admissions'], regression_df['Fast Food Prevalence'])[0])

            air_pollution_corr = regression_df.drop([0,1,2,3,4,6,8,11,14,15], axis=0)
            correlations.append(stats.pearsonr(air_pollution_corr['Emergency Admissions'], air_pollution_corr['Particulate Emissions'])[0])

            radar_df = pd.DataFrame(dict(
                r=correlations,
                theta=['ACSC Admissions', 'Fast Food Prevalence', 'Air Pollution']))
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, width=800, height=600)
            # fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[0,1], width=800, height=600)
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
            st.markdown("### Pearson Correlation Coefficients")
            st.markdown('##')
            st.plotly_chart(fig, theme="None", use_container_width=True)



def main():
    london_boroughs = ['-', 'City of London', 'Westminster', 'Kensington and Chelsea', 'Hammersmith and Fulham', 
            'Wandsworth', 'Lambeth', 'Southwark', 'Tower Hamlets', 'Hackney', 'Islington', 'Camden', 'Brent', 'Ealing', 'Hounslow', 
            'Richmond upon Thames', 'Kingston upon Thames', 'Merton', 'Sutton', 'Croydon', 'Bromley', 'Lewisham', 'Greenwich', 'Bexley', 'Havering', 
            'Barking and Dagenham', 'Redbridge', 'Newham', 'Waltham Forest', 'Haringey', 'Enfield', 'Barnet', 'Harrow', 'Hillingdon']

    borough_clusters = ['-', 'Barking and Dagenham, Havering, Redbridge']

    # Set webpage to a wide format to use width of screen, set sidebar be collapsed initially, set webpage title
    st.set_page_config(
        page_title='London Healthcare Dashboard',
        layout='wide',
        initial_sidebar_state='collapsed',
    )

    # Set sidebar to contain a selectbox where user can select a borough
    borough = st.sidebar.selectbox('Select Borough', london_boroughs)

    cluster = st.sidebar.selectbox('Select Borough Cluster', borough_clusters)

    # If option selected is '-' and no cluster selected, display choropleth map, else display the data suite for the selected borough or cluster
    if len(str(borough)) == 1:
        if len(str(cluster)) == 1:
            intro()
        else:
            cluster_data_suite(cluster)
    else:
        individual_data_suite(borough)




if __name__ == "__main__":
    main()