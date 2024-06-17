import pandas as pd
import json
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu



st.set_page_config(layout="wide")
st.header(":blue[AIRBNB DATA ANALYSIS]", divider="violet")

with open("C:\\Users\\Abdul\\Downloads\\sample_airbnb.json") as file:
    data = json.load(file)
df = pd.DataFrame(data)

df['host_id'] = df['host'].apply(lambda x: x['host_id'])
df['host_name'] = df['host'].apply(lambda x: x['host_name'])
df['host_total_listings_count'] = df['host'].apply(lambda x: x['host_total_listings_count'])
df['suburb'] = df['address'].apply(lambda x: x['suburb'])
df['market'] = df['address'].apply(lambda x: x['market'])
df['country'] = df['address'].apply(lambda x: x['country'])
df['availability_365'] = df['availability'].apply(lambda x: x['availability_365'])
df['latitude'] = df['address'].apply(lambda x: x['location']['coordinates'][1])
df['longitude'] = df['address'].apply(lambda x: x['location']['coordinates'][0])
df['no_amenities']=df['amenities'].apply(len)


df1 = df[['_id','name','property_type','room_type','bed_type','minimum_nights','number_of_reviews','no_amenities','maximum_nights','amenities','latitude','longitude','price','host_id','host_name','host_total_listings_count','suburb','market','country','availability_365','accommodates']]

selected_country = st.sidebar.selectbox("Select country", df1['country'].unique())
selected_area = st.sidebar.selectbox("Select city", df1['market'].unique())


def host_name1(selected_area):
    df_area = df[df['market'] == selected_area]

    host_df= df_area.groupby(['host_name','host_total_listings_count'])['market'].max().reset_index()
    hosts_df=host_df.sort_values(by='host_total_listings_count',ascending=False).head(10)

    fig = px.bar(hosts_df,
                x='host_name',
                y='host_total_listings_count',
                title=f"{selected_area}",
                color_discrete_sequence=px.colors.sequential.Blugrn_r)
    st.plotly_chart(fig)


def host_name2(selected_country):
    df_country = df[df['country'] == selected_country]

    host_df1= df_country.groupby(['host_name','country'])['host_total_listings_count'].max().reset_index()
    hosts_df1 = host_df1.sort_values(by='host_total_listings_count',ascending=False).head(10)

    fig = px.bar(hosts_df1,
                x='host_name',
                y='host_total_listings_count',
                title=f"{selected_country}",
                color_discrete_sequence=px.colors.sequential.Brwnyl_r)
    st.plotly_chart(fig)


def prices1(selected_area):
    df_area = df[df['market'] == selected_area]

    price_df= df_area.groupby(['room_type','market'])['price'].sum().reset_index()
    prices_df=price_df.sort_values(by='price',ascending=False)


    fig = px.bar(prices_df,
                x='room_type',
                y='price',
                title=f'{selected_area}',
                color_discrete_sequence=px.colors.sequential.Blugrn_r)
    st.plotly_chart(fig)


def prices2(selected_country):
    df_country = df[df['country'] == selected_country]

    price_df1= df_country.groupby(['room_type','country'])['price'].sum().reset_index()
    prices_df1=price_df1.sort_values(by='price',ascending=False)


    fig = px.bar(prices_df1,
                x='room_type',
                y='price',
                title=f'{selected_country}',
                color_discrete_sequence=px.colors.sequential.Blugrn_r)
    st.plotly_chart(fig)


def prices3(selected_area):
    df_area = df[df['market'] == selected_area]

    price_df1= df_area.groupby(['property_type','market'])['price'].sum().reset_index()
    prices_df1=price_df1.sort_values(by='price',ascending=False)


    fig = px.line(prices_df1,
                x='property_type',
                y='price',
                title=f'{selected_area}',
                markers=True,
                color_discrete_sequence=px.colors.sequential.Blugrn_r)
    st.plotly_chart(fig)


def prices4(selected_country):
    df_country = df[df['country'] == selected_country]

    price_df1= df_country.groupby(['property_type','country'])['price'].sum().reset_index()
    prices_df1=price_df1.sort_values(by='price',ascending=False)


    fig = px.line(prices_df1,
                x='property_type',
                y='price',
                title=f"{selected_country}",
                markers=True,
                color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig)



