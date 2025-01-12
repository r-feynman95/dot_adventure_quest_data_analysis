import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogFileProcessor:
  
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.meta_info = {}
    
    def process_file(self):
        column_names = [
            "start", "duration", "ip_address", "user", 
            "problem_status", "seed", "page", "response",
        ]

        # Load .log file
        logger.info("Loading the .log file")
        self.df = pd.read_csv(
                    self.file_path, 
                    names = column_names,
                    header = None,
                    usecols = range(8),    
                    quotechar= '"',        
                    sep = ", ", # Handle none standard CSV delimiter
                    )

        # Basic data cleaning
        logger.info("Perfoming initial cleaning")
        self.df = self.df[self.df['ip_address'] != '66.39.77.43']  # Remove admin ip interaction
        self.df['response'] = self.df['response'].replace('"', np.nan)                        
        self.df['response'] = self.df['response'].str.replace('^\"|\"$', '', regex=True)             

        # Unique Sessions analysis
        total_unique_sessions = len(self.df['start'].unique())
        self.meta_info['total_unique_sessions'] = len(total_unique_sessions)
        logger.info(f"There were {len(total_unique_sessions)} unique sessions")

        # Session Interactions
        logger.info("Adding distribution of all interactions")
        interactions_distribution = self.df.groupby('start').size()
        self.meta_info['interactions_distribution'] = interactions_distribution
        

        # Filter out sessions that end after start 
        df = df[df['start'].isin(interactions[interactions > 1].index)]
        student_analysis_unique_sessions = df['start'].unique()

    # Total number of unique session longer than 1 interaction
    print(f"There were {len(student_analysis_unique_sessions)} unique sessions")
    print(f"The data frame has {len(df)} entries after removing single interaction sessions")

    # Replace all user information by lowercased email if availible
    df['user'] = df.groupby('start')['user'].transform(
        lambda x: x if x.iloc[-1] == 'student' else x.iloc[-1].lower()
    )
    # Update all user information of shared ip_address
    df['user'] = df.groupby('ip_address')['user'].transform(
        lambda x: x[x.str.contains('@', na=False)].iloc[0] if (x.str.contains('@', na=False)).any() else x
    )

    # Replace all student users with ip_address
    df['user'] = df.groupby('ip_address')['user'].transform(
        lambda x: x.iloc[0] if ~(x.str.contains('@', na=False)).any() else x
    )

    # Anonymize Users
    df['user'] = df.groupby('user').ngroup()

    # Define the patterns
    problem_type_pattern = r"\/([^\/]+)\.pg$"
    problem_number_pattern = r"/S([0-9]+)E[0-9]+/"

    # Extract the problem type and problem number using str.extract
    df['problem_type'] = df['page'].str.extract(problem_type_pattern)[0]
    df['problem_number'] = df['page'].str.extract(problem_number_pattern)[0].astype(int)
    df = df.drop(columns=['page'])

    #print(f"The data frame has {len(df)} entries before double credit removal")

    # How many credit requests are there 
    #print(f" There are {(df['problem_status'] == 'creditRequest').sum()} credit requests")

    # Remove double credit requests
    """
    The lambda function filters the problem_status column for only the rows that contain credit request then
    selects the first row (occurence) using the .index[0] . After this the .loc() function selects all rows 
    in each group up to this first occurence. If the group contains no 'creditRequest' return the group unchanged.
    """
    df = df.groupby(['start', 'seed'], group_keys=False).apply(
        lambda group: group.loc[:group[group['problem_status'] == 'creditRequest'].index[0]]   
        if (group['problem_status'] == 'creditRequest').any() 
        else group
    )

    #print(f"The data frame has {len(df)} entries after double credit removal")
    df = df.drop(columns = ['ip_address'])
    new_order = ["user", "start", "duration", "seed", 'problem_number', "problem_type", "problem_status", "response"]
    df = df[new_order]
    df = df.sort_values(by=['user', 'start', 'duration'], ascending=[True, True, True])
    df = df.reset_index(drop=True)

    #print(df.head(50))

    # Total number of unique users 
    print(f"The total number of unique users is {df['user'].nunique()}")



