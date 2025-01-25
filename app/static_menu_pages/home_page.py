import streamlit as st

def homepage():
    st.title("🌱 SmartCrop")
    st.markdown("""
*Hello there, welcome to SmartCrop!*  
We’re thrilled to introduce you to our platform, designed to help you maximize your crop yield effortlessly. Powered by Artificial Intelligence, SmartCrop leverages real-time data to accurately predict yields and enable you to compare the performance of different crops on your land.  

### How Does It Work?  
It’s as simple as this:  
1.⁠ ⁠*Share your location.*  
2.⁠ ⁠*Select the crop you wish to grow.*  

*SmartCrop will do the rest!* Our AI engine provides precise yield predictions, allowing you to evaluate and compare various crops. We are also committed to promoting sustainable farming practices and do not encourage the use of pesticides. (Learn more about our mission on our Vision page.)  

### Ready to Start?  
Go to the menu and click on “Don't have an account?” to use the model and experience how SmartCrop can transform your farming:  

### Advanced Functionalities  
Looking for more features? Go to the menu and click on “My Data” to create your personal space in our community and save data. 
  
🌱 SmartCrop: Cultivating the future, today.   
""")
    st.markdown("""
    <div style="text-align: right;">
    Thank you from our team:<br>
    Cristina, Gabriele, and Alessandro.
    </div>
    """, unsafe_allow_html=True)