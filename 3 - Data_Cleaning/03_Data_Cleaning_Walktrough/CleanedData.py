import pandas as pd
import re


data_files = [
"https://raw.githubusercontent.com/TomazFilgueira/Dq_Datascientist/refs/heads/main/3%20-%20Data_Cleaning/03_Data_Cleaning_Walktrough/data/ap_2010.csv",
"https://raw.githubusercontent.com/TomazFilgueira/Dq_Datascientist/refs/heads/main/3%20-%20Data_Cleaning/03_Data_Cleaning_Walktrough/data/class_size.csv",
"https://raw.githubusercontent.com/TomazFilgueira/Dq_Datascientist/refs/heads/main/3%20-%20Data_Cleaning/03_Data_Cleaning_Walktrough/data/demographics.csv",
"https://raw.githubusercontent.com/TomazFilgueira/Dq_Datascientist/refs/heads/main/3%20-%20Data_Cleaning/03_Data_Cleaning_Walktrough/data/graduation.csv",
"https://raw.githubusercontent.com/TomazFilgueira/Dq_Datascientist/refs/heads/main/3%20-%20Data_Cleaning/03_Data_Cleaning_Walktrough/data/hs_directory.csv",
"https://raw.githubusercontent.com/TomazFilgueira/Dq_Datascientist/refs/heads/main/3%20-%20Data_Cleaning/03_Data_Cleaning_Walktrough/data/sat_results.csv",
]
data = {}

for d in data_files:
    file = pd.read_csv(d)
    #get "name" without .csv
    name = d.rsplit('data/')[1]
    name = name.replace(".csv", "")
    data[name]=file
    
#survey files    
data_files = [
"https://raw.githubusercontent.com/TomazFilgueira/Dq_Datascientist/refs/heads/main/3%20-%20Data_Cleaning/03_Data_Cleaning_Walktrough/data/survey_all.txt",
"https://raw.githubusercontent.com/TomazFilgueira/Dq_Datascientist/refs/heads/main/3%20-%20Data_Cleaning/03_Data_Cleaning_Walktrough/data/survey_d75.txt",
]

all_survey = pd.read_csv(data_files[0],delimiter="\t",encoding="windows-1252")
d75_survey = pd.read_csv(data_files[1],delimiter="\t",encoding="windows-1252")    
    
survey = pd.concat([all_survey,d75_survey],axis=0)

survey = survey.copy()
survey['DBN'] = survey['dbn']

cols = ["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]

#Filter survey so it only contains the columns we listed above
survey = survey[cols]

#Assign the dataframe survey to the key survey in the dictionary data.
data['survey'] = survey

#================================================================
data['hs_directory']['DBN'] = data['hs_directory']['dbn']

#===============================================================
#if string is 2 digits long - return the string
#if string is less than 2 digits - fills with 0 in the front
data['class_size']['padded_csd'] = data['class_size']['CSD'].apply(lambda x: str(x).zfill(2))
data['class_size']['DBN'] =  data['class_size']['padded_csd'] + data['class_size']['SCHOOL CODE']

#convert to numeric data
data['sat_results']['SAT Math Avg. Score'] = pd.to_numeric(data['sat_results']['SAT Math Avg. Score'],errors="coerce")

data['sat_results']['SAT Critical Reading Avg. Score'] = pd.to_numeric(data['sat_results']['SAT Critical Reading Avg. Score'],errors="coerce")

data['sat_results']['SAT Writing Avg. Score']= pd.to_numeric(data['sat_results']['SAT Writing Avg. Score'],errors="coerce")

#sum up all the three columns
data['sat_results']['sat_score'] = data['sat_results']['SAT Math Avg. Score'] + data['sat_results']['SAT Critical Reading Avg. Score'] + data['sat_results']['SAT Writing Avg. Score']


#==============================================================
def get_lat(x):
    #extract raw coordinates
    y = re.findall("\(.+\)", x)
    
    #split lat and lon. remove '(' for latitude
    lat = y[0].split(',')[0].replace("(","")
    return lat

def find_lon(x):
    #extract raw coordinates
    y = re.findall("\(.+\)", x)
    
    #split lat and lon. remove ')' for longitude
    lon = y[0].split(',')[1].replace(")","").strip()
    return lon

data['hs_directory']['lon'] = data['hs_directory']['Location 1'].apply(find_lon)
data['hs_directory']['lat'] = data['hs_directory']['Location 1'].apply(get_lat)


#convert coordinates to numeric
data["hs_directory"]["lat"] = pd.to_numeric(data["hs_directory"]["lat"], errors="coerce")
data["hs_directory"]["lon"] = pd.to_numeric(data["hs_directory"]["lon"], errors="coerce")


class_size = data["class_size"]
#Filter class_size so the GRADE = 09-12
#Filter class_size so that the PROGRAM = GEN ED
class_size = class_size[ (class_size["GRADE "]=="09-12") & (class_size["PROGRAM TYPE"]=="GEN ED")]

#################################################
data['demographics'] =data['demographics'][data['demographics']['schoolyear']==20112012]

##################################################
data['graduation'] = data['graduation'][(data['graduation']['Cohort']=="2006") & (data['graduation']['Demographic']=='Total Cohort')]

######################################################
cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

for c in cols:
    data['ap_2010'][c] = pd.to_numeric(data['ap_2010']  [c],errors="coerce")

#####################################################
combined = data["sat_results"]

#merge with ap_2010
combined = combined.merge(data["ap_2010"],how="left",on="DBN")

#merge with "graduation"
combined = combined.merge(data["graduation"],how="left",on="DBN")

#merge with class_size
combined = combined.merge(data["class_size"],how="inner",on="DBN")

#merge with demographics
combined = combined.merge(data["demographics"],how="inner",on="DBN")

#merge with survey
combined = combined.merge(data["survey"],how="inner",on="DBN")

#merge with hs_directory
combined = combined.merge(data["hs_directory"],how="inner",on="DBN")

#########################################################
#fill NAN with mean for each column
mean = combined.mean(numeric_only=True)
combined.fillna(mean)

#fill remaining NAN with 0
combined = combined.infer_objects(copy=False).fillna(0)

##########################################################
#extract first two digits
combined['school_dist'] = combined['DBN'].apply(lambda x:x[0:2])



