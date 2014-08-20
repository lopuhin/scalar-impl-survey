# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'survey_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'survey', ['Image'])

        # Adding model 'Description'
        db.create_table(u'survey_description', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'survey', ['Description'])

        # Adding model 'Filler'
        db.create_table(u'survey_filler', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Description'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Image'])),
            ('answer', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'survey', ['Filler'])

        # Adding model 'ItemSet'
        db.create_table(u'survey_itemset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'survey', ['ItemSet'])

        # Adding model 'Item'
        db.create_table(u'survey_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.ItemSet'])),
            ('description', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Description'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Image'])),
        ))
        db.send_create_signal(u'survey', ['Item'])

        # Adding model 'Participant'
        db.create_table(u'survey_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.ItemSet'])),
        ))
        db.send_create_signal(u'survey', ['Participant'])

        # Adding model 'ResultItem'
        db.create_table(u'survey_resultitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Participant'])),
            ('filler', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Filler'], null=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Item'], null=True)),
            ('answer', self.gf('django.db.models.fields.BooleanField')()),
            ('n', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'survey', ['ResultItem'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table(u'survey_image')

        # Deleting model 'Description'
        db.delete_table(u'survey_description')

        # Deleting model 'Filler'
        db.delete_table(u'survey_filler')

        # Deleting model 'ItemSet'
        db.delete_table(u'survey_itemset')

        # Deleting model 'Item'
        db.delete_table(u'survey_item')

        # Deleting model 'Participant'
        db.delete_table(u'survey_participant')

        # Deleting model 'ResultItem'
        db.delete_table(u'survey_resultitem')


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
            'filler': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Filler']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Item']", 'null': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Participant']"})
        }
    }

    complete_apps = ['survey']