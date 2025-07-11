import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


st.set_page_config(
    page_title="Flight Redemption Optimizer",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .excellent { border-left: 4px solid #28a745; }
    .good { border-left: 4px solid #17a2b8; }
    .fair { border-left: 4px solid #ffc107; }
    .poor { border-left: 4px solid #dc3545; }
</style>
""", unsafe_allow_html=True)


def main():
    st.sidebar.title("✈️ Flight Redemption Optimizer")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home", "🔍 Search Flights", "📊 Results", "📚 About"]
    )
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔍 Search Flights":
        show_search_page()
    elif page == "📊 Results":
        show_results_page()
    elif page == "📚 About":
        show_about_page()


def show_home_page():
    st.markdown('<h1 class="main-header">Flight Redemption Optimizer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find the best value for your miles with expert-backed recommendations</p>', unsafe_allow_html=True)
   
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800",
                caption="Maximize your travel rewards", use_container_width=True)
   
    st.markdown("---")
    st.markdown("## 🎯 Why Use Flight Redemption Optimizer?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 💰 Maximize Value
        Compare your redemptions to expert valuations from Upgraded Points, The Points Guy, and more.
        """)
    with col2:
        st.markdown("""
        ### 🛣️ Find Best Routes
        Discover direct and layover options you might have missed, ranked by value.
        """)
    with col3:
        st.markdown("""
        ### 📊 Expert Analysis
        Get detailed breakdowns of savings, complexity, and why each option is recommended.
        """)
    st.markdown("---")
    st.markdown("## 📈 Understanding Value Categories")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        ### 🟢 EXCELLENT
        **2.0+ cpm**
        - Rare and highly sought after
        - Significantly above average
        - Top 10% of redemptions
        """)
    with col2:
        st.markdown("""
        ### 🔵 GOOD
        **1.5-2.0 cpm**
        - Solid value redemptions
        - Above expert average
        - Top 25% of redemptions
        """)
    with col3:
        st.markdown("""
        ### 🟡 FAIR
        **1.0-1.5 cpm**
        - Acceptable but not outstanding
        - Near expert average
        - Standard redemptions
        """)
    with col4:
        st.markdown("""
        ### 🔴 POOR
        **<1.0 cpm**
        - Consider paying cash instead
        - Below expert average
        - Better to earn miles
        """)


def show_search_page():
    st.markdown("## 🔍 Search for Flight Redemptions")
    st.markdown("Enter your travel details to find the best redemption options.")
    with st.expander("💡 Quick Examples", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Popular Domestic Routes:**")
            st.markdown("""
            - **BOS → SFO** (Boston to San Francisco)
            - **JFK → LAX** (New York to Los Angeles)  
            - **ORD → MIA** (Chicago to Miami)
            - **DFW → SEA** (Dallas to Seattle)
            """)
        with col2:
            st.markdown("**Recommended Settings:**")
            st.markdown("""
            - **Max Miles:** 25,000-35,000
            - **Max Fees:** $15-25
            - **Min Value:** 1.0-1.5 cpm
            - **Cabin:** Economy (best value)
            """)
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("Origin Airport", placeholder="BOS", help="Enter 3-letter airport code")
            destination = st.text_input("Destination Airport", placeholder="SFO", help="Enter 3-letter airport code")
            departure_date = st.date_input("Departure Date", value=datetime.now() + timedelta(days=30), help="When you want to leave")
            return_date = st.date_input("Return Date", value=None, help="When you want to return (optional)")
        with col2:
            max_miles = st.number_input("Maximum Miles", value=30000, step=5000, help="Your miles budget")
            max_fees = st.number_input("Maximum Fees ($)", value=20, step=5, help="Maximum taxes/fees you'll pay")
            min_value = st.slider("Minimum Value (cpm)", 0.5, 3.0, 1.0, 0.1, help="Minimum cents per mile value")
            cabin_class = st.selectbox("Cabin Class", ["Economy", "Business", "First"])
        if origin and destination:
            if return_date and return_date > departure_date:
                trip_type = "Round Trip"
                st.info(f"🔁 {trip_type}: {departure_date.strftime('%b %d')} → {return_date.strftime('%b %d')} ({return_date - departure_date} days)")
            else:
                trip_type = "One Way"
                st.info(f"➡️ {trip_type}: {departure_date.strftime('%b %d')}")
        else:
            trip_type = "One Way"
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            with col1:
                include_layovers = st.checkbox("Include Layover Routes", value=True, help="Find routes with connections")
                preferred_airlines = st.multiselect("Preferred Airlines", ["AA", "UA", "DL", "AS", "B6"])
            with col2:
                max_layover_hours = st.slider("Max Layover Time (hours)", 1, 12, 6, help="Maximum connection time")
                adults = st.number_input("Number of Passengers", 1, 8, 1)
        submitted = st.form_submit_button("🔍 Search for Redemptions", type="primary")
        if submitted:
            if origin and destination:
                if return_date and return_date <= departure_date:
                    st.error("Return date must be after departure date!")
                    return
                st.session_state.search_params = {
                    'origin': origin.upper(),
                    'destination': destination.upper(),
                    'departure_date': departure_date.strftime('%Y-%m-%d'),
                    'return_date': return_date.strftime('%Y-%m-%d') if return_date and return_date > departure_date else None,
                    'trip_type': trip_type,
                    'max_miles': max_miles,
                    'max_fees': max_fees,
                    'min_value': min_value,
                    'cabin_class': cabin_class.lower(),
                    'include_layovers': include_layovers,
                    'preferred_airlines': preferred_airlines,
                    'max_layover_hours': max_layover_hours,
                    'adults': adults
                }
                with st.spinner("Searching for the best redemption options (sample data)..."):
                    recommendations = generate_synthetic_routes(
                        origin=origin.upper(),
                        destination=destination.upper(),
                        departure_date=departure_date.strftime('%Y-%m-%d'),
                        return_date=return_date.strftime('%Y-%m-%d') if return_date and return_date > departure_date else None,
                        max_miles=max_miles,
                        max_fees=max_fees,
                        min_value=min_value,
                        include_layovers=include_layovers,
                        max_layover_hours=max_layover_hours
                    )
                    st.session_state.recommendations = recommendations
                    st.session_state.search_completed = True
                    st.success(f"Showing {len(recommendations)} sample redemption options! Click the Result Tab to view results.")
                    st.balloons()
            else:
                st.error("Please enter both origin and destination airports.")


def generate_synthetic_routes(origin, destination, departure_date, return_date=None,
                            max_miles=30000, max_fees=20, min_value=1.0,
                            include_layovers=True, max_layover_hours=6):
    layover_options = {
        ('BOS', 'SFO'): ['ORD', 'JFK', 'DEN', 'ATL'],
        ('JFK', 'LAX'): ['ORD', 'DEN', 'ATL', 'DFW'],
        ('ORD', 'MIA'): ['ATL', 'DFW', 'CLT', 'IAH'],
        ('DFW', 'SEA'): ['DEN', 'ORD', 'LAX', 'SLC'],
        ('ATL', 'LAX'): ['DFW', 'DEN', 'ORD', 'CLT'],
        ('BOS', 'LAX'): ['ORD', 'JFK', 'DEN', 'ATL'],
        ('JFK', 'SFO'): ['ORD', 'DEN', 'ATL', 'LAX']
    }
    route_key = (origin, destination)
    reverse_key = (destination, origin)
    layover_airports = layover_options.get(route_key, layover_options.get(reverse_key, ['ORD', 'DEN', 'ATL', 'DFW']))
   
    recommendations = []
   
    direct_route = {
        'origin': origin,
        'destination': destination,
        'type': 'direct',
        'cash_price': 450.00,
        'miles_used': 25000,
        'fees': 11.20,
        'value_per_mile': 1.8,
        'category': 'GOOD',
        'airline': 'AA',
        'flight_number': 'AA1234',
        'departure_time': '10:30',
        'arrival_time': '13:45',
        'duration': '3h 15m',
        'layover': None,
        'layover_duration': None,
        'route_display': f"{origin} → {destination}",
        'expert_comparison': {
            'status': 'ABOVE_AVERAGE',
            'upgraded_points_value': 1.4,
            'points_guy_value': 1.3,
            'awardwallet_value': 1.35
        },
        'savings_analysis': {
            'savings': 438.80,
            'savings_percentage': 97.5,
            'cash_equivalent': 250.00
        },
        'complexity_score': 3,
        'recommendation_reason': 'Direct flight with good value - above expert average'
    }
    recommendations.append(direct_route)
   
    layover_routes = [
        {
            'origin': origin,
            'destination': destination,
            'type': 'layover',
            'cash_price': 520.00,
            'miles_used': 35000,
            'fees': 22.40,
            'value_per_mile': 1.5,
            'category': 'GOOD',
            'airline': 'UA',
            'flight_number': 'UA5678',
            'departure_time': '09:15',
            'arrival_time': '16:30',
            'duration': '7h 15m',
            'layover': layover_airports[0],
            'layover_duration': '2h 45m',
            'route_display': f"{origin} → {layover_airports[0]} → {destination}",
            'expert_comparison': {
                'status': 'ABOVE_AVERAGE',
                'upgraded_points_value': 1.4,
                'points_guy_value': 1.3,
                'awardwallet_value': 1.35
            },
            'savings_analysis': {
                'savings': 497.60,
                'savings_percentage': 95.7,
                'cash_equivalent': 350.00
            },
            'complexity_score': 6,
            'recommendation_reason': 'Layover option with good connection time and solid value'
        },
        {
            'origin': origin,
            'destination': destination,
            'type': 'layover',
            'cash_price': 480.00,
            'miles_used': 30000,
            'fees': 22.40,
            'value_per_mile': 1.6,
            'category': 'GOOD',
            'airline': 'DL',
            'flight_number': 'DL9012',
            'departure_time': '11:45',
            'arrival_time': '18:20',
            'duration': '6h 35m',
            'layover': layover_airports[1],
            'layover_duration': '1h 30m',
            'route_display': f"{origin} → {layover_airports[1]} → {destination}",
            'expert_comparison': {
                'status': 'ABOVE_AVERAGE',
                'upgraded_points_value': 1.4,
                'points_guy_value': 1.3,
                'awardwallet_value': 1.35
            },
            'savings_analysis': {
                'savings': 457.60,
                'savings_percentage': 95.3,
                'cash_equivalent': 300.00
            },
            'complexity_score': 5,
            'recommendation_reason': 'Alternative layover route with excellent value per mile'
        }
    ]
    recommendations.extend(layover_routes)
   
    recommendations.sort(key=lambda x: x['value_per_mile'], reverse=True)
    return recommendations


def show_results_page():
    if not hasattr(st.session_state, 'recommendations') or not st.session_state.get('search_completed'):
        recommendations = generate_synthetic_routes(
            origin='BOS',
            destination='SFO',
            departure_date=(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            max_miles=30000,
            max_fees=20,
            min_value=1.0,
            include_layovers=True,
            max_layover_hours=6
        )
        st.session_state.recommendations = recommendations
        st.session_state.search_params = {
            'origin': 'BOS',
            'destination': 'SFO',
            'departure_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'return_date': None,
            'trip_type': 'One Way',
            'max_miles': 30000,
            'max_fees': 20,
            'min_value': 1.0,
            'cabin_class': 'economy',
            'include_layovers': True,
            'preferred_airlines': [],
            'max_layover_hours': 6,
            'adults': 1
        }
        st.session_state.search_completed = True
        st.info('No search performed yet. Showing sample results for BOS → SFO.')
   
    recommendations = st.session_state.recommendations
    st.markdown("## 📊 Redemption Analysis Results")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Options", len(recommendations))
    with col2:
        if recommendations:
            avg_value = sum(r['value_per_mile'] for r in recommendations) / len(recommendations)
            st.metric("Avg Value (vpm)", f"{avg_value:.2f}")
    with col3:
        if recommendations:
            best_value = max(r['value_per_mile'] for r in recommendations)
            st.metric("Best Value (vpm)", f"{best_value:.2f}")
    with col4:
        if recommendations:
            total_savings = sum(r['savings_analysis']['savings'] for r in recommendations)
            st.metric("Total Savings", f"${total_savings:.0f}")
   
    st.markdown("### 🎯 Recommended Redemptions")
    df_data = []
    for rec in recommendations:
        df_data.append({
            'Type': rec.get('type', 'direct').title(),
            'Route': rec.get('route_display', f"{rec['origin']} → {rec['destination']}"),
            'Cash Price': rec.get('cash_price'),
            'Miles': rec.get('miles_used'),
            'Fees': rec.get('fees'),
            'Value (cpm)': rec.get('value_per_mile'),
            'Category': rec.get('category'),
            'Expert Status': rec.get('expert_comparison', {}).get('status', ''),
            'Savings %': rec.get('savings_analysis', {}).get('savings_percentage', 0),
            'Complexity': rec.get('complexity_score', 0)
        })
   
    df = pd.DataFrame(df_data)
    if df.empty:
        st.warning('No data available to display. Please try searching again or reload the page.')
        return
   
    df_display = df.copy()
    df_display['Cash Price'] = df_display['Cash Price'].apply(lambda x: f"${x:.0f}")
    df_display['Miles'] = df_display['Miles'].apply(lambda x: f"{x:,}")
    df_display['Fees'] = df_display['Fees'].apply(lambda x: f"${x:.0f}")
    df_display['Value (cpm)'] = df_display['Value (cpm)'].apply(lambda x: f"{x:.3f}")
    df_display['Savings %'] = df_display['Savings %'].apply(lambda x: f"{x:.0f}%")
    st.dataframe(df_display, use_container_width=True)


def show_about_page():
    st.markdown("## 📚 About Flight Redemption Optimizer")
    st.markdown("""
    ### 🎯 Our Mission
    We help travelers maximize the value of their miles and points by providing expert-backed
    recommendations and transparent analysis of redemption options.
   
    ### 🔧 How It Works
    1. **Search:** Enter your travel details and constraints
    2. **Analyze:** Our system searches for all available options (direct and layover)
    3. **Calculate:** We compute value-per-mile using multiple methods
    4. **Compare:** Results are compared to expert valuations
    5. **Rank:** Options are ranked by value and savings
   
    ### 📊 Expert Sources
    Our recommendations are benchmarked against:
    - **Sample Data:** Realistic flight scenarios for demonstration
    - **Value Calculator:** Multiple calculation methods
    - **Synthetic Routing:** Direct and layover route analysis
    - **Expert Comparison:** Published valuation integration
    """)
   
    st.markdown("### 📈 Value Categories")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **EXCELLENT (2.0+ cpm)**
        - Rare and highly sought after
        - Significantly above average
        - Top 10% of redemptions
       
        **GOOD (1.5-2.0 cpm)**
        - Solid value redemptions
        - Above expert average
        - Top 25% of redemptions
        """)
    with col2:
        st.markdown("""
        **FAIR (1.0-1.5 cpm)**
        - Acceptable but not outstanding
        - Near expert average
        - Standard redemptions
       
        **POOR (<1.0 cpm)**
        - Consider paying cash instead
        - Below expert average
        - Better to earn miles
        """)


if __name__ == "__main__":
    main()

