import streamlit as st
import requests
import os

from image_processing import AngleCalculator

FirstName = os.environ.get('FIRSTNAME')
LastName = os.environ.get('LASTNAME')

# Streamlit interface
st.title("Horus Prosthetics - Angle Measurement")

# Instructions for users
st.write("Please follow the instructions below to collect data for angle measurement:")
st.write("1. You will take 2 pictures of your residual limb, natural leg, and prosthetic leg: \
    one from the front and the other from the side (the limb side).")
st.write("2. Ensure you are in a weight-bearing stance for accurate measurements.")
st.write("3. Try to pose next to a structure perpendicular to the floor (a door edge for example).")

# User input for test information
test_number = st.number_input("Test Number", min_value=1, help="Numerical value for test tracking")

# User input for file upload
front_shot = st.file_uploader("Upload front capture", key="front", type=["jpg", "jpeg", "png"])
side_shot = st.file_uploader("Upload side capture", key="side", type=["jpg", "jpeg", "png"])

if front_shot and side_shot and test_number:
    # Display the uploaded front and side images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(front_shot, use_column_width=True, caption="Front capture")
    with col2:
        st.image(side_shot, use_column_width=True, caption="Side capture")

    front_angle_calculator = AngleCalculator(image_path=front_shot)
    side_angle_calculator = AngleCalculator(image_path=side_shot)

    if front_angle_calculator and side_angle_calculator:

        col1, col2 = st.columns(2)
        with col1:
            front_kp = front_angle_calculator. visualize_keypoints()
            st.image(front_kp, use_column_width=True, caption="Front capture with keypoints", channels="BGR")
        with col2:
            side_kp = side_angle_calculator. visualize_keypoints()
            st.image(side_kp, use_column_width=True, caption="Side capture with keypoints", channels="BGR")

        if st.button("Calculate Angles"):

            front_lines, front_angle = front_angle_calculator.calculate_angle()
            side_lines, side_angle = side_angle_calculator.calculate_angle()

            col1, col2 = st.columns(2)
            with col1:
                st.image(front_lines, use_column_width=True, caption="Front capture with lines", channels="BGR")
            with col2:
                st.image(side_lines, use_column_width=True, caption="Side capture with lines", channels="BGR")

            payload = {'abduction_angle': front_angle,
                       'flexion_angle': side_angle,
                       'any_data_as_file': (front_lines, side_lines),
                       'test_number': test_number
                       }

            if front_angle is not None:
                st.text(f'abduction_angle: {payload.get("abduction_angle")}')
            if front_angle is not None:
                st.text(f'flexion_angle: {payload.get("flexion_angle")}')

            api_url = f"https://cms.horusleg.com/api/collections/CV_Angles_{FirstName}_{LastName}/records"
            # response = requests.post(api_url, json=payload)

            # if response.status_code == 200:
            #     st.success("Angles have been calculated and submitted successfully.")
            # else:
            #     st.error("Failed to submit angles. Please try again.")

            st.text(f'Sending to:{api_url})')
