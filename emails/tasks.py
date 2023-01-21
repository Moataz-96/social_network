# emails/tasks.py

from celery import shared_task
from emails.templates.factory import TemplateFactory
from users.models import CustomUser


@shared_task()
def send_email(id, template_engine):
    user = CustomUser.objects.get(id=id)
    template = TemplateFactory(engine=template_engine)
    template.send(user)
