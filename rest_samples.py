'''
Created on Nov 12, 2014
@author: mdixon
'''

from rest import rest_api
import requests

def login_and_refresh_token( login_url, login, password):     

    try:
        instance = rest_api( debug=True )
        instance.login(login_url, login, password)
        instance.refreshToken( login_url )
        print (instance.Auth_Token)
        print (instance.End_Point)
        
    except requests.exceptions.RequestException as e:
        print (e)


'''
Begin contact list management
'''

def mergeRecord():
    try:
        instance = rest_api( debug=True )
        fieldNames = ['EMAIL_ADDRESS_', 'CITY_']
        fieldValuesArray = []
        record_vals_1 = ['mdixon@email.com', 'san bruno']
        record_vals_2 = ['some@email.com', 'san francisco']
        
        fieldValuesArray.append(record_vals_1)
        fieldValuesArray.append(record_vals_2)
        
        recordData = instance.build_RecordData(fieldNames, fieldValuesArray)
        
        mergeRule  = instance.build_ListMergeRule( True, 'REPLACE_ALL', 'EMAIL_ADDRESS_', None, 'NONE', 'OPTOUT')
        
        instance.login('https://loginX.responsys.net', '******', '*******')
        
        response_json = instance.manageContactList('Mason','masonList1', recordData, mergeRule)
        
        print( response_json.content )
        
    except requests.exceptions.RequestException as e:
        print (e)
        
        
def retrieveRecord():
    try:
        
        instance = rest_api( debug=True )
        list_name = 'masonList'
        identifier = 'e' # e is for email
        fields = 'RIID_,FIRST_NAME,CITY_'
        recipient_id = 'mdixon@email.com'

        instance.login('https://loginX.responsys.net', '******', '*******')
        
        response_json = instance.retrieveContactListMember(list_name, identifier, fields, recipient_id)
        
        print( response_json )
        
    except requests.exceptions.RequestException as e:
        print (e)
        
def retrieveRecordByRIID():
    try:
        #24720425
        instance = rest_api( debug=True )
        list_name = 'masonList'
        fields = 'EMAIL_ADDRESS_,FIRST_NAME,CITY_'
        recipient_id = '409580667'

        instance.login('https://loginX.responsys.net', '******', '*******')
        
        response_json = instance.retrieveContactListMemberByRIID(list_name, fields, recipient_id)
        
        print( response_json )
        
    except requests.exceptions.RequestException as e:
        print (e)
        
        
        
'''
End contact list management
'''
        
'''
Begin profile extension table management
'''
        
def retrieveAllPetsByList():
    try:
        #24720425
        instance = rest_api( debug=True )
        list_name = 'masonList'
        instance.login('https://loginX.responsys.net', '******', '*******')
        
        response_json = instance.retrievePetsByList(list_name)
        
        print( response_json )
        
    except requests.exceptions.RequestException as e:
        print (e)
           
        
def createProfileExtensionTable():
    try:
        
        instance = rest_api( debug=True )
        
        list_name = 'masonList'
        table_name = 'instance_PET_table'
        folder_name = 'mason'
        
        fields = []
        field_1 = {'fieldName' : 'Field_1', 'fieldType' : 'STR500'}
        field_2 = {'fieldName' : 'Field_2', 'fieldType' : 'STR500'}
        
        fields.append(field_1)
        fields.append(field_2)
        
        instance.login('https://loginX.responsys.net', '******', '*******')
        create_response = instance.createProfileExtensionTable(list_name, table_name, folder_name, fields)
        print( create_response.content )
        
    except requests.exceptions.RequestException as e:
        print (e)
        

def updateProfileExtensionTableRecord():
    try:
        instance = rest_api( debug=True )
        list_name = 'masonList'
        table_name = 'instance_PET_table'
        
        fieldNames = ['RIID_','FIELD_1','FIELD_2']
        fieldValuesArray = []
        fields_1 = ['409580667','some_val1','some_val2']
        fields_2 = ['123455','some_val3','some_val4']
        fieldValuesArray.append(fields_1)
        fieldValuesArray.append(fields_2)
        
        recordData = instance.build_RecordData2(fieldNames, fieldValuesArray)
        
        insertOnNoMatch = True
        updateOnMatch = "REPLACE_ALL"
        matchColumn = "RIID"
        
        instance.login('https://loginX.responsys.net', '******', '*******')
        update_response = instance.updateProfileExtensionTableRecord(list_name, table_name, recordData, insertOnNoMatch, updateOnMatch, matchColumn)
        print( update_response.content )
        
        
    except requests.exceptions.RequestException as e:
        print (e)
        
