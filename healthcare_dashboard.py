import altair as alt
import matplotlib.pyplot as plt
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
        # Convert NHS provider to uppercase
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
    # Convert NHS provider to uppercase
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

    # Standardise year values from 'xxxx/xx' format to 'xxxx'
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

    air_pollution['df_2013'] = pd.read_csv('Data/AirPollution/PM2.5 Totals by Borough2013.csv', dtype=str, keep_default_na=False)
    air_pollution['df_2013'] = air_pollution['df_2013'].rename({'PM2.5 Pivot Table by Borough': 'Area', 'Unnamed: 13': 'PM25'}, axis='columns')
    air_pollution['df_2013']['PM25'] = air_pollution['df_2013']['PM25'].str.replace('\t', '')

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


    return air_pollution




# --------------------------------------------------
# Dashboard
# --------------------------------------------------

def intro():
    st.title('London Healthcare Dashboard')

    # Mapping between London Boroughs and their respective NHS providers
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
    # Mapping between London Boroughs and their respective NHS providers
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
            if i < 2015:
                year_vals.append(float(e_admissions[df_str].loc[e_admissions[df_str]['Area'] == str(borough), 'EmergencyAdmissions'])/100)
            else:
                year_vals.append(float(e_admissions[df_str].loc[e_admissions[df_str]['Provider'] == borough_trust_mapping[str(borough)].upper(), 'EmergencyAdmissions'])/100)
        if 'ACSC Admissions/10' in options:
            df_str = str(i)
            year_vals.append(float(df_acsc.loc[(df_acsc['Year'] == df_str) & (df_acsc['Level description'] == str(borough)) & (df_acsc['Quarter'] == 'Annual')].head(1)['Observed'])/10)
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

    # Line Graph of Attributes selected over time period selected
    st.markdown("### Time Series")
    # Convert df from wide to long format, drop empty rows
    borough_df = borough_df.melt('Date').dropna()
    line = alt.Chart(borough_df).mark_line().encode(
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
    line_plot = st.altair_chart(line)

    # Animate line chart, redraw whenever page reloaded
    # Use for loop to plot an extra row of the df each iteration
    for i in range(1, borough_df.shape[0]+1):
        temp_df = borough_df.iloc[0:i]
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
        line_plot = line_plot.altair_chart(line)




def main():
    london_boroughs = ['-', 'City of London', 'City of Westminster', 'Kensington and Chelsea', 'Hammersmith and Fulham', 
            'Wandsworth', 'Lambeth', 'Southwark', 'Tower Hamlets', 'Hackney', 'Islington', 'Camden', 'Brent', 'Ealing', 'Hounslow', 
            'Richmond', 'Kingston', 'Merton', 'Sutton', 'Croydon', 'Bromley', 'Lewisham', 'Greenwich', 'Bexley', 'Havering', 
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