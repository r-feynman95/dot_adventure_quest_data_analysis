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
        self.df['response'] = self.df['response'].replace('"', np.nan)  # Remove internal quotes in responses                        
        self.df['response'] = self.df['response'].str.replace('^\"|\"$', '', regex=True)             

        # Unique Sessions analysis
        total_unique_sessions = len(self.df['start'].unique())
        self.meta_info['total_unique_sessions'] = total_unique_sessions
        logger.info(f"There were {total_unique_sessions} unique sessions")

        # Session Interactions
        logger.info("Adding distribution of all interactions to meta_info")
        interactions = self.df.groupby('start').size()
        self.meta_info['interactions_distribution'] = interactions
        
        # Filter out sessions that end after start 
        self.df = self.df[self.df['start'].isin(interactions[interactions > 1].index)]
        student_analysis_unique_sessions = len(self.df['start'].unique())
        
        self.meta_info['student_analysis_unique_sessions'] = student_analysis_unique_sessions

        logger.info(f"There were {student_analysis_unique_sessions} unique student sessions")
        logger.info(f"The data frame has {len(self.df)} entries after cleaning")

        self._anonymize_users()
        self._extract_problem_data()
        self._remove_double_credits()
        self._reformat()

    def _anonymize_users(self):
        # Replace all user information by lowercased email if availible
        self.df['user'] = self.df.groupby('start')['user'].transform(
            lambda x: x if x.iloc[-1] == 'student' else x.iloc[-1].lower()
        )
        # Update all user information of shared ip_address
        self.df['user'] = self.df.groupby('ip_address')['user'].transform(
            lambda x: x[x.str.contains('@', na=False)].iloc[0] if (x.str.contains('@', na=False)).any() else x
        )

        # Replace all student users with ip_address
        self.df['user'] = self.df.groupby('ip_address')['user'].transform(
            lambda x: x.iloc[0] if ~(x.str.contains('@', na=False)).any() else x
        )

        # Anonymize Users
        self.df['user'] = self.df.groupby('user').ngroup()

        logger.info("Users anonymized")

    def _extract_problem_data(self):
        # Define the patterns
        problem_type_pattern = r"\/([^\/]+)\.pg$"
        problem_number_pattern = r"/S([0-9]+)E[0-9]+/"

        # Extract the problem type and problem number using str.extract
        self.df['problem_type'] = self.df['page'].str.extract(problem_type_pattern)[0]
        self.df['problem_number'] = self.df['page'].str.extract(problem_number_pattern)[0].astype(int)
        self.df = self.df.drop(columns=['page'])

        logger.info("Problem type and number seperated")

    def _remove_double_credits(self):
        """
        Removes double credit requests
         
        Lambda function filters the problem_status column of each group for rows that contain credit request,
        selects the first row (occurence) using the .index[0], then the .loc() function selects all rows 
        in each group up to this first occurence. If the group contains no 'creditRequest' return the group unchanged.
        """
        temp_size = len(self.df)

        self.df = self.df.groupby(['start', 'seed'], group_keys=False).apply(
            lambda group: group.loc[:group[group['problem_status'] == 'creditRequest'].index[0]]   
            if (group['problem_status'] == 'creditRequest').any() 
            else group
        )

        logger.info("Double Credit Requests clenaed")
        logger.info(f"The data frame is now of size {temp_size - len(self.df)}")

    def _reformat(self):
        new_order = ["user", "start", "duration", "seed", 'problem_number', "problem_type", "problem_status", "response"]

        self.df = self.df.drop(columns = ['ip_address'])
        self.df = self.df[new_order]
        self.df = self.df.sort_values(by=['user', 'start', 'duration'], ascending=[True, True, True])
        self.df = self.df.reset_index(drop=True)

        unique_users = self.df['user'].nunique()
        logger.info(f"The total number of unique users is {unique_users}")
        self.meta_info['unique users'] = unique_users




