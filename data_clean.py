import pandas as pd
import numpy as np

column_names = ["start", "duration", "ip_address", "user", "problem_status", "seed", "page", "response"]

df = pd.read_csv("interactions.log", 
                 names = column_names,
                 header = None,
                 usecols = range(8),    # use only first 8 occurences of seperator
                 quotechar= '"',        # final column can contain commas inside string
                 sep = ", "             # .log is not proper csv instead ", "
                 )

print(df.head(5)) # Print out the first 5 lines of the dataframe
print(df.dtypes)
# Find unique sessions
unique_sessions = df['start'].unique()

# Print the count and unique values
print(f"There were {len(unique_sessions)} unique sessions")

# Remove OpenLab IP Address 66.39.77.43
df = df[df['ip_address'] != '66.39.77.43']
df['response'] = df['response'].replace('"', np.nan)                        # replace empty response with NAN
df['response'] = df['response'].str.replace('^\"|\"$', '', regex=True)      # Remove quotes surrounding response

print(df.head(5)) # Print out the first 5 lines of the dataframe

# Find unique sessions
unique_sessions = df['start'].unique()

# Print the count and unique values
print(f"There were {len(unique_sessions)} unique sessions")

# Print the number of interaction in each session
interactions = df.groupby('start').size()
print(interactions)

# Filter out sessions that end after start 
df = df[df['start'].isin(interactions[interactions > 1].index)]
unique_sessions = df['start'].unique()

# Print the count and unique values
print(f"There were {len(unique_sessions)} unique sessions")
print(f"The data frame has {len(df)} entries")
