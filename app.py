import streamlit as st
import requests
import os

from image_processing import AmputationAngleCalculator

FirstName = os.environ.get('FIRSTNAME')
LastName = os.environ.get('LASTNAME')
api_url = f"https://cms.horusleg.com/api/collections/CV_Angles_{FirstName}_{LastName}/records"

st.title("Horus Prosthetics - Limb angle measurement")

st.write("Please follow the instructions below to collect data for angle measurement:")
st.write("1. You will take 2 pictures of your residual limb, natural leg, and prosthetic leg: one from the front and the other from the side (the limb side).")
st.write("2. Ensure you are in a weight-bearing stance for accurate measurements.")
st.write("3. Try to pose next to a structure perpendicular to the floor (a door edge for example).")

test_number = st.number_input("Test Number", min_value=1, help="Numerical value for test tracking")
col1, col2 = st.columns(2)
with col1:
    front_shot = st.file_uploader("Upload front capture", key="front", type=["jpg", "jpeg", "png"])
with col2:
    side_shot = st.file_uploader("Upload side capture", key="side", type=["jpg", "jpeg", "png"])

if front_shot and side_shot and test_number:

    front = AmputationAngleCalculator(front_shot)
    side = AmputationAngleCalculator(side_shot)

    front_landmarked = front.draw_landmarks()
    side_landmarked = side.draw_landmarks()

    col1, col2 = st.columns(2)
    with col1:
        st.image(front_landmarked, caption="Landmarks on front view", use_column_width=True)

    with col2:
        st.image(side_landmarked, caption="Landmarks on side view", use_column_width=True)

    if st.button("Calculate angles"):
        angle_front = front.calculate_angle()
        angle_side = side.calculate_angle()

        payload = {'abduction_angle': angle_front,
                   'flexion_angle': angle_side,
                   'any_data_as_file': 'yes' if front_shot or side_shot else 'no',
                   'test_number': test_number
                   }

        st.text(payload)
        st.text(f'Sending to: {api_url}')

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                st.success("Angles have been calculated and submitted successfully.")
            else:
                st.error("Failed to submit angles. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
