#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:01:04 2023

@author: zhongyuanchen
"""

import getGames
import writeGames

date_range = ["2000-00-00","9999-99-99"]
df = getGames.get_range(date_range)

host = "mydemodb.c6ttcyoyckbo.us-east-2.rds.amazonaws.com"
user = "admin"
password = "mynbaproject"
database = "mydemodb"
port = 3306

#writeGames.write_to_db(df = df,database = db, user = user, password = password, host = host)
writeGames.get_connection(user, password, host, port, databse)
print("Finished")