![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

# 🌾 SmartCrop: agricultural yield predictor
This web application leverages Python and Streamlit to provide farmers and agricultural enthusiasts with insights into crop yield predictions. Built on a machine learning engine, the app combines data-driven predictions with user-friendly features to encourage sustainable farming practices.

## Features

1. **Crop Yield Prediction**: 
   - Get accurate predictions for your field's yield based on machine learning algorithms trained on agricultural datasets.

2. **User Authentication**:
   - **Login** and **registration** functionality with secure session management using cookies.

3. **Session Management**:
   - User sessions are maintained with cookies, ensuring a seamless experience across the platform.

4. **Sustainable Farming Recommendations**:
   - Receive personalized **seed suggestions** based on your location and field size.
   - Emphasis on **pesticide-free farming** as part of our vision for sustainable agriculture.

5. **Geolocation Integration**:
   - Automatically use your geographical location to tailor predictions and suggestions.

6. **Field Size Input and storage**:
   - Provide and save the size of your field to improve prediction accuracy and recommendations.

## Installation and Setup

#### Prerequisites
- Python 3.8+
- `pip` (Python package manager)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/cristinavisentin/CropML-data-driven-app.git
2. Navigate to the project directory:
    ```bash
    cd CropML-data-driven-app
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
4. Run the application:
    ```bash
    streamlit run app/app.py

## Vision and Commitment

Our mission is to empower farmers with cutting-edge technology while promoting sustainable agricultural practices. We believe in minimizing the ecological impact of farming, which is why we:

Provide seed suggestions tailored to your needs.

Actively discourage the use of pesticides, advocating for eco-friendly alternatives.

## Technologies Used

Python: Core programming language.

Streamlit: Framework for building the web interface.

Machine Learning: Custom ML engine for predictions.

Geolocation API: For location-based recommendations.