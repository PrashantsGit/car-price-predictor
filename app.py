import streamlit as st
import pickle
import numpy as np



@st.cache_resource
def load_model():
    with open("final_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()


insurance_map = {
    'Comprehensive': 0,
    'Third Party insurance': 1,
    'Third Party': 1,
    'Zero Dep': 2,
    'Not Available': 3
}

fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}

owner_map = {
    'First Owner': 1,
    'Second Owner': 2,
    'Third Owner': 3,
    'Fourth Owner': 4,
    'Fifth Owner': 5
}

transmission_map = {'Manual': 0, 'Automatic': 1}

st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)


st.markdown(
    "<h1 style='text-align: center;'>🚗 Used Car Price Predictor</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: grey;'>Get an instant estimate of your car's resale value</p>",
    unsafe_allow_html=True
)

st.markdown("---")


with st.container():

    st.subheader("🔍 Enter Car Details")

    col1, col2 = st.columns(2)

    with col1:
        insurance = st.selectbox("Insurance Type", list(insurance_map.keys()))
        fuel = st.selectbox("Fuel Type", list(fuel_map.keys()))
        owner = st.selectbox("Ownership", list(owner_map.keys()))

    with col2:
        transmission = st.selectbox("Transmission", list(transmission_map.keys()))
        kms_driven = st.slider("Kilometers Driven", 0, 300000, 50000)


st.markdown("")

if st.button("🚀 Predict Price", use_container_width=True):

    try:
        # Encode inputs
        input_data = np.array([[
            insurance_map[insurance],
            fuel_map[fuel],
            kms_driven,
            owner_map[owner],
            transmission_map[transmission]
        ]])

        prediction = model.predict(input_data)[0]

        # Result Card
        st.markdown("---")

        st.markdown(
            f"""
            <div style="
                background-color:#f0f2f6;
                padding:20px;
                border-radius:10px;
                text-align:center;">
                <h2>💰 Estimated Price</h2>
                <h1 style="color:green;">₹ {prediction:.2f} Lakhs</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        
        if prediction < 5:
            st.info("💡 Budget Segment Car")
        elif prediction < 15:
            st.info("💡 Mid-range Car")
        else:
            st.info("💡 Premium Car")

    except Exception as e:
        st.error(f"Error: {e}")


st.markdown("---")
st.caption("Built with Streamlit | ML Project")