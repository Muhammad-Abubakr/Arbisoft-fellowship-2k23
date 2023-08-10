import pandas as pd
import logging
import os

printd = logging.debug

logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s : %(asctime)s\n%(message)s',
    datefmt='%Y-%M-%d %H:%M')

file: pd.DataFrame = pd.read_csv(
    os.path.join(os.getcwd(), 'tasks', 'pandas', 'sample.csv'))

mydataset = {
    'cars': ["BMW", "Volvo", "Ford"],
    'passings': [3, 7, 2]
}

calories = {"day1": 420, "day2": 380, "day3": 390}

# file.mean('index')
# logging.debug(file)
# df = pd.DataFrame(mydataset)
# printd(df.loc[0])
# printd(pd.Series(calories))
# printd(pd.Series(mydataset))
# printd(pd.Series(mydataset['passings'], index=[1, 2, 3]))
printd(pd.__version__)

df = pd.DataFrame(mydataset)
print(df.loc[0])