import streamlit as st
from linkedin_api import Linkedin
import re

st.set_page_config(layout='wide')
def linkedin_id_extrator(linkedin_url:str)-> str:
    """
    Gives the LinkedIn id from URL if matches
    """
    pattern = r'in/([^/]+)'
    match = re.search(pattern, linkedin_url)
    
    if match:
        result = match.group(1)
        return result

@st.cache_data(ttl=600)
def linkedin_authenticator(Linkedin_email:str,password:str) -> object:

    return  Linkedin(Linkedin_email, password)

def main():
    st.title("LinkedIn profile extractor")
    col1,col2=st.columns(2)
    with col1:
        Linkedin_email=st.text_input("Enter your LinkedIn email:")

    with col2:
        Linkedin_pwd=st.text_input("Enter your LinkendIn Password:",type='password')


    if Linkedin_email and Linkedin_pwd:
        # Authenticate using any Linkedin account credentials
        api = Linkedin(Linkedin_email, Linkedin_pwd)

        st.success("Authentication Completed!")

        linkedin_profile_url=st.text_input("Enter LinkedIn profile URL:")

        if linkedin_profile_url:
            
            #get the userid from LinkedIn profile URL 
            userid=linkedin_id_extrator(linkedin_profile_url)

            if userid!="":

                #get the LinkedIn details 
                profile = api.get_profile(userid)

                #get About info
                st.header(f"About")
                st.text(profile['summary'])

                st.markdown('---')
                st.header("Skills")
                for skill_no in range(0,len(profile['skills'])):
                    st.text(profile['skills'][skill_no]['name'])
                
                st.markdown('---')



                st.header("Work Experience")
                for i in range(0,len(profile['experience'])):
                    experience=profile['experience'][i]
                    time_duration = experience['timePeriod']
                    start_time = time_duration['startDate']
                    start_date_text = f"Started: {start_time['month']}/{start_time['year']}"

                    end_date_text = (
                        f"Ended: {time_duration['endDate']['month']}/{time_duration['endDate']['year']}"
                        if 'endDate' in time_duration
                        else "Ongoing"
                    )

                    st.info(f"""
                    **Company name:** {experience['companyName']}
                    
                    **Title:** {experience['title']}
                    
                    **{start_date_text}**
                    
                    **{end_date_text}**
                    """)


                # st.json(profile)



if __name__=="__main__":
    main()
