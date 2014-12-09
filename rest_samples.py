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


def login_and_mergeRecord():
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
        
        test.manageList('Mason','masonList1', recordData, mergeRule)
        
    except requests.exceptions.RequestException as e:
        print (e)
    
def login_and_merge_and_triggerSMS():
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
        
def login_and_triggerEmail():
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