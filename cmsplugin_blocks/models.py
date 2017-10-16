# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

#from filebrowser.fields import FileBrowseField

from cms.models.pluginmodel import CMSPlugin


class Cmsplugin_blocks(CMSPlugin):
    title = models.CharField(
        _(u"Title"),
        max_length=120,
    )
    #image = FileBrowseField(
        #_('image'),
        #max_length=255,
        #null=True,
        #blank=True,
        #default=None,
    #)
    description = models.TextField(
        _(u"Description"),
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Cmsplugin_blocks, self).save(*args, **kwargs)
