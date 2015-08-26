'''
Created on Nov 12, 2014
@author: mdixon
'''

from rest import rest_api
import requests

def login_and_refresh_token( login_url, login, password):     

    try:
        test = rest_api( debug=True )
        test.login(login_url, login, password)
        test.refreshToken( login_url )
        print (test.Auth_Token)
        print (test.End_Point)
        
    except requests.exceptions.RequestException as e:
        print (e)


'''
Begin contact list management
'''

def mergeRecord():
    try:
        test = rest_api( debug=True )
        fieldNames = ['EMAIL_ADDRESS_', 'CITY_']
        fieldValuesArray = []
        record_vals_1 = ['mdixon@email.com', 'san bruno']
        record_vals_2 = ['some@email.com', 'san francisco']
        
        fieldValuesArray.append(record_vals_1)
        fieldValuesArray.append(record_vals_2)
        
        recordData = test.build_RecordData(fieldNames, fieldValuesArray)
        
        mergeRule  = test.build_ListMergeRule( True, 'REPLACE_ALL', 'EMAIL_ADDRESS_', None, 'NONE', 'OPTOUT')
        
        test.login('https://loginX.responsys.net', '******', '*******')
        
        response_json = test.manageContactList('Mason','masonList1', recordData, mergeRule)
        
        print( response_json.content )
        
    except requests.exceptions.RequestException as e:
        print (e)
        
        
def retrieveRecord():
    try:
        
        test = rest_api( debug=True )
        list_name = 'masonList'
        identifier = 'e' # e is for email
        fields = 'RIID_,FIRST_NAME,CITY_'
        recipient_id = 'mdixon7@gmail.com'

        test.login('https://loginX.responsys.net', '******', '*******')
        
        response_json = test.retrieveContactListMember(list_name, identifier, fields, recipient_id)
        
        print( response_json )
        
    except requests.exceptions.RequestException as e:
        print (e)
        
def retrieveRecordByRIID():
    try:
        #24720425
        test = rest_api( debug=True )
        list_name = 'masonList'
        fields = 'EMAIL_ADDRESS_,FIRST_NAME,CITY_'
        recipient_id = '409580667'

        test.login('https://loginX.responsys.net', '******', '*******')
        
        response_json = test.retrieveContactListMemberByRIID(list_name, fields, recipient_id)
        
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
        test = rest_api( debug=True )
        list_name = 'masonList'
        test.login('https://loginX.responsys.net', '******', '*******')
        
        response_json = test.retrievePetsByList(list_name)
        
        print( response_json )
        
    except requests.exceptions.RequestException as e:
        print (e)
           
        
def createProfileExtensionTable():
    try:
        
        test = rest_api( debug=True )
        
        list_name = 'masonList'
        table_name = 'test_PET_table'
        folder_name = 'mason'
        
        fields = []
        field_1 = {'fieldName' : 'Field_1', 'fieldType' : 'STR500'}
        field_2 = {'fieldName' : 'Field_2', 'fieldType' : 'STR500'}
        
        fields.append(field_1)
        fields.append(field_2)
        
        test.login('https://loginX.responsys.net', '******', '*******')
        create_response = test.createProfileExtensionTable(list_name, table_name, folder_name, fields)
        print( create_response.content )
        
    except requests.exceptions.RequestException as e:
        print (e)
        

def updateProfileExtensionTableRecord():
    try:
        test = rest_api( debug=True )
        list_name = 'masonList'
        table_name = 'test_PET_table'
        
        fieldNames = ['RIID_','FIELD_1','FIELD_2']
        fieldValuesArray = []
        fields_1 = ['409580667','some_val1','some_val2']
        fields_2 = ['123455','some_val3','some_val4']
        fieldValuesArray.append(fields_1)
        fieldValuesArray.append(fields_2)
        
        recordData = test.build_RecordData2(fieldNames, fieldValuesArray)
        
        insertOnNoMatch = True
        updateOnMatch = "REPLACE_ALL"
        matchColumn = "RIID"
        
        test.login('https://loginX.responsys.net', '******', '*******')
        update_response = test.updateProfileExtensionTableRecord(list_name, table_name, recordData, insertOnNoMatch, updateOnMatch, matchColumn)
        print( update_response.content )
        
        
    except requests.exceptions.RequestException as e:
        print (e)
        
def retrieveProfileExtensionTableRecordByRIID():
    try:
        test = rest_api( debug=True )
        list_name = 'masonList'
        table_name = 'test_PET_table'
        fields = 'FIELD_1,FIELD_2'
        recipientId = '415580852'
        
        test.login('https://loginX.responsys.net', '******', '*******')
        retrieve_response = test.retrieveFromProfileExtensionTableByRIID(list_name, table_name, fields, recipientId)
        print( retrieve_response.content ) 
    except requests.exceptions.RequestException as e:
        print (e)

        
