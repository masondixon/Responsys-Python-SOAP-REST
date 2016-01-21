'''
Created on Nov 5, 2014
'''

import requests
import json
import logging


class rest_api(object):
    
    Auth_Token = None
    End_Point  = None
    Login_Url  = None
    Logged_In  = False
    
    Service_Url = '/rest/api/v1/auth/token'
    
    List_Service_Url = '/rest/api/v1/lists/'
    PET_Service_Url  = '/listExtensions'
    
    HAtrigger_Service_Url     = '/rest/haApi/v1.1/campaigns/'
    Trigger_Service_Url       = '/rest/api/v1/campaigns/'
    Trigger_SMS_Service_Url   = '/sms'
    Trigger_EMAIL_Service_Url = '/email'
    
    SUPP_SERVICE_URL      = '/rest/api/v1/folders/'
    SUPP_SERVICE_SUPPDATA = 'suppData'
    SUPP_SERVICE_MEMBERS  = 'members'
    
    

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
   
    '''
    Authenticate, to obtain an auth token and service end point
    Set token and end point
    '''     
    def login(self, login_url, login, password):
        
        payload = {'user_name': login, 'auth_type': 'password', 'password': password}
        login_request = requests.post( login_url + self.Service_Url, data=payload )
        response = login_request.json()
        
        try:
            self.Auth_Token = response['authToken']
            self.End_Point  = response['endPoint']
            
            if self.Auth_Token is not None and self.End_Point is not None:
                #print(response)
                self.Logged_In = True
            else:
                raise Exception("Auth failed -  missing auth token and or endpoint!")
                
        except KeyError as key_error:
            '''
            If we cant get keys set, then login failed
            '''
            raise Exception("Auth failed -  missing auth token and or endpoint!")
            print(response)
            print(key_error)

    '''
    Instead of logging in again, one can opt to refresh an auth token....
    '''
    def refreshToken(self, login_url ):

        request_payload = {'auth_type':'token'}
        header_payload  = {'Authorization':self.Auth_Token}            
        refresh_request = requests.post( login_url + self.Service_Url, data=request_payload, headers=header_payload)
        
        return refresh_request.json()

    
    '''
    Merge or update members in a profile list table....
    ''' 
    def manageContactList(self, folderName, listName, recordData, mergeRule):

        manageListParams = {}
        manageListParams['list'] = {'folderName' : folderName }
        manageListParams['recordData'] = recordData
        manageListParams['mergeRule'] = mergeRule    
        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}

        manageList_request = requests.post(self.End_Point + self.List_Service_Url + listName, data=json.dumps(manageListParams), headers=header_payload)
        
        return manageList_request.json()

    
    '''
    Retrieve a member of a profile list table....
    /rest/api/v1/lists/<listName>?qa=<qa>&fs=<fs>&id=<id>
    Request parameters:
       qa - single character (r:RIID, e:email, c:customer ID or m:mobile)
       fs - comma separated list of fields to retrieve
       id - id to retrieve based on qa value specified (e.g., r for RIID)
    '''
    def retrieveContactListMember(self, list_name, identifier, fields, recipient_id):
        
        params = { 'qa' : identifier, 'fs' : fields, 'id' : recipient_id }

        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}

        retrieve_request = requests.get(self.End_Point + self.List_Service_Url + list_name, params=params, headers=header_payload)
            
        return retrieve_request.json()
    
    
    '''
    Retrieve a member of a profile list using RIID...
    /rest/api/v1/lists/<listName>/members/<riid>
    '''
    def retrieveContactListMemberByRIID(self, list_name, fields, recipient_id):
        
        params = { 'fs' : fields }

        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}

        retrieve_request = requests.get(self.End_Point + self.List_Service_Url + list_name + '/members/' + recipient_id, params=params, headers=header_payload)
            
        return retrieve_request.json()
    
    
    '''
    Get all PET tables for a given list...
    /rest/api/v1/lists/<listName>/listExtensions
    '''
    
    def retrievePetsByList(self, list_name ):
        
        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}

        retrieve_request = requests.get(self.End_Point + self.List_Service_Url + list_name + '/listExtensions', params=None, headers=header_payload)
            
        return retrieve_request.json()

    '''
    Create a profile extension table against an existing contact list....
    /rest/api/v1/lists/<listName>/listExtensions
    '''
    def createProfileExtensionTable(self, list_name, table_name, folder_name, fields):
 
        params = {}        
        params['profileExtension'] = { 'objectName' : table_name, 'folderName' : folder_name }
        params['fields'] = fields

        print (json.dumps( params ) )
        
        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}
    
        create_pet_response = requests.post( self.End_Point + self.List_Service_Url + list_name + self.PET_Service_Url, data=json.dumps( params ), headers=header_payload )
    
        return create_pet_response
    
    '''
    Merge or update members in a profile extension table...
    '''
    def retrieveFromProfileExtensionTableByRIID(self, list_name, table_name, fields, recipient_id):  
        
        params = {}
        params['fs'] = fields    
        
        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}
    
        create_pet_response = requests.get( self.End_Point + self.List_Service_Url + list_name + self.PET_Service_Url + '/' + table_name + '/members/' + recipient_id, params=params, headers=header_payload )
    
        return create_pet_response
    
    
    
    '''
    Insert or update a PET table record...
    /rest/api/v1/lists/<listName>/listExtensions/<petName>
    '''
    def updateProfileExtensionTableRecord(self, list_name, table_name, recordData, insertOnNoMatch, updateOnMatch, matchColumn):
        
        params = {}
        params['recordData'] = recordData
        params['insertOnNoMatch'] = insertOnNoMatch
        params['updateOnMatch'] = updateOnMatch
        params['matchColumn'] = matchColumn
        
        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}
        
        print( json.dumps( params ))

        create_pet_response = requests.post( self.End_Point + self.List_Service_Url + list_name + self.PET_Service_Url + '/' + table_name + '/members', data=json.dumps(params), headers=header_payload )
    
        return create_pet_response
        
        
    '''
    Delete a record from an extension table....
    /rest/api/v1/lists/<listName>/listExtensions/<petName>?qa=<qa>&id=<id>
    '''
    def deleteProfileExtensionTableRecord(self, list_name, table_name, identifier, recipient_id):
 
        params = { 'qa' : identifier, 'id' : recipient_id }        
        
        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}
    
        create_pet_response = requests.delete( self.End_Point + self.List_Service_Url + list_name + self.PET_Service_Url + '/' + table_name, params=params, headers=header_payload )
    
        return create_pet_response
    
    
    '''
    Create a supplemental table....
    /rest/api/v1/folders/<folderName>/suppData
    '''
    
    '''
    Update or insert into a supplemental table....
    /rest/api/v1/folders/<folderName>/suppData/<tableName>/members
    '''
    
    '''
    Retrieve records from a supplemental table....
    /rest/api/v1 /folders/<folderName>/suppData/<tableName>/members
    /rest/api/v1/folders/DemoNewsLetter/suppData/CompositePKSuppTable/members?qa=PK1&qa=PK2&qa=PK3&fs=PK1,PK2,PK3,F1,F2&id=1&id=1&id=1
    '''
    
    '''
    Delete records from supplemental table....
    /rest/api/v1/lists /folders/<folderName>/suppData/<tableName>/members
    rest/api/v1/folders/DemoNewsLetter/suppData/CompositePKSuppTable/members?qa=PK1&qa=PK2&qa=PK3&fs=PK1,PK2,PK3,F1,F2&id=1&id=1&id=1
    '''
    
    '''
    Trigger a custom event aka PROGRAM
    /rest/api/v1/events/<eventName>
    '''
    
    '''
    Merge members into a profile list and subsequently send them an email message.
    '''        
    def triggerEmail(self, campaignName, recordData, triggerData, mergeRule):  

        triggerParams = {}
        triggerParams['recordData']  = recordData
        triggerParams['mergeRule']   = mergeRule
        triggerParams['triggerData'] = triggerData
        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}
        
        triggerEmail_request = requests.post( self.End_Point + self.Trigger_Service_Url + campaignName + '/email', data=json.dumps( triggerParams ), headers=header_payload )
        
        return triggerEmail_request.json()
 
    '''
    Merging members into a profile list and subsequently send them an SMS message
    '''      
    def triggerSMS(self, campaignName, recordData, triggerData, mergeRule):

        triggerParams = {}
        triggerParams['triggerData'] = triggerData
        triggerParams['recordData']  = recordData
        triggerParams['mergeRule']   = mergeRule    
        header_payload  = {'Authorization':self.Auth_Token,'Content-type': 'application/json'}

        triggerSMS_request = requests.post(self.End_Point + self.Trigger_Service_Url + campaignName + self.Trigger_SMS_Service_Url, data=json.dumps(triggerParams), headers=header_payload)
        
        return triggerSMS_request.json()

    '''
    Helper Methods
    '''

    '''
    TriggerData nodes should match 1:1 with the record nodes in recordData.
    The triggerData nodes can contain many optionalData name / value pairs however.
    '''
    def build_TriggerData(self, dataArray):
 
        optionalDataCollection = []
        for data in dataArray: 
            
            if data is not None:            
                optionalData = {}
                optionalData['optionalData'] = []
                
                for value_pairs in data:
                    for key_name in value_pairs.iterkeys():
                        optionalData['optionalData'].append( {'name': key_name, 'value' : value_pairs[key_name] } )
                optionalDataCollection.append( optionalData )       
            else:
                optionalDataCollection.append( None ) 

        return optionalDataCollection


    def build_RecordData(self, fieldNames, fieldValuesArray):
        
        recordData = {}
        recordData['fieldNames'] = fieldNames
        recordData['records'] = []
        recordData['mapTemplateName'] = None
    
        for fieldValues in fieldValuesArray:
            recordData['records'].append({'fieldValues' : fieldValues})
            
        #print(recordData)
        return recordData
    
    '''
    Due to bad design have to create another wrapper to deal with non-standard json formats
    '''
    def build_RecordData2(self, fieldNames, fieldValuesArray ):
        recordData = {}
        recordData['fieldNames'] = fieldNames
        recordData['records'] = []
        recordData['mapTemplateName'] = None
    
        for fieldValues in fieldValuesArray:
            recordData['records'].append( fieldValues )
            
        #print(recordData)
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
        
