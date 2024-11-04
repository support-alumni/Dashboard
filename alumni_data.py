import json
import pandas as pd
import requests
import boto3


#Function to read JSON files from API
def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except Exception as e:
        raise Exception(f"Reading {filename} file encountered an error: {str(e)}")
    return data

def create_dataframe(data: list) -> pd.DataFrame:
    # Normalize the JSON data within "students" key to flatten it
    dataframe = pd.json_normalize(data, sep='_')
    return dataframe
 
#Function for connecting to EC2 (used my personal account)
ec2 = boto3.client('ec2',
                   'ap-east',
                   aws_access_key_id='AKIAU6GD2NWS2XKAPLPC',
                   aws_secret_access_key='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')

#API call to retrive some of engineering alumni (personal key)
api_key = 'MCskBT_zYEYIEoCrl-Q5Hg'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/school/students/'
params = {
    'linkedin_school_url': 'https://www.linkedin.com/school/northtexas',
    'country': 'us',
    'enrich_profiles': 'enrich',
    'search_keyword': 'computer science|computer engineering|information technology|electrical engineering|mechanical engineering|civil engineering|Material Science|Material Engineering|biomedical engineering',
    'page_size': '10',
    'student_status': 'past',
    'sort_by': 'recently-matriculated',
    'resolve_numeric_id': 'false',
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)

def save_to_rds(dataframe: pd.DataFrame, table_name: str, db_uri: str):
    try:
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data saved to {table_name} in RDS successfully.")
    except Exception as e:
        raise Exception(f"Error saving data to RDS: {str(e)}")


db_uri = 'unt-eng-alumni-db.c30ysygymhtq.us-east-1.rds.amazonaws.com'



def main():
    # Read the JSON file as a Python dictionary
    data = read_json(response)
    
    # Access the "students" key within the JSON structure
    if 'students' in data:
        dataframe = create_dataframe(data=data['students'])
        
        # Initialize lists to collect education and experience data
        education_records = []
        experience_records = []

        # Process 'profile_education' and 'profile_url' together
        for index, entry in dataframe.iterrows():
            try:
                # Process education data
                education_data = entry['profile_education']
                if isinstance(education_data, str):
                    education_data = json.loads(education_data)

                # Collect education entries along with the corresponding profile_url
                for edu in education_data:
                    education_records.append({
                        'profile_url': entry['profile_url'],
                        'profile_full_name': entry['profile_full_name'],
                        **edu  # Unpack the education fields
                    })
            except Exception as e:
                print(f"Error parsing 'profile_education' entry: {e}")

        # Create DataFrame from the collected education records
        education_df = pd.DataFrame(education_records)

        # Process 'profile_experiences' similarly if needed
        for index, entry in dataframe.iterrows():
            try:
                experience_data = entry['profile_experiences']
                if isinstance(experience_data, str):
                    experience_data = json.loads(experience_data)

                # Collect experience entries along with the corresponding profile_url
                for exp in experience_data:
                    experience_records.append({
                        'profile_url': entry['profile_url'],
                        **exp  # Unpack the experience fields
                    })
            except Exception as e:
                print(f"Error parsing 'profile_experiences' entry: {e}")

        experience_df = pd.DataFrame(experience_records)

       
    else:
        print("Key 'students' not found in the JSON file.")

    save_to_rds(dataframe, 'tbl_alumni', db_uri)
    save_to_rds(education_df, 'tbl_education', db_uri)
    save_to_rds(experience_df, 'tbl_experience', db_uri)

if __name__ == "__main__":
    main()