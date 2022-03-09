#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 17:48:36 2022

@author: hancalki
"""

import pandas as pd

file=pd.read_csv("/Users/hancalki/Documents/UMLS Mappings/FITBIR_demographics_mapping_explode_new2.csv")


file=file.fillna(' ')

new_df=file[['variable_name', 'permissible_values','permissible_value_descriptions','result_name','cui','url']].copy()

pvd=new_df.groupby(['variable_name', 'permissible_values'])['permissible_value_descriptions'].agg(';'.join).reset_index(name='permissible_value_descriptions')

cui=new_df.groupby(['variable_name', 'permissible_values'])['cui'].agg(';'.join).reset_index(name='cui')

url=new_df.groupby(['variable_name', 'permissible_values'])['url'].agg(';'.join).reset_index(name='url')

result=new_df.groupby(['variable_name', 'permissible_values'])['result_name'].agg(';'.join).reset_index(name='result_name')

temp1 = pd.merge(pvd, cui, on=["variable_name","permissible_values"])

temp2 = pd.merge(temp1, url, on=["variable_name","permissible_values"])

final = pd.merge(temp2, result, on=["variable_name","permissible_values"])


#output dataframe to csv
final.to_csv('/Users/hancalki/Documents/UMLS Mappings/final_mapping.csv')