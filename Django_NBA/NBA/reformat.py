import pandas as pd
from NBA.name_enums import DfColumnNames,TableColumnNames

def reformat(df,id_name):
    df1 = df[[ DfColumnNames.GAME_ID.value,id_name,DfColumnNames.GAME_DATE.value,DfColumnNames.WL.value]]
    df2 = df[[id_name,DfColumnNames.GAME_ID.value]] 
    merged = pd.merge(df1,df2,on = DfColumnNames.GAME_ID.value)
    merged = merged[merged[id_name+"_x"] != merged[id_name+"_y"]]
    merged.drop_duplicates(subset = DfColumnNames.GAME_ID.value,inplace = True)
    merged = merged.dropna()
    return merged