def retrieveProfileExtensionTableRecordByRIID():
    try:
        instance = rest_api( debug=True )
        list_name = 'masonList'
        table_name = 'instance_PET_table'
        fields = 'FIELD_1,FIELD_2'
        recipientId = '415580852'
        
        instance.login('https://loginX.responsys.net', '******', '*******')
        retrieve_response = instance.retrieveFromProfileExtensionTableByRIID(list_name, table_name, fields, recipientId)
        print( retrieve_response.content ) 
    except requests.exceptions.RequestException as e:
        print (e)

        
def deleteProfileExtensionTableRecord():
    try:
        instance = rest_api( debug=True )
        list_name = 'masonList'
        table_name = 'instance_PET_table'
        identifier = 'r' # r is for recipientId aka RIID
        recipientId = 415580852
        
        instance.login('https://loginX.responsys.net', '******', '*******')
        delete_response = instance.deleteProfileExtensionTableRecord(list_name, table_name, identifier, recipientId)
        print( delete_response.content )
        
    except requests.exceptions.RequestException as e:
        print (e)
'''
End profile extension table management
'''        
        
'''
Begin supplemental table management
'''
def createSupplementalTable():
    try:
        instance = rest_api( debug=True )
        
    except requests.exceptions.RequestException as e:
        print (e)

        
def updateSupplementalTableRecord():
    try:
        instance = rest_api( debug=True )
    
    except requests.exceptions.RequestException as e:
        print (e)


def retrieveSupplementalTableRecord():
    try:
        instance = rest_api( debug=True )
    
    except requests.exceptions.RequestException as e:
        print (e)
        
def deleteSupplementalTableRecord():
    try:
        instance = rest_api( debug=True )
    
    except requests.exceptions.RequestException as e:
        print (e)

'''
END Supplemental table management
'''

'''
Begin PROGRAM aka Custom Event
'''
def triggerCustomEvent():
    try:
        instance = rest_api( debug=True )
        
    except requests.exceptions.RequestException as e:
        print (e)


        
'''
Begin campaign management     
   
def triggerSMS():
    try:
        
        instance = rest_api( debug=True )
        
        fieldNames = ['EMAIL_ADDRESS_', 'MOBILE_NUMBER_', 'MOBILE_COUNTRY_', 'MOBILE_PERMISSION_STATUS_']
        fieldValuesArray = []
        triggerDataArray = []
        record_vals_1 = ['email@smoracle.com', '16504835108', 'US', 'OPTOUT']
        
        triggerData = []
        opt1 = {'data_1':'api value 1'}
        opt2 = {'data_2': 'api value 2'}
        triggerData.append(opt1)
        triggerData.append(opt2)
        
        triggerDataArray.append(triggerData)
        fieldValuesArray.append(record_vals_1)
        #fieldValuesArray.append(record_vals_2)
        
        recordData  = instance.build_RecordData(fieldNames, fieldValuesArray)
        
        triggerData = instance.build_TriggerData(triggerDataArray)
        
        mergeRule  = instance.build_ListMergeRule( True, 'REPLACE_ALL', 'EMAIL_ADDRESS_', None, 'NONE', 'OPTIN')
    
        instance.login('https://loginX.responsys.net', '*******', '*******')
        response = instance.triggerSMS('MASON', recordData, triggerData, mergeRule)
        
        return response 
    
    except requests.exceptions.RequestException as e:
        print (e)
''' 
                
def triggerEmail():
    try:
        
        instance = rest_api( debug=True )
        
        fieldNames = ['EMAIL_ADDRESS_', 'CITY_']
        fieldValuesArray = []
        triggerDataArray = []
        
        record_vals_1 = ['mark.l.jarvis@oracle.com', 'san bruno']

        triggerData_record1 = []
        
        optional_data_1 = {'FIRST_NAME':'Masonovich'}
        optional_data_2 = {'LAST_NAME':'Dixonovich'}
        
        triggerData_record1.append(optional_data_1)
        triggerData_record1.append(optional_data_2)
        
        triggerDataArray.append(triggerData_record1)
        
        fieldValuesArray.append(record_vals_1)
        
        recordData  = instance.build_RecordData(fieldNames, fieldValuesArray)
        
        triggerData = instance.build_TriggerData(triggerDataArray)
        
        triggerData = None
        
        mergeRule  = instance.build_ListMergeRule( True, 'REPLACE_ALL', 'EMAIL_ADDRESS_', None, 'NONE', 'OPTIN')
    
        instance.login('https://loginX.responsys.net', '*********', '*******')
        response = instance.triggerEmail('masonCampaign1', recordData, triggerData, mergeRule)
        print(response)
    
    except requests.exceptions.RequestException as e:
        print (e)
        
   