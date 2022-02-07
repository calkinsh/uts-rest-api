#################################################################################
# usage of the script
# usage: python search-terms.py -k APIKEY -v VERSION -s STRING
# see https://documentation.uts.nlm.nih.gov/rest/search/index.html for full docs
# on the /search endpoint
#################################################################################

from __future__ import print_function
from Authentication import *
import requests
import json
import argparse
import pandas as pd
from io import StringIO



parser = argparse.ArgumentParser(description='process user given parameters')
#parser.add_argument("-u", "--username", required =  True, dest="username", help = "enter username")
#parser.add_argument("-p", "--password", required =  True, dest="password", help = "enter passowrd")
parser.add_argument("-k", "--apikey", required = True, dest = "apikey", help = "enter api key from your UTS Profile")
parser.add_argument("-v", "--version", required =  False, dest="version", default = "current", help = "enter version example-2015AA")
parser.add_argument("-s", "--string", required =  True, dest="string", help = "enter a search term, like 'diabetic foot'")

args = parser.parse_args()
#username = args.username
#password = args.password
apikey = args.apikey
version = args.version
string = args.string
uri = "https://uts-ws.nlm.nih.gov"
content_endpoint = "/rest/search/"+version
##get at ticket granting ticket for the session
AuthClient = Authentication(apikey)
tgt = AuthClient.gettgt()
pageNumber=0

base=pd.read_csv("/Users/hancalki/Documents/UMLS Mappings/FITBIR_demographics_mapping_explode_new2.csv")


columnSeriesObj = base['permissible_value_descriptions']
#print('Column Contents : ', columnSeriesObj.values)

#comment out print statement, we want to write to a variable which can get written to a file

# for y in columnSeriesObj.values: 
#         x=y.strip()
#         ##generate a new service ticket for each page if needed
#         ticket = AuthClient.getst(tgt)
#         pageNumber += 1
#         query = {'string':x,'ticket':ticket, 'pageNumber':pageNumber, 'searchType':'exact'}
#         #query['includeObsolete'] = 'true'
#         #query['includeSuppressible'] = 'true'
#         #query['returnIdType'] = "sourceConcept"
#         #query['sabs'] = "SNOMEDCT_US"
#         r = requests.get(uri+content_endpoint,params=query)
#         r.encoding = 'utf-8'
#         items  = json.loads(r.text)
#         jsonData = items["result"]
        
#         #print (json.dumps(items, indent = 4))
        
#         for result in jsonData["results"]:
          
#           try:
#             print(str(len(items["result"]["results"]))+'\t' + x +'\t'+ result["name"] +'\t' + result["ui"] + '\t' + "https://uts.nlm.nih.gov/uts/umls/concept/"
#                   + result["ui"]  )
#           except:
#             NameError

#         ##Either our search returned nothing, or we're at the end
#         if jsonData["results"][0]["ui"] == "NONE":
#             break
#         pageNumber=0


#define text variable with headers 

lis="count \t value \t result_name \t cui \t url \n "

#incrimentally append new search values to text string        
for y in columnSeriesObj.values: 
        x=y.strip()
        ##generate a new service ticket for each page if needed
        ticket = AuthClient.getst(tgt)
        pageNumber += 1
        #searchType= exact match to get rid of excessive results
        query = {'string':x,'ticket':ticket, 'pageNumber':pageNumber, 'searchType':'exact'}
        #query['includeObsolete'] = 'true'
        #query['includeSuppressible'] = 'true'
        #query['returnIdType'] = "sourceConcept"
        #query['sabs'] = "SNOMEDCT_US"
        r = requests.get(uri+content_endpoint,params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        jsonData = items["result"]
        
        #print (json.dumps(items, indent = 4))
        
        for result in jsonData["results"]:
        #print number of results matching that field at start so easy to filter for items with more than one match returned  
        #check if there is a "none" result and if so, set number of results as 0
          if jsonData["results"][0]["ui"] == "NONE":
              lis=lis+("0"+'\t' + x +'\t'+ result["name"] +'\t' + result["ui"] + '\t' + "none" + '\n' )
          else:
              try:
                  lis=lis+(str(len(items["result"]["results"]))+'\t' + x +'\t'+ result["name"] +'\t' + result["ui"] + '\t' + "https://uts.nlm.nih.gov/uts/umls/concept/"
                      + result["ui"] + '\n' )
              except:
                NameError

        ##Either our search returned nothing, or we're at the end
       # if jsonData["results"][0]["ui"] == "NONE":
        #    break
        pageNumber=0        

#read string into dataframe
new_df=pd.read_csv(StringIO(lis), sep='\t', header=0)

#output dataframe to csv
new_df.to_csv('/Users/hancalki/Documents/UMLS Mappings/FITBIR_demographics_mapping_umls_test.csv')
    
    

