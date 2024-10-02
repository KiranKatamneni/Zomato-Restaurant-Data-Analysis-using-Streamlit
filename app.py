import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set page layout
st.set_page_config(layout="wide")

# Define a function to load the data
@st.cache_data
def load_data():
    zomato = pd.read_csv("C:/Users/Kiran/Downloads/zomato.csv", encoding='ISO-8859-1')
    country = pd.read_excel("C:/Users/Kiran/Downloads/Country_Code.xlsx")
    return zomato, country

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ('Home', 'Data preprocessing and EDA'))

# Home Page
if page == 'Home':
    st.title("Home Page")
    st.write("Welcome! This application performs data preprocessing and EDA on Zomato Data.")

    st.subheader("Get Started:")
    st.write("Navigate to 'Data and Preprocessing' to explore the processed data.")

    st.subheader("About Data:")
    st.write("The collected data has been stored in the Comma Separated Value file Zomato.csv")
    st.markdown("• Restaurant Id: Unique id of every restaurant across various cities of the world")
    st.markdown("• Restaurant Name: Name of the restaurant")
    st.markdown("• Country Code: Country in which restaurant is located")
    st.markdown("• City: City in which restaurant is located")
    st.markdown("• Address: Address of the restaurant")
    st.markdown("• Locality: Location in the city")
    st.markdown("• Locality Verbose: Detailed description of the locality")
    st.markdown("• Longitude: Longitude coordinate of the restaurant's location")
    st.markdown("• Latitude: Latitude coordinate of the restaurant's location")
    st.markdown("• Cuisines: Cuisines offered by the restaurant")
    st.markdown("• Average Cost for two: Cost for two people in different currencies")
    st.markdown("• Currency: Currency of the country")
    st.markdown("• Has Table booking: yes/no")
    st.markdown("• Has Online delivery: yes/ no")
    st.markdown("• Is delivering: yes/ no")
    st.markdown("• Switch to order menu: yes/no")
    st.markdown("• Price range: range of price of food")
    st.markdown("• Aggregate Rating: Average rating out of 5")
    st.markdown("• Rating color: depending upon the average rating color")
    st.markdown("• Rating text: text on the basis of rating of rating")
    st.markdown("• Votes: Number of ratings casted by people")

