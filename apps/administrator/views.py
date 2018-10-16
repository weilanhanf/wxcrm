from django.shortcuts import render_to_response


# Create your views here.
def page_not_found(request):
    """404页面: 请求错误"""
    response = render_to_response('404.html', {})
    response.status_code = 404
    return  response


def page_error(request):
    """500页面：服务器出错"""
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response