def deleteProfileExtensionTableRecord():
    try:
        test = rest_api( debug=True )
        list_name = 'masonList'
        table_name = 'test_PET_table'
        identifier = 'r' # r is for recipientId aka RIID
        recipientId = 415580852
        
        test.login('https://loginX.responsys.net', '******', '*******')
        delete_response = test.deleteProfileExtensionTableRecord(list_name, table_name, identifier, recipientId)
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
        test = rest_api( debug=True )
        
    except requests.exceptions.RequestException as e:
        print (e)

        
def updateSupplementalTableRecord():
    try:
        test = rest_api( debug=True )
    
    except requests.exceptions.RequestException as e:
        print (e)


def retrieveSupplementalTableRecord():
    try:
        test = rest_api( debug=True )
    
    except requests.exceptions.RequestException as e:
        print (e)
        
def deleteSupplementalTableRecord():
    try:
        test = rest_api( debug=True )
    
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
        test = rest_api( debug=True )
        
    except requests.exceptions.RequestException as e:
        print (e)


        
'''
Begin campaign management     
'''    
def triggerSMS():
    try:
        
        test = rest_api( debug=True )
        
        fieldNames = ['EMAIL_ADDRESS_', 'MOBILE_NUMBER_', 'MOBILE_COUNTRY_', 'MOBILE_PERMISSION_STATUS_']
        fieldValuesArray = []
        triggerDataArray = []
        record_vals_1 = ['email@smoracle.com', '16504835108', 'US', 'OPTOUT']
        #record_vals_2 = ['mei.chan@oracle.com', '14083415539', 'US']
        
        triggerData = []
        opt1 = {'data_1':'api value 1'}
        opt2 = {'data_2': 'api value 2'}
        triggerData.append(opt1)
        triggerData.append(opt2)
        
        triggerDataArray.append(triggerData)
        fieldValuesArray.append(record_vals_1)
        #fieldValuesArray.append(record_vals_2)
        
        recordData  = test.build_RecordData(fieldNames, fieldValuesArray)
        
        triggerData = test.build_TriggerData(triggerDataArray)
        
        mergeRule  = test.build_ListMergeRule( True, 'REPLACE_ALL', 'EMAIL_ADDRESS_', None, 'NONE', 'OPTIN')
    
        test.login('https://loginX.responsys.net', '*******', '*******')
        response = test.triggerSMS('MASON', recordData, triggerData, mergeRule)
        
        return response 
    
    except requests.exceptions.RequestException as e:
        print (e)
        
def triggerEmail():
    try:
        
        test = rest_api( debug=True )
        
        fieldNames = ['EMAIL_ADDRESS_', 'CITY_']
        fieldValuesArray = []
        triggerDataArray = []
        
        record_vals_1 = ['kity.daly@oracle.com', 'san bruno']
        record_vals_2 = ['mdixon@gmail.com', 'martinez']
        
        triggerData_record1 = []
        triggerData_record2 = []
        
        opt1 = {'FIRST_NAME':'Mason'}
        opt2 = {'ORDER_NUMBER': '1234567'}
        
        opt3 = {'FIRST_NAME':'Mike'}
        opt4 = {'ORDER_NUMBER': '32432424'}
        
        triggerData_record1.append(opt1)
        triggerData_record1.append(opt2)
        
        triggerData_record2.append(opt3)
        triggerData_record2.append(opt4)
        
        triggerDataArray.append(triggerData_record1)
        triggerDataArray.append(triggerData_record2)
        
        fieldValuesArray.append(record_vals_1)
        fieldValuesArray.append(record_vals_2)
        
        recordData  = test.build_RecordData(fieldNames, fieldValuesArray)
        
        triggerData = test.build_TriggerData(triggerDataArray)
        
        mergeRule  = test.build_ListMergeRule( True, 'REPLACE_ALL', 'EMAIL_ADDRESS_', None, 'NONE', 'OPTIN')
    
        test.login('https://loginX.responsys.net', '*******', '*******')
        response = test.triggerEmail('masonCampaign1', recordData, triggerData, mergeRule)
        print(response)
    
    except requests.exceptions.RequestException as e:
        print (e)

#test = login_and_refresh_token('https://login5.responsys.net', 'someLogin', 'somePass')
#test = login_and_merge_and_triggerSMS()
#test = login_and_triggerEmail()
#test = retrieveAllPetsByList()
#test = deleteProfileExtensionTableRecord()
#test = retrieveProfileExtensionTableRecordByRIID()
test = updateProfileExtensionTableRecord()