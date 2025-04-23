import * as commons from './commons.js';

document.addEventListener("DOMContentLoaded", function() {
    //getTestcasesTopLevel()
    commons.getInstantMessages('testcases');
    commons.getServerTime();
})

/*
async function getTestcasesTopLevel() {
    try {
        console.log(`getTestcasesTopLevel()`)
        const data = await commons.postData("/api/v1/testcases/topLevelInternal",  
                {remoteController: sessionStorage.getItem("remoteController")})

        if (data.status == "failed") {
            document.querySelector("#flashingError").innerHTML = '<strong>Error</strong>';
        } else {
            document.querySelector("#insertTestcases").innerHTML = data.testcases;
            await addListeners("caret2");
        }

    } catch (error) {    
        alert("getTestcasesTopLevel() error: " + error);
    }
    commons.getInstantMessages('testcases');
}
*/

const  getTestcaseContents = async (object) => {
    try {
        //const testcaseFullPath = object.getAttribute('testcaseFullPath');
        const testcaseFullPath = object;
        console.log(`getTestcaseContents(): ${testcaseFullPath}`)

        const data = await commons.postData("/api/v1/testcase/getContents",  
                {remoteController: sessionStorage.getItem("remoteController"),
                 mainController: sessionStorage.getItem("mainControllerIp"),
                 testcaseFullPath: testcaseFullPath})

        if (data.status == "failed") {
            document.querySelector("#flashingError").innerHTML = '<strong>Error</strong>';
        } else {
            document.querySelector("#showTestcaseContentsModal").style.display = 'block';
            document.querySelector("#testcaseFilePath").innerHTML = `Testcase:&ensp;&ensp;${testcaseFullPath}`;
            document.querySelector("#insertTestcaseContents").innerHTML = `<textarea id="testcaseContentsTextareaId" cols="135" rows="30">${data.testcaseContents}</textarea>`;
            //await addListeners("caret2");
        }

    } catch (error) {    
        alert("getTestcaseContents() error: " + error);
    }
}

const modifyFileTestcase = async () => {
    /* Modify existing env */
    try {
        const testcasePathTitle = document.querySelector('#testcaseFilePath').innerHTML;
        const testcaseTitleSplit = envPathTitle.split("Testcase:\u2002");
        const testcasePath = testcaseTitleSplit[1];
        const textarea = document.querySelector('#testcaseContentsTextareaId').value;

        const data = await commons.postData("/api/v1/fileMgmt/modifyFile",  
                                            {remoteController: sessionStorage.getItem("remoteController"),
                                             mainController: sessionStorage.getItem("mainControllerIp"), 
                                             textarea: textarea,
                                             filePath: testcasePath})

        if (data.status == "success") {
            const status = `<div style='color:green'>Successfully modified Env</div>`;
            document.querySelector("#modifyTestcaseStatus").innerHTML = status;
        } else {
            const status = `<div style='color:red'>Failed: ${data.errorMsg}</div>`;
            document.querySelector("#modifyTestcaseStatus").innerHTML = status;
        }
    } catch (error) {    
        console.error(`modifyFileTestcase error: ${error}`);
    }
}

const closeShowTestcaseContentsModal = () => {
    document.querySelector('#showTestcaseContentsModal').style.display = 'none';
    document.querySelector('#testcaseFilePath').innerHTML = 'Testcase:&ensp;';
    document.querySelector("#insertTestcaseContents").innerHTML = '';
}


async function addListeners(caretName="caret2", newVarName='x') {
    // caret2
    //let toggler = document.getElementsByClassName(caretName);
    window[caretName] = document.getElementsByClassName(caretName);

    for (let x= 0; x < window[caretName].length; x++) {
        window[caretName][x].addEventListener("click", function() {
            this.parentElement.querySelector(".nested").classList.toggle("active");
            //this.classList.toggle("caret-down");               
        });
    }
}

//window.getTestcasesTopLevel = getTestcasesTopLevel;
window.getTestcaseContents = getTestcaseContents;
window.closeShowTestcaseContentsModal = closeShowTestcaseContentsModal;
//window.closeShowModifyTestcasesModal = closeShowModifyTestcasesModal;

