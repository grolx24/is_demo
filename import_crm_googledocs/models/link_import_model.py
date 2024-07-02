import os

import requests
from django.conf import settings
from django.db import models


class LinkImport(models.Model):
    link_google_docs = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.link_google_docs = "/".join(self.link_google_docs.split("/")[0:-1]) + "/export"
        super(LinkImport, self).save(*args, **kwargs)

    def download_xlsx(self):
        res = requests.get(self.link_google_docs)
        filename = os.path.join(settings.BASE_DIR, 'temp.xlsx')
        with open(filename, 'wb') as f:
            f.write(res.content)

        return filename


