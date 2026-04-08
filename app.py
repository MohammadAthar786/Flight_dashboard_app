import streamlit as st
import plotly.express as px
import pandas as pd
from dbhelper import DB

# Page Configuration 
st.set_page_config(layout="wide", page_title="Flight Analytics")
# Making DB class Object 
db = DB()

st.title(" Flight Analytics Dashboard")
st.markdown("Explore insights and search flights")

# Sidebar
st.sidebar.title("Navigation")
user_option = st.sidebar.selectbox(
    "Menu",
    ["Select One", "Check Flights", "Analytics"]
)

#  Check Flights
if user_option == "Check Flights":
    
    st.header(" Search Flights")
    col1, col2 = st.columns(2)

    with col1:
        city = db.fetch_city_names()
        source = st.selectbox("Source", sorted(city))

    with col2:
        city = db.fetch_city_names()
        destination = st.selectbox("Destination", sorted(city))

    if st.button("Search Flights"):
        with st.spinner("Fetching flights "):
            results = db.fetch_all_flights(source, destination)

        if len(results) == 0:
            st.warning("No flights found for this route 🙁")
        else:
##  Coloumn name is set Manually (By default column name is not set its will be 0 1 2 .. )
            df = pd.DataFrame(
                results,
                columns=[
                    "Airline", "Date", "Route",
                    "Departure", "Duration", "Price"
                ]
            )

            # Price Filter
            min_price = int(df["Price"].min())
            max_price = int(df["Price"].max())

            price_range = st.slider(
                "Filter by Price",
                min_price,
                max_price,
                (min_price, max_price)
            )

            df = df[
                (df["Price"] >= price_range[0]) &
                (df["Price"] <= price_range[1])
            ]

            # Metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Flights", len(df))
            with col2:
                st.metric("Avg Price", round(df["Price"].mean(), 2))

            st.dataframe(df, use_container_width=True)


#  ANALYTICS

elif user_option == "Analytics":

    st.header(" Flight Insights")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Airlines", "Airports", "Trends", "Advanced"]
    )

    
    #  Airlines

    with tab1:
        airlines, frequency = db.fetch_airlines()

        fig = px.pie(
            names=airlines,
            values=frequency,
            title="Flights Distribution by Airline"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Avg Price per airline
        airlines, prices = db.avg_price_per_airline()

        fig = px.bar(
            x=airlines,
            y=prices,
            title="Average Price per Airline"
        )
        st.plotly_chart(fig, use_container_width=True)

    
    #  Airports
   
    with tab2:
        airport, traffic = db.busiest_airport()

        fig = px.bar(
            x=airport,
            y=traffic,
            title="Top 10 Busiest Airports"
        )
        st.plotly_chart(fig, use_container_width=True)

    
    #  Trends

    with tab3:
        dates, flights_count = db.daily_number_of_flights()

        df = pd.DataFrame({
            "Date": pd.to_datetime(dates),
            "Flights": flights_count
        }).sort_values("Date")

        fig = px.line(
            df,
            x="Date",
            y="Flights",
            title="Daily Flights Trend"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Monthly trend
        data = db.flights_per_month()
        df_month = pd.DataFrame(data, columns=["Month", "Flights"])

        fig = px.bar(
            df_month,
            x="Month",
            y="Flights",
            title="Flights per Month"
        )
        st.plotly_chart(fig, use_container_width=True)

    
    #  Advanced
 
    with tab4:
        data = db.expensive_routes()

        df = pd.DataFrame(
            data,
            columns=["Source", "Destination", "Avg Price"]
        )

        fig = px.bar(
            df,
            x="Source",
            y="Avg Price",
            color="Destination",
            title="Top Expensive Routes"
        )
        st.plotly_chart(fig, use_container_width=True)


#  DEFAULT

else:
    st.title(" About This Project")
    st.markdown("""
    This is a Flight Analytics App built using:

    - Python
    - Streamlit
    - MySQL
    - Plotly

    Features:
    - Flight search system
    - Data analytics dashboard
    - SQL-based backend
    """)