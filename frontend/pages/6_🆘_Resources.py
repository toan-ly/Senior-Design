import streamlit as st

from components.auth_guard import require_login
from components.sidebar import sidebar
from components.footer import footer


st.set_page_config(page_title="Resources", page_icon="🆘", layout="wide")
sidebar()

st.title("🆘 Mental Health Resources")

st.markdown(
    """
Mental support is a serious matter and **MedAssist is not clinically certified** to offer professional advice.  

If you or someone you know is struggling, in crisis, or needs professional care, please consider the resources below.
"""
)

st.divider()


# ----------------------------
# 🚨 Immediate Support
# ----------------------------
st.subheader("🚨 Immediate Support & Crisis Lines")

st.markdown(
    """
- **Emergency Medical Services**  
  Call **911 immediately**

- **988 Suicide & Crisis Lifeline**  
  Call or text **988**  
  🌐 https://988lifeline.org/

- **Crisis Text Line**  
  Text **HOME** to **741741**  
  🌐 https://www.crisistextline.org/

- **Veterans Crisis Line**  
  Call **988**, then press **1**  
  🌐 https://www.veteranscrisisline.net/
"""
)

st.divider()


# ----------------------------
# 🧑‍⚕️ Therapist Finder
# ----------------------------
st.subheader("🧑‍⚕️ Finding a Therapist or Counselor")

st.markdown(
    """
- **Psychology Today Therapist Finder**  
  🌐 https://www.psychologytoday.com/us/therapists  

- **Mental Health Match**  
  🌐 https://mentalhealthmatch.com/  

- **Open Path Psychotherapy Collective**  
  🌐 https://openpathcollective.org/  

- **Inclusive Therapists**  
  🌐 https://www.inclusivetherapists.com/
"""
)

st.divider()


# ----------------------------
# 🏥 Medical Care
# ----------------------------
st.subheader("🏥 Medical & Psychiatric Care")

st.markdown(
    """
- **NAMI HelpLine**  
  🌐 https://www.nami.org/help  

- **SAMHSA Treatment Locator**  
  🌐 https://findtreatment.gov/
"""
)

st.divider()


# ----------------------------
# 🤝 Support Groups
# ----------------------------
st.subheader("🤝 Support Groups")

st.markdown(
    """
- **Alcoholics Anonymous (AA)**  
  🌐 https://www.aa.org/

- **Narcotics Anonymous (NA)**  
  🌐 https://na.org/

- **SMART Recovery**  
  🌐 https://www.smartrecovery.org/
"""
)

st.divider()


# ----------------------------
# 📚 Other Resources
# ----------------------------
st.subheader("📚 Other Resources")

st.markdown(
    """
- **CDC Mental Health Resources**  
  🌐 https://www.cdc.gov/mental-health/caring/index.html  

- **National Institute of Mental Health (NIMH)**  
  🌐 https://www.nimh.nih.gov/  

- **Mayo Clinic Mental Health Overview**  
  🌐 https://www.mayoclinic.org/diseases-conditions  

- **Mental Health America Resource List**  
  🌐 https://mhanational.org/learn-about-your-mental-health/
"""
)

footer()
