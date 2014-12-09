'''
Created on Aug 27, 2012
@author: mdixon

DEPENCIES:
--SUDS-- SOAP FOR PYTHON

'''
import logging

from suds.client import Client
from suds import WebFault

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

class interact_api:
    
    #global interactObject
    
    def __init__( self, login_, password, pod, isDev ):

        self.login    = login_
        self.password = password
        self.pod      = pod
        self.isDev    = isDev
        self.loggedIn = False
        ursa          = "1"
       
        # Pods 2 and 5 are orion so wsdl and endpoint are different
        pod_to_ws = [ "2", "5" ]
        
        for ws_type in pod_to_ws:
            self.printIt(ws_type)
            if pod == ws_type:
                ursa = "0"
                continue
        
        print ( "ursa " + ursa )
        # This logic allows us to derive web services assets by pod
        if ursa == "1":
            self.api_url  = 'https://ws' + pod + '.responsys.net/webservices57/services/ResponsysWS57?wsdl'
            self.endpoint = 'https://ws' + pod + '.responsys.net/webservices57/services/ResponsysWS57'
        else:
            self.api_url  = 'https://ws' + pod + '.responsys.net/webservices/wsdl/ResponsysWS_Level1.wsdl'
            self.endpoint = 'https://ws' + pod + '.responsys.net/webservices/services/ResponsysWSService'
        
        
    def soap_client_init( self ):
        try:
            self.printIt( 'INVOKING WEB SERVICES ON : ' + self.api_url )
            
            # set proxy setting to something fiddler can use
            # if fiddler isnt running soap client fault ensues
            if self.isDev == 1:
                proxy_settings = dict(http='127.0.0.1:8888', https='127.0.0.1:8888')
            else:
                proxy_settings = dict()
                
            client = Client( self.api_url, location = self.endpoint, proxy = proxy_settings )
            self.client = client
        except WebFault as detail:
            self.printIt( detail )


    def doLogin( self ):
        try:
            loginResponse   = self.client.service.login( self.login, self.password )
            token           = self.client.factory.create( 'SessionHeader' )
            token.sessionId = loginResponse.sessionId
            self.client.set_options( soapheaders = token )
            self.loggedIn   = True
            self.printIt( 'Logged in...' )
        except WebFault as detail:
            self.printIt( detail )
                     
            
    def setInteractObject( self, folderName, objectName ):
        interactObj = self.client.factory.create( 'InteractObject' )
        interactObj.folderName = folderName
        interactObj.objectName = objectName
        return interactObj
          
        
    def printIt( self, whatever ):
        print ( whatever )

    
    
    def logOut( self ):
        logout = self.client.service.logout()
        self.printIt( logout )
    
    
        
    def listFolders( self ):
        listfolders = self.client.service.listFolders()
        
        for folder in listfolders:
            self.printIt( folder )
            

    '''
    MergeListMembers
    Add or update records in a table
    '''
    def mergeListMembers( self, folderName, listName, fieldNames, fieldValues ):
        try:
            #Create Campaign Object:
            interactObj = self.setInteractObject( folderName, listName )
            
            #Create RecordObj
            recordObj = self.client.factory.create('Record')
            
            #Create RecorDataObj
            recordDataObj = self.client.factory.create('RecordData')
            
            for value in fieldValues:
                recordObj.fieldValues.append( value )
                
            for name in fieldNames:
                recordDataObj.fieldNames.append( name )

            recordDataObj.records  = recordObj
            
            #Create listMerge Object:
            listMergeObj = self.client.factory.create('mergeRule')
            listMergeObj.insertOnNoMatch  = True
            listMergeObj.updateOnMatch    = 'REPLACE_ALL'
            listMergeObj.matchColumnName1 = 'EMAIL_ADDRESS_'
            listMergeObj.matchOperator    = 'NONE'
            listMergeObj.optinValue       = 'I'
            listMergeObj.optoutValue      = 'O'
            listMergeObj.htmlValue        = 'H'
            listMergeObj.textValue        = 'T'
            listMergeObj.rejectRecordIfChannelEmpty = 'E'
            listMergeObj.defaultPermissionStatus = 'OPTIN'
        
            print self.client.service.mergeListMembers( interactObj, recordDataObj, listMergeObj );
       
        except WebFault as detail:
            self.printIt( detail )
            
            
    '''
    RetrieveListMembers
    Retrieve records from a table by a specified column and id or email or see doc ( QueryColumn )
    '''
    def retrieveListMembers( self, folderName, objectName, fields, emails ):
        try:
            InteractObject = self.setInteractObject(folderName, objectName)
            QueryColumn    = self.client.factory.create('QueryColumn')
            
            fieldNames        = []
            recordsToRetrieve = []
            
            for name in fields:
                fieldNames.append( name )
                
            for email in emails:
                recordsToRetrieve.append( email )

            print self.client.service.retrieveListMembers( InteractObject, QueryColumn.EMAIL_ADDRESS, fieldNames, recordsToRetrieve );
            
        except WebFault as detail:
            self.printIt( detail )
            
            
    '''
    TriggerCustomEvent
    Push a contact into a program using the event name or id
    Contact needs to be in a list or table prior to being inserted into program
    This sample assumes that all recipients are in the same folder/list will use same InteractObject
    '''
    def triggerCustomEvent( self, folderName, objectName, recipientEmails, customEvent ):
        try:
            InteractObject = self.setInteractObject(folderName, objectName)
            CustomEvent = self.client.factory.create('CustomEvent')
            CustomEvent.eventName = customEvent
            
            OptionalDataList = []
            
            for email in recipientEmails:
                Recipient = self.client.factory.create('Recipient')    
                Recipient.emailAddress = email
                Recipient.listName     = InteractObject
                Recipient.emailFormat  = 'NO_FORMAT'
                
                OptionalData = self.client.factory.create('OptionalData')
                OptionalData.name  = ""
                OptionalData.value = ""
                
                RecipientData = self.client.factory.create('RecipientData')
                RecipientData.recipient    = Recipient
                RecipientData.optionalData = OptionalData
            
                OptionalDataList.append(RecipientData)
            
            
            print self.client.service.triggerCustomEvent( CustomEvent, OptionalDataList )
        
        except WebFault as detail:
            self.printIt( detail )
            
    '''
    TriggerCampaignMessage
    Send an email or campaign to a recipient or group of recipients
    This sample assumes that all recipients are in the same folder/list will use same InteractRecipientObject
    '''
    def triggerCampaignMessage( self, campaignFolderName, campaignObjectName, recipientEmails, recipientFolderName, recipientObjectName ):
        try:
            InteractObject = self.client.factory.create("InteractObject")
            InteractObject.folderName = campaignFolderName
            InteractObject.objectName = campaignObjectName
            
            InteractRecipientObject = self.client.factory.create("InteractObject")
            InteractRecipientObject.folderName = recipientFolderName
            InteractRecipientObject.objectName = recipientObjectName
            
            OptionalDataList = []
            
            for email in recipientEmails:
                Recipient = self.client.factory.create('Recipient')    
                Recipient.emailAddress = email
                Recipient.listName     = InteractRecipientObject
                Recipient.emailFormat  = 'NO_FORMAT'
                
                OptionalData = self.client.factory.create('OptionalData')
                OptionalData.name  = ""
                OptionalData.value = ""
                
                RecipientData = self.client.factory.create('RecipientData')
                RecipientData.recipient    = Recipient
                RecipientData.optionalData = OptionalData
            
                OptionalDataList.append(RecipientData)
            
            print self.client.service.triggerCampaignMessage( InteractObject, OptionalDataList )
        
        except WebFault as detail:
            self.printIt( detail )

# Example usage    
class runTests:
    
    someLogin = 'something'
    somePass  = 'something'
    pod       = '5' # Expects your pod number here 5 is for interact 5 for exmaple
    isDev     = 1   # 1 pipes the calls through local proxy which would be picked up by Fiddler if installed 
    
    folder    = 'someFolder'
    list      = 'someList'
    
    fields    = ['EMAIL_ADDRESS_' , 'CUSTOMER_ID_']
    values    = ['test@email.com', '123abc']
    
    email     = ['test@email.com']
    eventName = 'Some Event Name'
    
def __init__(self):
        
        print( '*** Running Python Tests ***')
        
        test = interact_api( self.someLogin, self.somePass, self.pod, self.isDev)
        test.soap_client_init()
        test.doLogin()
        
        if test.loggedIn:
        
            #LIST FOLDERS
            test.listFolders()
            
            #MERGE LIST MEMBERS
            #test.mergeListMembers( self.folder, self.list, self.fields, self.values )
            
            #TRIGGER CUSTOM EVENT
            #test.triggerCustomEvent( self.folder, self.list, self.email, self.eventName )
            
            if(test.loggedIn):
                test.logOut()
        else:
            test.printIt( "Login failed, didn't run any tests ")
            
            
runTests = runTests()

