"""
IxSuiteStore.py

A high level wrapper library that executes IxSuiteStore REST APIs.
If an error occurs, an IxSuiteStoreException will be raised
and the script will be aborted.

Requirements:
   - Python 3.7.0 minimum
   - python-gitlab (If integration GitLab pipeline testing)
   
Note:
   - Python 2 is not supported
"""

import os, requests, json, traceback, time, datetime, platform, shutil

class IxSuiteStore:
    """
    A high level wrapper library that executes IxSuiteStore REST APIs.
    If an error occurs, an IxSuiteStoreException will be raised
    and the script will be aborted.
    """
    # For IxSuiteStoreException log handling
    debugLogFile = None
    
    def __init__(self, serverIp, username='admin', password='admin', sessionId=None, printStdout=True,
                 debugLogFile='ixSuiteStoreDebug.log'):
        """
        serverIp (str): The IxSuiteStore server IP address
        username (str): The login username
        password (str): The login password
        sessionId (int): The existing session ID to connect to
        debugLogFile (bool|str): Set to False or None to disable generating a debug log file.
        """
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self._session = requests.Session()
        self.sessionId = sessionId
        self.serverIp = serverIp
        self.username = username
        self.password = password
        self.httpHeader = f'https://{self.serverIp}'
        self.baseUrl = f'{self.httpHeader}/ixsuitestore'
        self.headers = {"content-type": "application/json; charset=us-ascii"}
        self.verifySslCert = False
        self.debugLogFile = debugLogFile

        # For connecting to the session directly. This is set in startSession
        self.suiteStoreSession = ''
        
        # Sometimes there are situations to not print outputs. In this case, set: session.printStdout = False
        self.printStdout = printStdout
        
        if debugLogFile:
            open(self.debugLogFile, 'w').close()

    def request(self, httpVerb, restApi, data={}, headers=None, printLogMsg=True, execWaitForComplete=True):
        """
        This function sends all the rest api.
        
        httpVerb (str): GET, POST, PATCH, DELETE
        restApi (str): The REST API
        data (dict): The data payload
        printLogMsg (bool): True=Print debugging log messages. Some fuctions such as waitForComplete
                            would not want this enabled for better display of the operation status.
        execWaitForComplete (bool): True=Verify the operation status.  In most POST operations, it is
                            required to verify the operation status for SUCCESS before continuing, but
                            some POST operations such as authenticating username/password doesn't 
                            require it. 
        """
        if headers is None:
            headers = self.headers
            
        try:
            if self.printStdout:
                # If it's waitForOperation, don't print this
                if printLogMsg:
                    self.logMsg(msgType='info', msg=f'\n{httpVerb}: {restApi}\nDATA: {data}')
                    #self.logMsg(msgType='info', msg=f'\n{httpVerb}: {restApi}\nDATA: {data}\nHEADERS: {self.headers}')

            response = self._session.request(httpVerb.upper(), restApi, data=json.dumps(data), 
                                             headers=headers, allow_redirects=True, verify=self.verifySslCert)
            
            self.logMsg(msgType='info', msg=f'\nStatus: {response.status_code}')
            
            if not str(response.status_code).startswith('2'):
                raise IxSuiteStoreException(response.json())

        except (requests.exceptions.RequestException, Exception) as errMsg:
            raise IxSuiteStoreException(errMsg)
        
        if httpVerb.lower() == 'post' and execWaitForComplete:
            self.waitForComplete(response)
    
        return response
    
    def logMsg(self, msgType=None, msg=None, nextLine='\n'):
        """
        A centralize function to conduct stdout prints and logging to debug file.
        if the msgType is error, the test will raise an IxSuiteStoreException and abort.
        
        msgType (str): info|warning|debug|error
        msg (str): The message to show
        nextLine (str): To add a line carriage or not to add.  Defaults to adding a new line.
        """
        if self.printStdout:
            dateAndTime = str(datetime.datetime.now()).split(' ')
            date = dateAndTime[0]
            timestamp= dateAndTime[1]
            msg = f'{nextLine}{date} {timestamp}: {msgType.upper()}: {msg}'
            print(msg)

        if self.debugLogFile:
            with open(self.debugLogFile, 'a') as logFile:
                logFile.write(f'{msg}\n')
                 
        if msgType and msgType.lower() == 'error':
            raise IxSuiteStoreException(msg)
        
    def waitForComplete(self, response):
        """
        Wait for the operation to complete with a SUCCESS.
        
        response (request object): The POST request response object.
        """
        while True:
            if 'state' not in response.json().keys():
                self.logMsg('error', f'waitForComplete:\r\n{response.json()}')
                break

            state = response.json()["state"]
            url = response.json()["url"]
            
            if state == "SUCCESS":
                self.logMsg('info', 'waitForComplete: state=SUCCESS', nextLine='')
                return
            
            elif state == "IN_PROGRESS":
                time.sleep(1)
                self.logMsg('info', msg=f'waitForComplete: state=IN_PROGRESS', nextLine='')
                response = self.request('GET', url)
                continue
            
            else:
                raise IxSuiteStoreException(f'waitForComplete failed: {response.json()}')
       
    def connect(self):
        """
        Connect to IxSuiteStore server.
        
        Return
          Example:
            {'apiKey': 'b2f87d1ac4a54472b15383dbcf74d8xx', 'sessionName': 'suitestore-ixSessionId', 
            'sessionId': 'a9b85b49-7554-46b8-94e3-53cde32a7df7', 'username': 'admin', 
            'userAccountUrl': 'https://10.x.x.x/ixsuitestore/api/v1/auth/users/1'}
        """
        url = f'{self.baseUrl}/api/v1/auth/session'
        data = {'username': self.username, 'password': self.password}
        response = self.request('POST', restApi=url, data=data, execWaitForComplete=False)
        self.headers.update({'X-Api-Key': response.json()['apiKey']})
        
        if self.sessionId:
            self.sessionUrl = f'{self.baseUrl}/api/v1/sessions/{self.sessionId}'
    
        # Note: If self.sessionId is None, startSession() will create the self.sessionUrl

        # For Keystack direct connection to the runtime session
        self.suiteStoreSession = f'{self.baseUrl}/suitestore/#/suite/{self.sessionId}/edit'
        
    def stopSession(self):
        self.request('POST', f'{self.sessionUrl}/operations/stop')
        
    def deleteSession(self):
        self.request('DELETE', self.sessionUrl)
        
    def startSession(self):
        if self.sessionId:
            self.logMsg('WARNING', f'startSession: You are connected to an existing sessionID {self.sessionId}. Starting a new session is disgarded.')
            return
        
        # Create a new session ID
        url = f'{self.baseUrl}/api/v1/sessions'
        data = {'applicationType': 'suitestore'}
        response = self.request('POST', url, data=data, execWaitForComplete=False)
        sessionId = response.json()['id']
        self.sessionUrl = f'{url}/{sessionId}'
        
        # For Keystack direct connection to the runtime session
        self.suiteStoreSession = f'{self.baseUrl}/suitestore/#/suite/{sessionId}/edit'
        
        # Start the session ID
        url = f'{self.sessionUrl}/operations/start'
        response = self.request('POST', url)
    
    def loadConfigFile(self, configFileName):
        data = {'arg2': configFileName}
        self.request('POST', f'{self.sessionUrl}/suitestore/config/operations/open?fullurls=true', data)
    
    def getPlaylist(self):
        """
        Get all the playlist
        """
        response = self.request('GET', f'{self.sessionUrl}/suitestore/config/playLists')
        return response.json()
    
    def getPlayListValueByParam(self, playListName, param):
        """
        Get a playlist value by a playlist parameter.
        
        playListName (str): The name of the playlist
        param (str): The parameter.  Below are all of the parameters in a dict format.
        
        The parameters:
        
        {'id': 15, 'name': 'ReserveSandbox', 'description': '', 'runListCount': 1, 'runState': 'pending', 
         'result': 'pending', 'maxRunListStartOrder': 1, 'changeCount': 0, 'isConfigured': True, 'order': 1, 
         'startWithPrevious': False, 'startOrder': 1, 'startDelay': 0, 
         'links': [{'rel': 'meta', 'method': 'OPTIONS', 
         'href': '/api/v1/sessions/35/suitestore/config/playLists/15'}]}
        """
        response = self.getPlaylist()
   
        for playlist in response:
            if playListName == playlist['name']:
                if param == 'href':
                    return playlist['links'][0]['href']
                else:
                    return playlist[param]
    
    def getPlaylistParameters(self, playlist):
        """
        Get a playlist parameters
        
        playlist (str): The playlist name
        
        Returns
           A list of parameters. Example:
           
           [{'name': 'PWLabOpsServer', 'value': 'PM LabOpsServer (10.36.x.x)'}, 
            {'name': 'Sandbox', 'value': 'devops'}
           ]
        """
        playlistIdUrl = self.getPlayListValueByParam(playlist, 'href')
        
        if playlistIdUrl:
            response = self.request('POST', f'{self.baseUrl}{playlistIdUrl}/operations/getParameterMap')
            return response.json()['result'][0]['parameters']
        else:
            raise IxSuiteStoreException(f'Playlist Id {playlist} url not found')
        
    def setPlaylistParameters(self, playlist, parameters):
        """
        playlist: playlist name
        
        self.baseUrl = https://10.36.86.189/ixsuitestore
        self.sessionUrl = https://10.36.86.189/ixsuitestore/api/v1/sessions/{self.sessionId}
        playlistIdUrl = /api/v1/sessions/1/suitestore/config/playLists/71
        """
        playlistIdUrl = self.getPlayListValueByParam(playlist, 'href')
        if playlistIdUrl:
            response = self.request('POST', restApi=f'{self.baseUrl}{playlistIdUrl}/operations/setParameterMap',
                                    data=parameters)
        else:
            raise IxSuiteStoreException(f'Playlist Id {playlist} url not found')

    def getRequiredParams(self, playlistName):
        """
        playlistIdUrl = /api/v1/sessions/1/suitestore/config/playLists/71
         /config/playLists/<playlist-id>/operations/getRequiredParameters
         """
        playlistIdUrl = self.getPlayListValueByParam(playlistName, 'href')
        url = self.baseUrl + playlistIdUrl + '/operations/getRequiredParameters'
        response = self.request('POST', url)
        return response.json()

    def getRunPath(self, playlistName):
        response = self.getRequiredParams(playlistName)
        runPath = response['result'][0]['runPath']
        return runPath
    
    def getProfileByType(self, profileType):
        """
        url = self.url + '/api/v1/sessions/0/' + self.appType + '/settings/profileRegistry/operations/' + 'getProfilesByType'
        """
        url = self.baseUrl + '/api/v1/sessions/0/suitestore/settings/profileRegistry/operations/getProfilesByType'
        body = { "arg2": profileType }
        response = self.request('POST', url, data=body)
        #response = requests.request('POST', url, headers=self.headers, data=json.dumps(body), verify=False)
        return response.json()

    def getAllProfiles(self):
        """
        url = self.url + '/api/v1/sessions/0/' + self.appType + '/settings/profileRegistry/profiles'
        
        Return
           {'id': 19, 'name': 'Demo LabOpsServer', 'type': 'DevOps_Demo/LabOpsServer', 'readOnly': False, 'isBuiltIn': False, 
           'links': [{'rel': 'meta', 'method': 'OPTIONS', 'href': '/api/v1/sessions/0/suitestore/settings/profileRegistry/profiles/19'}]}
       
        """
        url = self.baseUrl + '/api/v1/sessions/0/suitestore/settings/profileRegistry/profiles'
        response = self.request('GET', url)
        return response.json()

    def getProfileId(self, profileName):
        """
        Note:
           {'id': 19, 'name': 'Demo LabOpsServer', 'type': 'DevOps_Demo/LabOpsServer', 'readOnly': False, 'isBuiltIn': False, 
           'links': [{'rel': 'meta', 'method': 'OPTIONS', 'href': '/api/v1/sessions/0/suitestore/settings/profileRegistry/profiles/19'}]}
           returns the profile ID 19
        """
        response = self.getAllProfiles()
        for profile in response:
            # TODO: replace profileName to profileType
            # if profile['type'] == profileName:
            #     return profile['id']
            
            if profile['name'] == profileName:
                return profile['id']
            
    def getProfileByModuleName(self, moduleName):
        """
        url = self.url + '/api/v1/sessions/0/' + self.appType + '/settings/profileRegistry/operations/' + 'getProfilesByType'
        
        Return
        {'executionTimeMs': 5.093, 'id': '', 'state': 'SUCCESS', 'progress': 100, 'message': None, 'url': '', 'resultUrl': '', 
        'result': [{'readOnly': True, 'name': 'Default LabOpsServer', 'profileType': 'DevOps_Demo/LabOpsServer', 
        'parameters': [{'name': 'hostname', 'value': '10.0.0.1', 'internalValue': ''}, {'name': 'username', 'value': 'admin', 'internalValue': ''}, 
        {'name': 'password', 'value': 'admin', 'internalValue': ''}], 'isBuiltIn': True}, {'readOnly': False, 'name': 'Demo LabOpsServer', 
        'profileType': 'DevOps_Demo/LabOpsServer', 'parameters': [{'name': 'hostname', 'value': '10.36.84.199', 'internalValue': ''}, 
        {'name': 'username', 'value': 'admin', 'internalValue': ''}, {'name': 'password', 'value': 'Ixia4Ixia', 'internalValue': ''}], 
        'isBuiltIn': False}, {'readOnly': False, 'name': 'GitLabSDLOProfile', 'profileType': 'DevOps_Demo/LabOpsServer', 
        'parameters': [{'name': 'hostname', 'value': '0.0.0.0', 'internalValue': ''}, 
        {'name': 'username', 'value': 'admin', 'internalValue': ''}, {'name': 'password', 'value': 'admin', 'internalValue': ''}], 'isBuiltIn': False}]}
        """
        url = self.baseUrl + '/api/v1/sessions/0/suitestore/settings/profileRegistry/operations/getProfilesByModule'
        body = { "arg2": moduleName }
        response = self.request('POST', url, data=body)
        return response.json()
    
    def getProfileParameters(self, profileId):
        """"
        url = self.url + '/api/v1/sessions/0/' + self.appType + '/settings/profileRegistry/profiles/' + str(profile_id) + '/operations/getParameters'
        
        Return
           {'executionTimeMs': 0.6, 'id': '', 'state': 'SUCCESS', 'progress': 100, 'message': None, 'url': '', 'resultUrl': '', 
           'result': [{'name': 'hostname', 'value': '10.36.84.199'}, {'name': 'username', 'value': 'admin'}, 
                      {'name': 'password', 'value': 'Ixia4Ixia'}]}

        """
        url = self.baseUrl + '/api/v1/sessions/0/suitestore/settings/profileRegistry/profiles/' + str(profileId) + '/operations/getParameters'
        #response = requests.request('POST', url, headers=self.headers, verify=False)
        response = self.request('POST', url)
        return response.json()
  
    def setProfileParameters(self, profileId, parameters):
        """
        # url = self.url + '/api/v1/sessions/0/' + self.appType + '/settings/profileRegistry/profiles/' + str(profile_id) + '/operations/setParameters'
        
        profile example:                                                                                            
        {                                                                                                            
           "arg2": [                                                                                                
               {                                                                                                    
                   "arg1": "dhcp",                                                                                  
                   "arg2": "true"                                                                                   
	           },                                                                                                   
	           {                                                                                                    
	               "arg1": "hostname",                                                                              
                   "arg2": "10.10.10.10"                                                                            
               }                                                                                                    
           ]                                                                                                        
        }
        """
        url = self.baseUrl + '/api/v1/sessions/0/suitestore/settings/profileRegistry/profiles/' + str(profileId) + '/operations/setParameters'
        response = self.request('POST', url, data=parameters)
        return response.json()        

    def getCurrentRunLogs(self, sessionId, skip, take):
        pass
    
    def getLastError(self, sessionId, fullUrls=None):
        pass
    
    def startRun(self):
        response = self.request('POST', f'{self.sessionUrl}/suitestore/config/operations/start')
        return response.json()
    
    def stopRun(self):
        self.request('POST', f'{self.sessionUrl}/suitestore/config/operations/stop')

        
    def getCurrentRunResults(self, printLogMsg=True):
        '''
        Use this to get results url at the end of the test.

        {'runId': 'da42a9d9-cdc3-4434-a621-6e9de8793d94', 'runState': 'done', 'host': '', 'userName': 'admin', 'date': 1622655089475, 'dateString': '2021-06-02T17:31:29.475Z', 'duration': 6947, 'resultsDownloadUrl': '/api/v1/sessions/0/suitestore/files?filename=runda42a9d9-cdc3-4434-a621-6e9de8793d94-20210602103129.zip', 'totalCount': 1, 'passCount': 0, 'failCount': 1, 'pendingCount': 0, 'passPercent': 0.0, 'failPercent': 100.0, 'runPercent': 100.0, 'logCount': 7, 'resultsChangeCount': 148, 'reportUri': '', 'uniqueId': 'da42a9d9-cdc3-4434-a621-6e9de8793d94', '__id__': 56, 'links': [{'rel': 'self', 'method': 'GET', 'href': '/api/v1/sessions/9/suitestore/currentRun'}, {'rel': 'meta', 'method': 'OPTIONS', 'href': '/api/v1/sessions/9/suitestore/currentRun'}]}
        '''
        response = self.request('GET', f'{self.sessionUrl}/suitestore/currentRun?fullurls=true', printLogMsg=printLogMsg)
        return response.json()

    def getTestRunResultZipFile(self, targetPath=None):
        """
        Get Suite Store result files.

        Parameter
            targetPath <str>: The path to where to put the result zip file.

        resultsDownloadUrl = https://<ip>/api/v1/sessions/0/suitestore/files?filename=run66237e50-8e12-40d3-8083-51a3c0f3c8de-20210602104756.zip
        """
        response = self.getCurrentRunResults()
        resultsDownloadUrl = response['resultsDownloadUrl']
        
        headers = dict( list(self.headers.items()) + \
                        [("Accept", "text/html,application/xhtml+xml,application/xml, \
                                    application/zip;q=0.9,image/webp,image/apng,*/*;q=0.8"),
                         ("Accept-Encoding","gzip, deflate, br")])

        self.logMsg('info', f'getTestRunResultZipFile HEADERS: {headers}')
        
        # run95490758-5444-4cbe-8627-c1c3b8bf4c07-20210602125451.zip
        suiteStoreZipFile = resultsDownloadUrl.split('=')[-1]
        self.logMsg('info', f'suiteStoreZipFile: {suiteStoreZipFile}')
        
        response = self.request('GET', resultsDownloadUrl, headers=headers)
        if response.status_code != 200:
            self.logMsg('error', 'Failed to get results download url')
            
        fileObj = open(suiteStoreZipFile, 'wb')
        for chunk in response.iter_content(chunk_size=512*1024):
            if chunk:
                fileObj.write(chunk)
        
        fileObj.close()

        if targetPath:
            shutil.move(f'./{suiteStoreZipFile}', targetPath)
            
        #import io
        #from zipfile import ZipFile
        #zip_res =  ZipFile(io.BytesIO(response.content))
        #files = ZipFile.namelist(zip_res)
        #for eachFile in files:
        #    print(f'--- {eachFile}')
        
        return response
                
    def waitForTestToComplete(self, pollInterval=3):
        print('\nCurrent Run Status:')
        while True:
            results = self.getCurrentRunResults(printLogMsg=True)
                
            self.logMsg('info', f"runState={results['runState']}", nextLine='')
            if results['runState'] == 'running':
                time.sleep(pollInterval)
                continue
            else:
                self.logMsg('info', f"totalCount={results['totalCount']} passedCount={results['passCount']} failedCount={results['failCount']}")
                break
       

class IxSuiteStoreException(Exception):
    def __init__(self, msg=None):
        if platform.python_version().startswith('3'):
            super().__init__(msg)

        if platform.python_version().startswith('2'):
            super(IxSuiteStoreException, self). __init__(msg)

        showErrorMsg = '\nIxSuiteStoreException error: {0}\n\n'.format(msg)
        print(showErrorMsg)

        if IxSuiteStore.debugLogFile:
            with open(IxSuiteStore.debugLogFile, 'a') as restLogFile:
                restLogFile.write(showErrorMsg)
                


