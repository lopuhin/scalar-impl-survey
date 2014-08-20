# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ResultItem.dt'
        db.add_column(u'survey_resultitem', 'dt',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ResultItem.dt'
        db.delete_column(u'survey_resultitem', 'dt')


    models = {
        u'survey.description': {
            'Meta': {'object_name': 'Description'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'survey.filler': {
            'Meta': {'object_name': 'Filler'},
            'answer': ('django.db.models.fields.BooleanField', [], {}),
            'description': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Description']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Image']"})
        },
        u'survey.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'survey.item': {
            'Meta': {'object_name': 'Item'},
            'description': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Description']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Image']"}),
            'item_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.ItemSet']"})
        },
        u'survey.itemset': {
            'Meta': {'object_name': 'ItemSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'survey.participant': {
            'Meta': {'object_name': 'Participant'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.ItemSet']"})
        },
        u'survey.resultitem': {
            'Meta': {'object_name': 'ResultItem'},
            'answer': ('django.db.models.fields.BooleanField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'filler': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Filler']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Item']", 'null': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Participant']"})
        }
    }

    complete_apps = ['survey']