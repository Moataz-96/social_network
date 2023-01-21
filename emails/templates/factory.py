from emails.templates import *


class TemplateFactory(object):

    def __new__(cls, engine):
        try:
            template_engine = dict(verification=Verification(),)
            return template_engine[engine]
        except Exception as err:
            raise Exception(f"ERROR: Invalid request, " + str(err))
