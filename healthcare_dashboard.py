import numpy as np
import pandas as pd
import streamlit as st


# --------------------------------------------------
# Emergency Admissions Datasets
# --------------------------------------------------
@st.cache
def emergency_admissions_data():
    e_admissions = {}

    e_admissions['df_2003'] = pd.read_csv('Data/E-admissions/2003-04-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2004'] = pd.read_csv('Data/E-admissions/2004-05-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2005'] = pd.read_csv('Data/E-admissions/2005-06-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2006'] = pd.read_csv('Data/E-admissions/2006-07-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2007'] = pd.read_csv('Data/E-admissions/2007-08-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2008'] = pd.read_csv('Data/E-admissions/2008-09-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2009'] = pd.read_csv('Data/E-admissions/2009-10-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2010'] = pd.read_csv('Data/E-admissions/2010-11-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2011'] = pd.read_csv('Data/E-admissions/2011-12-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2012'] = pd.read_csv('Data/E-admissions/2012-13-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2013'] = pd.read_csv('Data/E-admissions/2013-14-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2014'] = pd.read_csv('Data/E-admissions/2014-15-Table 1.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2015'] = pd.read_csv('Data/E-admissions/hosp-epis-stat-admi-hosp-prov-2015-16.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2016'] = pd.read_csv('Data/E-admissions/hosp-epis-stat-admi-hosp-prov-2016-17.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2017'] = pd.read_csv('Data/E-admissions/hosp-epis-stat-admi-prov-2017-18.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2018'] = pd.read_csv('Data/E-admissions/hosp-epis-stat-admi-prov-2018-19.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2019'] = pd.read_csv('Data/E-admissions/hosp-epis-stat-admi-prov-2019-20.csv', dtype=str, keep_default_na=False)
    e_admissions['df_2020'] = pd.read_csv('Data/E-admissions/2020-21-Table A.csv', dtype=str, keep_default_na=False)

    for i in range(2003,2015):
        # Rename column for Emergency Admissions
        df_str = 'df_' + str(i)
        e_admissions[df_str] = e_admissions[df_str].rename({'Number of Admission Continuous Inpatient Spells - Numerator': 'EmergencyAdmissions'}, axis='columns')
        e_admissions[df_str].drop(e_admissions[df_str].tail(30).index, inplace = True)
        e_admissions[df_str] = e_admissions[df_str][e_admissions[df_str].Area != 'Inner London']
        e_admissions[df_str]['Area'].replace('', np.nan, inplace=True)
        e_admissions[df_str].dropna(subset=['Area'], inplace=True)
        # e_admissions[df_str] = e_admissions[df_str].astype({'EmergencyAdmissions':'int'})

    for i in range(2009,2011):
        # Drop unnecessary columns in dataframes for 2009, 2010
        df_str = 'df_' + str(i)
        e_admissions[df_str] = e_admissions[df_str].drop(e_admissions[df_str].iloc[:, 15:241],axis='columns')
        e_admissions[df_str] = e_admissions[df_str].drop(['EmergencyAdmissions'], axis='columns')
        # Rename column for Emergency Admissions
        e_admissions[df_str] = e_admissions[df_str].rename({'Number of Admission Continuous Inpatient Spells - Numerator.1': 'EmergencyAdmissions'}, axis='columns')

    for i in range(2015,2020):
        # Rename columns for NHS provider and Emergency Admissions
        df_str = 'df_' + str(i)
        e_admissions[df_str] = e_admissions[df_str].rename({'Unnamed: 1': 'Provider', 'Unnamed: 12': 'EmergencyAdmissions'}, axis='columns')
        # Drop unnecessary columns
        for i in range(len(e_admissions[df_str].columns)):
            if i != 1 and i != 12:
                e_admissions[df_str] = e_admissions[df_str].drop(['Unnamed: ' + str(i)], axis='columns')
        # Drop unnecessary rows
        e_admissions[df_str] = e_admissions[df_str].drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        # Drop '\t' from Emergency column
        e_admissions[df_str]['EmergencyAdmissions'] = e_admissions[df_str]['EmergencyAdmissions'].str.replace(r'\D', '')
        # Convert provider to uppercase
        e_admissions[df_str]['Provider'] = e_admissions[df_str]['Provider'].str.upper()

    # Rename columns for NHS provider and Emergency Admissions
    e_admissions['df_2020'] = e_admissions['df_2020'].rename({'Unnamed: 1': 'Provider', 'Unnamed: 6': 'EmergencyAdmissions'}, axis='columns')
    # Drop unnecessary columns
    for i in range(len(e_admissions['df_2020'].columns)):
        if i != 1 and i != 6:
            e_admissions['df_2020'] = e_admissions['df_2020'].drop(['Unnamed: ' + str(i)], axis='columns')
    # Drop unnecessary rows
    e_admissions['df_2020'] = e_admissions['df_2020'].drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    # Drop '\t' from Emergency column
    e_admissions['df_2020']['EmergencyAdmissions'] = e_admissions['df_2020']['EmergencyAdmissions'].str.replace(r'\D', '')
    # Convert provider to uppercase
    e_admissions['df_2020']['Provider'] = e_admissions['df_2020']['Provider'].str.upper()


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

    # Stadardise year values
    df_acsc['Year'] = df_acsc['Year'].str[:-3]


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

    # Rename column for each year
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
    # rename columns needed
    air_pollution['df_2008'] = air_pollution['df_2008'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2008_other'] = air_pollution['df_2008_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2008_other'].drop(air_pollution['df_2008_other'].tail(3).index, inplace = True)
    # remove rows not related to boroughs
    air_pollution['df_2008'].drop(air_pollution['df_2008'].index[1:52], inplace = True)
    air_pollution['df_2008'].drop(air_pollution['df_2008'].tail(22).index, inplace = True)
    # remove all rows except for borough totals
    air_pollution['df_2008'] = air_pollution['df_2008'][air_pollution['df_2008']['Area'].str.contains("Total") == True]
    # format borough names
    air_pollution['df_2008']['Area'] = air_pollution['df_2008']['Area'].str.replace(' Total', '')
    air_pollution['df_2008']['Area'] = air_pollution['df_2008']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # reset dataframe index
    air_pollution['df_2008'].reset_index(drop=True, inplace=True)
    # add total column to 'other' total column
    air_pollution['df_2008']['PM25'] = air_pollution['df_2008']['PM25'].astype(float) + air_pollution['df_2008_other']['PM25'].astype(float)

    air_pollution['df_2010'] = pd.read_csv('Data/AirPollution/Road 2010 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2010_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2010.csv', dtype=str, keep_default_na=False)
    # rename columns needed
    air_pollution['df_2010'] = air_pollution['df_2010'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2010_other'] = air_pollution['df_2010_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2010_other'].drop(air_pollution['df_2010_other'].tail(3).index, inplace = True)
    # remove rows not related to boroughs
    air_pollution['df_2010'].drop(air_pollution['df_2010'].index[1:52], inplace = True)
    air_pollution['df_2010'].drop(air_pollution['df_2010'].tail(22).index, inplace = True)
    # remove all rows except for borough totals
    air_pollution['df_2010'] = air_pollution['df_2010'][air_pollution['df_2010']['Area'].str.contains("Total") == True]
    # format borough names
    air_pollution['df_2010']['Area'] = air_pollution['df_2010']['Area'].str.replace(' Total', '')
    air_pollution['df_2010']['Area'] = air_pollution['df_2010']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # reset dataframe index
    air_pollution['df_2010'].reset_index(drop=True, inplace=True)
    # add total column to 'other' total column
    air_pollution['df_2010']['PM25'] = air_pollution['df_2010']['PM25'].astype(float) + air_pollution['df_2010_other']['PM25'].astype(float)

    air_pollution['df_2012'] = pd.read_csv('Data/AirPollution/Road 2012 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2012_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2012.csv', dtype=str, keep_default_na=False)
    # rename columns needed
    air_pollution['df_2012'] = air_pollution['df_2012'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2012_other'] = air_pollution['df_2012_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2012_other'].drop(air_pollution['df_2012_other'].tail(3).index, inplace = True)
    # remove rows not related to boroughs
    air_pollution['df_2012'].drop(air_pollution['df_2012'].index[1:52], inplace = True)
    air_pollution['df_2012'].drop(air_pollution['df_2012'].tail(22).index, inplace = True)
    # remove all rows except for borough totals
    air_pollution['df_2012'] = air_pollution['df_2012'][air_pollution['df_2012']['Area'].str.contains("Total") == True]
    # format borough names
    air_pollution['df_2012']['Area'] = air_pollution['df_2012']['Area'].str.replace(' Total', '')
    air_pollution['df_2012']['Area'] = air_pollution['df_2012']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # reset dataframe index
    air_pollution['df_2012'].reset_index(drop=True, inplace=True)
    # add total column to 'other' total column
    air_pollution['df_2012']['PM25'] = air_pollution['df_2012']['PM25'].astype(float) + air_pollution['df_2012_other']['PM25'].astype(float)

    air_pollution['df_2013'] = pd.read_csv('Data/AirPollution/PM2.5 Totals by Borough2013.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2013'] = air_pollution['df_2013'].rename({'PM2.5 Pivot Table by Borough': 'Area', 'Unnamed: 13': 'PM25'}, axis='columns')
    air_pollution['df_2013']['PM25'] = air_pollution['df_2013']['PM25'].str.replace('\t', '')

    air_pollution['df_2015'] = pd.read_csv('Data/AirPollution/Road 2015 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2015_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2015.csv', dtype=str, keep_default_na=False)
    # rename columns needed
    air_pollution['df_2015'] = air_pollution['df_2015'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2015_other'] = air_pollution['df_2015_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2015_other'].drop(air_pollution['df_2015_other'].tail(3).index, inplace = True)
    # remove rows not related to boroughs
    air_pollution['df_2015'].drop(air_pollution['df_2015'].index[1:52], inplace = True)
    air_pollution['df_2015'].drop(air_pollution['df_2015'].tail(22).index, inplace = True)
    # remove all rows except for borough totals
    air_pollution['df_2015'] = air_pollution['df_2015'][air_pollution['df_2015']['Area'].str.contains("Total") == True]
    # format borough names
    air_pollution['df_2015']['Area'] = air_pollution['df_2015']['Area'].str.replace(' Total', '')
    air_pollution['df_2015']['Area'] = air_pollution['df_2015']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # reset dataframe index
    air_pollution['df_2015'].reset_index(drop=True, inplace=True)
    # add total column to 'other' total column
    air_pollution['df_2015']['PM25'] = air_pollution['df_2015']['PM25'].astype(float) + air_pollution['df_2015_other']['PM25'].astype(float)

    air_pollution['df_2016'] = pd.read_csv('Data/AirPollution/PM2.5 Summary2016.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2016'] = air_pollution['df_2016'].transpose()
    air_pollution['df_2016'] = air_pollution['df_2016'].rename({6: 'Area', 68: 'PM25'}, axis='columns')
    air_pollution['df_2016']['PM25'] = air_pollution['df_2016']['PM25'].str.replace('\t', '')

    air_pollution['df_2019'] = pd.read_csv('Data/AirPollution/PM2.5 Summary2019.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2019'] = air_pollution['df_2019'].transpose()
    air_pollution['df_2019'] = air_pollution['df_2019'].rename({6: 'Area', 71: 'PM25'}, axis='columns')
    air_pollution['df_2019']['PM25'] = air_pollution['df_2019']['PM25'].str.replace('\t', '')

    air_pollution['df_2020'] = pd.read_csv('Data/AirPollution/Road 2020 - Total-Table 1.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2020_other'] = pd.read_csv('Data/AirPollution/PM25NRMM:Agriculture2020.csv', dtype=str, keep_default_na=False)
    # rename columns needed
    air_pollution['df_2020'] = air_pollution['df_2020'].rename({'Unnamed: 0': 'Area', 'Unnamed: 11': 'PM25'}, axis='columns')
    air_pollution['df_2020_other'] = air_pollution['df_2020_other'].rename({'NRMM/Agriculture/Other-ALL': 'Area', 'PM25_TA': 'PM25'}, axis='columns')
    air_pollution['df_2020_other'].drop(air_pollution['df_2020_other'].tail(3).index, inplace = True)
    # remove rows not related to boroughs
    air_pollution['df_2020'].drop(air_pollution['df_2020'].index[1:52], inplace = True)
    air_pollution['df_2020'].drop(air_pollution['df_2020'].tail(22).index, inplace = True)
    # remove all rows except for borough totals
    air_pollution['df_2020'] = air_pollution['df_2020'][air_pollution['df_2020']['Area'].str.contains("Total") == True]
    # format borough names
    air_pollution['df_2020']['Area'] = air_pollution['df_2020']['Area'].str.replace(' Total', '')
    air_pollution['df_2020']['Area'] = air_pollution['df_2020']['Area'].str.replace(r'City$', 'City of London', regex = True)
    # reset dataframe index
    air_pollution['df_2020'].reset_index(drop=True, inplace=True)
    # add total column to 'other' total column
    air_pollution['df_2020']['PM25'] = air_pollution['df_2020']['PM25'].astype(float) + air_pollution['df_2020_other']['PM25'].astype(float)


    return air_pollution






def main():
    london_boroughs = ['-', 'City of London', 'City of Westminster', 'Kensington and Chelsea', 'Hammersmith and Fulham', 
            'Wandsworth', 'Lambeth', 'Southwark', 'Tower Hamlets', 'Hackney', 'Islington', 'Camden', 'Brent', 'Ealing', 'Hounslow', 
            'Richmond', 'Kingston', 'Merton', 'Sutton', 'Croydon', 'Bromley', 'Lewisham', 'Greenwich', 'Bexley', 'Havering', 
            'Barking and Dagenham', 'Redbridge', 'Newham', 'Waltham Forest', 'Haringey', 'Enfield', 'Barnet', 'Harrow', 'Hillingdon']

    borough_trust_mapping = {'City of London': 'Barts Health NHS Trust', 
        'City of Westminster': 'Chelsea and Westminster Hospital NHS Foundation Trust', 
        'Kensington and Chelsea': 'Chelsea and Westminster Hospital NHS Foundation Trust', 
        'Hammersmith and Fulham': 'Imperial College Healthcare NHS Trust', 
        'Wandsworth': 'St George\'s University Hospitals NHS Foundation Trust', 
        'Lambeth': 'Guy\'s and St Thomas\' NHS Foundation Trust', 
        'Southwark': 'Guy\'s and St Thomas\' NHS Foundation Trust', 
        'Tower Hamlets': 'Barts Health NHS Trust', 
        'Hackney': 'Homerton Healthcare NHS Foundation Trust', 
        'Islington': 'The Whittington Hospital NHS Trust', 
        'Camden': 'Royal Free London NHS Foundation Trust', 
        'Brent': 'London North West University Healthcare NHS Trust', 
        'Ealing': 'London North West University Healthcare NHS Trust', 
        'Hounslow': 'Hounslow and Richmond Community Healthcare NHS Trust', 
        'Richmond': 'Hounslow and Richmond Community Healthcare NHS Trust', 
        'Kingston': 'Kingston Hospital NHS Foundation Trust', 
        'Merton': 'Epsom and St Helier University Hospitals NHS Trust', 
        'Sutton': 'Epsom and St Helier University Hospitals NHS Trust', 
        'Croydon': 'Croydon Health Services NHS Trust', 
        'Bromley': 'King\'s College Hospital NHS Foundation Trust', 
        'Lewisham': 'Lewisham and Greenwich NHS Trust', 
        'Greenwich': 'Lewisham and Greenwich NHS Trust', 
        'Bexley': 'Lewisham and Greenwich NHS Trust', 
        'Havering': 'Barking, Havering And Redbridge University Hospitals NHS Trust', 
        'Barking and Dagenham': 'Barking, Havering And Redbridge University Hospitals NHS Trust', 
        'Redbridge': 'Barking, Havering And Redbridge University Hospitals NHS Trust', 
        'Newham':'Barts Health NHS Trust', 
        'Waltham Forest':'Barts Health NHS Trust', 
        'Haringey':'The Whittington Hospital NHS Trust', 
        'Enfield': 'North Middlesex University Hospital NHS Trust', 
        'Barnet': 'Royal Free London NHS Foundation Trust', 
        'Harrow': 'London North West University Healthcare NHS Trust', 
        'Hillingdon': 'The Hillingdon Hospitals NHS Foundation Trust'}

    st.set_page_config(
        page_title='London Healthcare Dashboard',
        layout='wide',
        initial_sidebar_state='collapsed',
    )

    e_admissions = emergency_admissions_data()
    df_acsc = acsc_admissions_data()
    df_fastfood = fast_food_data()
    air_pollution = air_pollution_data()




if __name__ == "__main__":
    main()