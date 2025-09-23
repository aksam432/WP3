import pytest
import yaml
import pandas as pd

canonical_yaml="../canonical_schema.yml"
excel_schema="../Schema/DB_scheme.xlsx"




def excel_to_keys():
    # Load the Excel file
    df = pd.read_excel(excel_schema)
   
    # Get the second column (row index 2)
    row = df.iloc[:,2]
    
    # Get first column
    col_1 = df.iloc[4:,1]
#    print(set(col_1.to_list()))

    # Get column as a list
    row_values = row.tolist()
    

    # Add an extra key to match canonical form 
    row_values.append('model_metadata')
  
    return set(row_values)


def get_canonical_keys():

    with open(canonical_yaml,'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    l=[]
    for k in data.keys():
        for elem in data[k].keys():
            l.append(elem)
#        l.append(k)  
    
    return set(l)



def test_schema(tmp_path):
    """ test to verify that excel and canonical_schema are same """

    ex_scheme= excel_to_keys()
    can_scheme= get_canonical_keys()
    assert  can_scheme.issubset(ex_scheme)
