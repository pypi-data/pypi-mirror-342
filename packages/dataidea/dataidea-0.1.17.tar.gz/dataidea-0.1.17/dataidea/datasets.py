from pathlib import Path
import pandas as pd

def load_dataset(name:str=None, inbuilt=True, file_type:str=None):
    '''
    Easily load datasets that are inbuit in DATAIDEA

    parameters:
    name: this is the name of the dataset, eg demo, fpl, music, titanic etc
    inbuilt: boolean to specify whether data is from DATAIDEA or custom data
    type: specifies the type of the dataset eg 'csv', 'excel' etc

    '''

    if inbuilt:
        package_dir = Path(__file__).parent
        data_path = package_dir / 'datasets' / f'{name}.csv'
        return pd.read_csv(data_path)

    if file_type == None:
        raise TypeError('The file type was not specified')
    
    if file_type == 'csv':
        return pd.read_csv(name)
    
    if file_type == 'excel':
        return pd.read_excel(name)



