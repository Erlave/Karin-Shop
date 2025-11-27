import requests
from django.conf import settings
from kavenegar import *
from celery import shared_task
from kavenegar import KavenegarAPI
from api_key import API



def send_sms(receptor, message):
    """
    ارسال پیامک با کاوه‌نگار
    receptor: شماره گیرنده (مثل '09120000000')
    message: متن پیامک
    """
    api = API
    params = { 'sender' : '2000660110', 'receptor': receptor, 'message' :message }
    response = api.sms_send(params)


    try:
        return response.json()
    except Exception:
        return {"status": "error", "response": str(response)}
    
    
    
    
    
  



# @shared_task
# def send_sms_async(receptor, message):
#     """
#     Task غیرهمزمان برای ارسال پیامک
#     """
#     api = KavenegarAPI('6C64644B46674D3751437A44715A2F727278746B70305336456F6D314A6E7147564C645A6F6845396270733D')
#     params = {
#         'sender': '2000660110',
#         'receptor': receptor,
#         'message': message
#     }
    
#     response = api.sms_send(params)
    
    
#     try:
#         return response.json()  # Celery نیاز داره مقداری برگشت داده بشه
#     except Exception:
#         return {"status": "error", "response": str(response)}