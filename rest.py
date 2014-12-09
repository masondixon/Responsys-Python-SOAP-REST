'''
Created on Nov 5, 2014
@author: mdixon
'''

import requests
import json
import logging
import sys


class rest_api(object):
    
    Auth_Token = None
    End_Point  = None
    Login_Url  = None
    Logged_In  = False
    
    Service_Url = '/rest/api/v1/auth/token'
    List_Service_Url = '/rest/api/v1/lists/'
    
    Trigger_Service_Url = '/rest/api/v1/campaigns/'
    Trigger_SMS_Service_Url = '/sms'
    Trigger_EMAIL_Service_Url = '/email'
    

    def __init__(self, debug=False):
        if debug is not False:
            # Taken from stack overflow - love you guys
            # These two lines enable debugging at httplib level (requests->urllib3->http.client)
            # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
            # The only thing missing will be the response.body which is not logged.
            try:
                import http.client as http_client
            except ImportError:
                # Python 2
                import httplib as http_client
            http_client.HTTPConnection.debuglevel = 1
            
            # You must initialize logging, otherwise you'll not see debug output.
            logging.basicConfig() 
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
            
            
    '''
    API Methods
    '''
        
    def login(self, login_url, login, password):
        
        payload = {'user_name': login, 'auth_type': 'password', 'password': password}
        login_request = requests.post( login_url + self.Service_Url, params=payload)
        response = login_request.json()
        
        try:
            self.Auth_Token = response['authToken']
            self.End_Point  = response['endPoint']
            
            if self.Auth_Token is not None:
                print(response)
                self.Logged_In = True
                
        except KeyError as key_error:
            '''
            If we cant get keys set, then login failed
            '''
            print(response)
            #print(key_error)


    def refreshToken(self, login_url ):
        
        if self.Auth_Token is not None:
            request_payload = {'auth_type':'token'}
            header_payload  = {'Authorization':self.Auth_Token}            
            refresh_request = requests.post( login_url + self.Service_Url, params=request_payload, headers=header_payload)
            
            return refresh_request.json()

       
    def manageList(self, folderName, listName, recordData, mergeRule):
        
        if self.Auth_Token is not None:
            manageListParams = {}
            manageListParams['list'] = {'folderName' : folderName }
            manageListParams['recordData'] = recordData
            manageListParams['mergeRule'] = mergeRule    
            header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}

            manageList_request = requests.post(self.End_Point + self.List_Service_Url + listName, data=json.dumps(manageListParams), headers=header_payload)
            
            return manageList_request.json()
        
        else:         
            sys.exit("Not logged in, please login and try again") 
            
    def triggerEmail(self, campaignName, recordData, triggerData, mergeRule):  
        
        if self.Auth_Token is not None:
            triggerParams = {}
            triggerParams['triggerData'] = triggerData
            triggerParams['recordData'] = recordData
            triggerParams['mergeRule'] = mergeRule    
            header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}

            triggerSMS_request = requests.post(self.End_Point + self.Trigger_Service_Url + campaignName + self.Trigger_EMAIL_Service_Url, data=json.dumps(triggerParams), headers=header_payload)
            
            return triggerSMS_request.json()
        else:         
            sys.exit("Not logged in, please login and try again")  
            
    def triggerSMS(self, campaignName, recordData, triggerData, mergeRule):
        
        if self.Auth_Token is not None:
            triggerParams = {}
            triggerParams['triggerData'] = triggerData
            triggerParams['recordData'] = recordData
            triggerParams['mergeRule'] = mergeRule    
            header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}

            triggerSMS_request = requests.post(self.End_Point + self.Trigger_Service_Url + campaignName + self.Trigger_SMS_Service_Url, data=json.dumps(triggerParams), headers=header_payload)
            
            return triggerSMS_request.json()
        
        else:         
            sys.exit("Not logged in, please login and try again")  
            

    '''
    Helper Methods
    '''

    '''
    TriggerData nodes should match 1:1 with the record nodes in recordData.
    The triggerData nodes can contain many optionalData name / value pairs however.
    '''
    def build_TriggerData(self, dataArray):
        
        triggerDataArray = []
        
        for data in dataArray:
            
            for value_pairs in data:
                optionalDataArray = []
            
                
                for key_name in value_pairs.iterkeys():
                    optionalData = {'name': key_name, 'value' : value_pairs[key_name] }
                    optionalDataArray.append( optionalData )
                    
                triggerDataArray.append({'optionalData' : optionalDataArray })
            
        return triggerDataArray

    '''
    Due to poor design the field names are global - not set at the record level
    Every field value needs to have these fields defined or be rejected
    Does not play nice with batching if records have different fields to be updated
    '''
    def build_RecordData(self, fieldNames, fieldValuesArray):
        
        recordData = {}
        recordData['fieldNames'] = fieldNames
        recordData['records'] = []
    
        for fieldValues in fieldValuesArray:
            recordData['records'].append({'fieldValues' : fieldValues})
            
        #print recordData
        return recordData
                
    '''
    ListMergeRules - use with caution, but this is a good base model
    See documents for more detail
    '''
    def build_ListMergeRule(self, insertOnNoMatch, updateOnMatch, matchColumn1, matchColumn2, matchOperator, defaultPermission):
        
        listMergeRule = {}
        listMergeRule['insertOnNoMatch'] = insertOnNoMatch
        listMergeRule['updateOnMatch']   = updateOnMatch
        listMergeRule['matchColumnName1']    = matchColumn1
        listMergeRule['matchColumnName2']    = matchColumn2
        listMergeRule['matchColumnName3']    = None
        listMergeRule['matchOperator']   = matchOperator
        listMergeRule['defaultPermissionStatus'] = defaultPermission
        listMergeRule['htmlValue'] = 'H'
        listMergeRule['textValue'] = 'T'
        listMergeRule['optinValue'] = 'I'
        listMergeRule['optoutValue'] = 'O'
        listMergeRule['rejectRecordIfChannelEmpty'] = 'E'  
        
        #print(listMergeRule)      
        return listMergeRule
        
