
import os, traceback, json
from IxSuiteStore import IxSuiteStore

class runTestcase():
    def __init__(self, keystackObj, testcase):
        self.keystackObj = keystackObj
        self.suiteStoreIp = keystackObj.envParams['suiteStoreIp']
        self.username = keystackObj.envParams['username']
        self.password = keystackObj.envParams['password']
        self.suiteStoreConfigFile = keystackObj.envParams['configs']['suiteStoreConfigFile']
        self.testcase = testcase
    
    def run(self):
        session = IxSuiteStore(self.suiteStoreIp, self.username, self.password, sessionId=None)
        
        self.keystackObj.updateStatusData('Started')
        session.connect()
        session.startSession()
        
        # Update the status.json with the session URL
        self.keystackObj.statusData['cases'][self.keystackObj.statusData['currentlyRunning']]['testSessionId'] = session.suiteStoreSession
        self.keystackObj.updateStatusData('Loading Config File')
        
        session.loadConfigFile(configFileName=self.suiteStoreConfigFile)
        
        # [{'id': 3, 'name': 'PlayList 1', 'description': '', 'runListCount': 1, 'runState': 'pending', 'result': 'pending', 'maxRunListStartOrder': 1, 'changeCount': 0, 'isConfigured': False, 'order': 1, 'startWithPrevious': False, 'startOrder': 1, 'startDelay': 0, 'links': [{'rel': 'meta', 'method': 'OPTIONS', 'href': '/api/v1/sessions/15/suitestore/config/playLists/3'}]}]
        playlistObj = session.getPlaylist()
        
        playlistId = playlistObj[0]['id'] # 3
        playlistName = playlistObj[0]['name'] # Playlist 1
        runPath = session.getRunPath(playlistName) # runlist/1
    
        self.keystackObj.writeToTestcaseLogFile(f'SuiteStore Session URL: {session.suiteStoreSession}')
        
        # For understanding what the parameters to get for the loaded .sscfg file
        #
        # getRequiredParams: {'executionTimeMs': 0.9, 'id': '', 'state': 'SUCCESS', 'progress': 100, 'message': None, 'url': '', 'resultUrl': '', 'result': [{'runPath': 'runList/1', 'runListOrder': '1', 'isConfigured': False, 'path': 'TOOLS/TOOLS_TS/PYTEST_WRAPPER', 'displayPath': 'Tools/Tools Test Suite/PyTest Wrapper', 'displayName': 'PyTest Wrapper', 'description': '', 'parameters': [{'name': 'PyTest', 'displayName': 'PyTest Zip Folder To Import', 'order': 1, 'registrationType': 'script', 'parameterType': 'file', 'defaultValue': '', 'hasDefault': False, 'typeDefaultValue': 'pytest_demo.zip', 'description': 'Import Pytest top level folder', 'help': '', 'value': '', 'internalValue': '', 'moduleName': 'TOOLS', 'details': {'moduleName': 'TOOLS', 'choices': ['pytest_demo.zip', 'pytest.ini', 'pytest_demo2.zip', 'regressionTest.zip']}, 'parameterGroup': 'PyTest Wrapper', 'groupOrder': 4, 'scope': 'default', 'isActive': True, 'valueChangeHandlers': []}, {'name': 'ProvidePyTestIni', 'displayName': 'Import a custom pytest.ini File?', 'order': 3, 'registrationType': 'script', 'parameterType': 'bool', 'defaultValue': 'False', 'hasDefault': True, 'typeDefaultValue': 'false', 'description': 'Do you want to import a custom pytest.ini file and also be able to make edits in Suite Store?', 'help': '', 'value': 'False', 'internalValue': '', 'moduleName': 'TOOLS', 'details': {}, 'parameterGroup': 'PyTest Wrapper', 'groupOrder': 4, 'scope': 'default', 'isActive': True, 'valueChangeHandlers': [{'condition': {'comparison': 'equalTo', 'value': 'True'}, 'enables': ['PytestIniFile'], 'disables': []}, {'condition': {'comparison': 'equalTo', 'value': 'False'}, 'enables': [], 'disables': ['PytestIniFile']}]}]}]}
        self.keystackObj.writeToTestcaseLogFile(f'getRequiredParams: {json.dumps(session.getRequiredParams(playlistName), indent=4)}')
        
        self.keystackObj.writeToTestcaseLogFile(f"SuiteStore config params: {json.dumps(self.keystackObj.envParams['configs']['parameters'], indent=4)}")
        
        if 'parameters' in self.keystackObj.envParams['configs']:
            parameters = { "arg2": [
                {"runPath": runPath,
                    "parameters": self.keystackObj.envParams['configs']['parameters']
                }
            ]}
            
            session.setPlaylistParameters(playlistName, parameters)
        
        self.keystackObj.updateStatusData('Running')
        startRunResult = session.startRun()
        print('\n--- startRunResult:', startRunResult)
        
        session.waitForTestToComplete(pollInterval=3)
        
        # results: {'runId': 'd2318bbb-bb74-42dc-98d1-5e1207cca387', 'runState': 'starting', 'host': '', 'userName': 'admin', 'date': 1649190249784, 'dateString': '2022-04-05T20:24:09.784Z', 'duration': 0, 'resultsDownloadUrl': '', 'totalCount': 1, 'passCount': 0, 'failCount': 0, 'pendingCount': 1, 'passPercent': 0.0, 'failPercent': 0.0, 'runPercent': 0.0, 'logCount': 2, 'resultsChangeCount': 220, 'reportUri': '', 'uniqueId': 'd2318bbb-bb74-42dc-98d1-5e1207cca387', '__id__': 80, 'links': [{'rel': 'self', 'method': 'GET', 'href': 'https://172.16.1.5/ixsuitestore/api/v1/sessions/20/suitestore/currentRun'}, {'rel': 'meta', 'method': 'OPTIONS', 'href': 'https://172.16.1.5/ixsuitestore/api/v1/sessions/20/suitestore/currentRun'}]}
        results = session.getCurrentRunResults()
        self.keystackObj.writeToTestcaseLogFile(results['failCount'])
        
        if results['failCount'] > 0:
            self.keystackObj.testcaseResult = 'Failed'