# Data and Preprocessing Page
if page == 'Data preprocessing and EDA':
    st.title("Data preprocessing")
    
    st.write("For this task, I have used two datasets: 'Zomato' and 'Country Code'.")

    # Load datasets
    zomato, country = load_data()

    # Display option to show data
    show_data = st.checkbox("**Show Data**")
    
    if show_data:
        # Display shapes and info of the datasets
        st.subheader("Shapes of Datasets")
        st.text(f"zomato: {zomato.shape}")
        st.text(f"country: {country.shape}")

        # Display sample data
        st.subheader("Sample Data:")
        st.text("zomato:")
        st.dataframe(zomato.head())
        st.text("country:")
        st.dataframe(country.head())

    # Ask user if they want to see preprocessing steps
    show_preprocessing = st.checkbox("**Show Preprocessing Steps**", value=False)
    
    # Preprocessing Data
    if show_preprocessing:
        if st.checkbox("Drop Rows with Null Values"):
            zomato = zomato.dropna()
            st.success("Dropped all rows with null values.")

        # Check for null values after filling
        st.subheader("Check Null Values After Preprocessing")
        null_values = zomato.isnull().sum()
        st.write(null_values[null_values > 0].sort_values(ascending=False))
    
    if st.checkbox("**Merge Datasets**"):
            # Assume 'country_code' is the common column in both datasets
            merged_data = pd.merge(zomato, country, left_on='Country Code', right_on='Country Code', how='inner')
            st.success("Datasets merged successfully!")

            st.session_state.merged_data = merged_data

            st.subheader("Merged Data:")
            st.dataframe(merged_data.head())
    
    st.title("EDA")

    if 'merged_data' in st.session_state:
        merged_data = st.session_state.merged_data  # Get merged data from session state

        # Map Visualization
        if st.checkbox("Show Restaurant Locations on Map"):
            st.subheader("Restaurant Locations Map")
            
            fig = px.scatter_mapbox(
                merged_data,
                lat='Latitude',
                lon='Longitude',
                hover_name='Restaurant Name',
                hover_data=['Cuisines', 'Average Cost for two', 'Currency', 'Aggregate rating'],
                center=dict(lat=merged_data['Latitude'].mean(), lon=merged_data['Longitude'].mean()),
                zoom=1,
            )
            
            fig.update_layout(mapbox_style='open-street-map')
            st.plotly_chart(fig)

        if st.checkbox("Show Pie Chart for Top 3 Countries Using Zomato"):
            st.subheader("Top 3 Countries Using Zomato")

            # Grouping and counting countries
            count_countries = merged_data.groupby('Country').agg({'Country': 'count'})
            count_countries = count_countries.rename(columns={'Country': 'count'}).sort_values(by='count', ascending=False)
            count_countries.reset_index(inplace=True)

            # Plot Pie Chart
            fig, ax = plt.subplots(figsize = (2,2))
            ax.pie(
                x=count_countries['count'][:3],
                labels=count_countries['Country'][:3],
                autopct='%.2f%%',
                textprops={'fontsize': 4}
            )
            ax.set_title('Top 3 Countries Using Zomato')

            # Display the plot in Streamlit
            st.pyplot(fig)

        if st.checkbox("Show Pie Chart for Top 5 cities Using Zomato"):
            st.subheader("Top 5 Cities Using Zomato")

            # Grouping and counting countries
            count_city = merged_data.groupby('City').agg({'City': 'count'})
            count_city = count_city.rename(columns={'City': 'count'}).sort_values(by='count', ascending=False)
            count_city.reset_index(inplace=True)

            # Plot Pie Chart
            fig, ax = plt.subplots(figsize = (2,2
        ))
            ax.pie(
                x=count_city['count'][:5],
                labels=count_city['City'][:5],
                autopct='%.2f%%',
                textprops={'fontsize': 5}
            )

            # Display the plot in Streamlit
            st.pyplot(fig)
        if st.checkbox("Show Countplot for Restaurant Ratings"):
            st.subheader("Count of Restaurant Ratings on Zomato")

            # Plotting the countplot for 'rating_text'
            fig, ax = plt.subplots(figsize=(8, 3))  # Adjust figure size if needed
            sns.countplot(data = merged_data, x='Rating text', ax=ax,palette='pastel')

            # Display the plot in Streamlit
            st.pyplot(fig)

        if st.checkbox("Show Bar Plot for Top 10 Cuisines"):
            st.subheader("Top 10 Most Popular Cuisines on Zomato")

            # Create a list of all cuisines from the 'cuisines' column
            cuisine_lst = []
            for cuis in merged_data['Cuisines'].dropna().values:
                cuisine_lst.extend(cuis.split(', '))

            # Create a dataframe with the top 10 cuisines
            top_cuisine_lst = pd.Series(cuisine_lst).value_counts().head(10).reset_index()
            top_cuisine_lst = top_cuisine_lst.rename(columns={'index': 'cuisine', 0: 'count'})

            # Plotting the barplot for top 10 cuisines
            fig, ax = plt.subplots(figsize=(8, 4))  # Adjust the figure size if needed
            sns.barplot(data=top_cuisine_lst, x='cuisine', y='count', ax=ax, palette='flare')

            # Customizing the plot
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")  # Rotate x-axis labels for better readability
            ax.set_title("Top 10 Cuisines on Zomato", pad=10)

            # Display the plot in Streamlit
            st.pyplot(fig)

        if st.checkbox("Show Bar Plot for Top 10 Restaurants by Votes"):
            st.subheader("Top 10 Restaurants by Votes")

            top_10_by_votes = merged_data.groupby('Restaurant Name')['Votes'].sum().reset_index().sort_values(by = 'Votes',ascending = False).head(10)

            # Assuming you already have 'top_10_by_votes' dataframe
            # Plotting the barplot for top 10 restaurants by votes
            fig, ax = plt.subplots(figsize=(8, 4))  # Adjust the figure size if needed
            sns.barplot(data=top_10_by_votes, y='Restaurant Name', x='Votes', palette="Spectral", ax=ax)

            # Customizing the plot
            ax.set_title("Top 10 Restaurants by Votes", pad=10)
            ax.set_xlabel("Votes")
            ax.set_ylabel("Restaurant Name")

            # Display the plot in Streamlit
            st.pyplot(fig)