page1,page2,page3 = st.tabs([":violet[Airbnb Data]",":violet[Data Analysis]",":violet[Insights]"])

with page1:
    st.subheader("Filtered data")
    st.write(df1)


with page2:
    st.subheader(":red[Top 10 hosts based on listings count]")
    top10_host_df= df1.groupby(['host_name','country','market'])['host_total_listings_count'].max().reset_index()
    top10_hosts_df = top10_host_df.sort_values(by='host_total_listings_count',ascending=False).head(10)
    fig1 = px.icicle(top10_hosts_df,
                path = ['country','market','host_name'],
                values = 'host_total_listings_count',
                width=800,
                height=800)
    st.plotly_chart(fig1)


    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Top hosts in selected city")
        host_name1(selected_area)
    with col2:
        st.subheader("Top hosts in selected country")
        host_name2(selected_country)


    st.subheader("Price distribution of Room type")
    top_price_df= df1.groupby(['room_type','country'])['price'].sum().reset_index()
    top_prices_df=top_price_df.sort_values(by='price',ascending=False).head(10)
    fig2 = px.choropleth(top_prices_df,
                        locations='country',
                        locationmode='country names',
                        color='room_type',
                        hover_name='price',
                        color_continuous_scale=px.colors.sequential.Plasma
                        )
    st.plotly_chart(fig2)


    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Room type prices citieswise")
        prices1(selected_area)
    with col2:
        st.subheader("Room type prices countrieswise")
        prices2(selected_country)


    st.subheader("Countries with max prices of Property type")
    price_df1= df1.groupby(['property_type','country','latitude','longitude'])['price'].sum().reset_index()
    prices_df1=price_df1.sort_values(by='price',ascending=False).head(10)
    fig3 = px.scatter_geo(prices_df1,
                        lat='latitude',
                        lon='longitude',
                        color='price',
                        text='country')
    st.plotly_chart(fig3)


    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Property type prices citieswise")
        prices3(selected_area)
    with col2:
        st.subheader("Property type prices countrieswise")
        prices4(selected_country)


    st.subheader("Listings based on max amenities")
    price_df = df1.groupby(['name','no_amenities'])['price'].max().reset_index()
    prices_df = price_df.sort_values(by='no_amenities',ascending=False).head(10)
    fig4 = px.pie(prices_df,
                values = 'no_amenities',
                names='name',
                hover_data=['price'],
                hole = 0.4
                )
    st.plotly_chart(fig4)


    st.subheader("Listings based on 365 days available")
    df_avail_365 = df[df['availability_365'] == 365]
    availability = df_avail_365.groupby(['name','price','availability_365'])['accommodates'].max().reset_index()
    Avail_365=availability.sort_values(by='accommodates',ascending=False).head(10)
    fig5 = px.sunburst(Avail_365,
                    path=['accommodates','name','availability_365'],
                    values='price',
                    color_continuous_scale="RdBu")
    st.plotly_chart(fig5)


    st.subheader("Listings based on max reviews")
    listing_df = df1.groupby(['name','number_of_reviews','country'])['price'].max().reset_index()
    listings_df = listing_df.sort_values(by='number_of_reviews',ascending=False).head(10)
    fig6 = px.bar(listings_df,
                x='number_of_reviews',
                y = 'name',
                orientation='h',
                hover_data='country',
                color_discrete_sequence=px.colors.sequential.Darkmint_r
                )
    st.plotly_chart(fig6)


    st.subheader("Correlation matrix")
    numeric_df = df1.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    sns.heatmap(corr)
    st.pyplot(plt)
    
with page3:
    st.header("Summarized Insights")
    st.write("""1) We can observe that, the host **Sonder** from **Canada** is having the max number of listings.
             Also, if we have a look by countries, **US** is having the maximum number of listings.""")
    st.write("""2) Coming to the room type and property type, we can observe that, **Entire house** and 
             **Apartment** are in the highest prices compared to other property types and room types.
             They are high in the countries like **Brazil,Hongkong,US**.""")
    st.write("""3) Private studio Waikiki Dream from **US** is having the maximum number of reviews.
             Here, we could imagine that many customers have visited this place""")
    st.write("""4) 365 days available listings with maximum accommodates of 16 were located in **Turkey**
             & **Brazil**.""")
    st.write("""5) Sublime loft with private roof top from **Montreal**,**Canada** is having the maximum number 
             of amenities""")