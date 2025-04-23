from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from topbar.settings.accountMgmt.verifyLogin import authenticateLogin
from globalVars import HtmlStatusCodes
    
    
class Testcases(View):
    @authenticateLogin
    def get(self, request):
        """
        Called by base.html sidebar/testcases
        """
        user = request.session['user']
        status = HtmlStatusCodes.success

        return render(request, 'testcases.html',
                      {'mainControllerIp': request.session['mainControllerIp'],
                       'topbarTitlePage': 'Testcase Mgmt',
                       'user': user
                      }, status=status)
