def reformat(df,id_name):
    df1 = df[["GAME_ID",id_name,"GAME_DATE","WL"]]
    df2 = teams_df[[id_name,"GAME_ID"]]
    merged = pd.merge(df1,df2,on = "GAME_ID")
    merged = merged[merged[id_name+"_x"] != merged[id_name+"_y"]]
    merged.drop_duplicates(subset = "GAME_ID",inplace = True)
    merged = merged.dropna()
    return merged

