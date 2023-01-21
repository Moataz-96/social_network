# users/tasks.py

import json
from celery import shared_task
import requests
from config import settings
from users import serializers
from requests.adapters import HTTPAdapter, Retry


@shared_task()
def geolocation_info_task(ip, user_id, current_date):
    req_session = requests.Session()
    req_session.mount('https://', HTTPAdapter(max_retries=Retry(total=5)))

    response = req_session.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_IP_KEY}&ip_address={ip}")
    country = json.loads(response.content)['country_code']
    response = req_session.get(f"https://holidays.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_HOLIDAYS_KEY}&country={country}&{current_date}")
    holidays = json.loads(response.content)

    for _iter in range(len(holidays)):
        holidays[_iter]['user'] = user_id
    print(holidays)
    instance = serializers.UserHolidaysSerializer(data=holidays, many=True)
    if instance.is_valid():
        instance.save()
    else:
        raise Exception(instance.errors)
