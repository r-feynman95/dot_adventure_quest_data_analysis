from application import app
from data_clean import LogFileProcessor
import pandas as pd

file = 'interactions.log'

processor = LogFileProcessor(file)
processor.process_file()

print(processor.df.head(10))


# if __name__ == "__main__":
#     app.run(debug = True)