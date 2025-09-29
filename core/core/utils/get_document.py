from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_document(request):
    return HttpResponse("document/PERSONAL_DATA_AGREEMENT")
