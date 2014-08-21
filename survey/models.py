# -*- encoding: utf-8 -*-

from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Картинка'
        verbose_name_plural = u'Картинки'


class Description(models.Model):
    text = models.TextField(verbose_name=u'Описание')

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = u'Описание'
        verbose_name_plural = u'Описания'


class Filler(models.Model):
    description = models.ForeignKey(Description)
    image = models.ForeignKey(Image)
    answer = models.BooleanField(verbose_name=u'Правильный ответ',
            blank=True)

    class Meta:
        verbose_name = u'Филлер'
        verbose_name_plural = u'Филлеры'

    def __unicode__(self):
        return u'%s: %s' % (self.image, self.description)


class ItemSet(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Лист'
        verbose_name_plural = u'Листы'

    def __unicode__(self):
        return u'Лист №%d' % self.id


class Item(models.Model):
    item_set = models.ForeignKey(ItemSet, verbose_name=u'Лист')
    description = models.ForeignKey(Description)
    image = models.ForeignKey(Image)

    class Meta:
        verbose_name = u'Элемент листа'
        verbose_name_plural = u'Элементы листа'

    def __unicode__(self):
        return u'%s: %s' % (self.image, self.description)


class Participant(models.Model):
    item_set = models.ForeignKey(ItemSet)

    def __unicode__(self):
        return u'%d: %s' % (self.id, self.item_set)


class ResultItem(models.Model):
    participant = models.ForeignKey(Participant)
    filler = models.ForeignKey(Filler, null=True)
    item = models.ForeignKey(Item, null=True)
    answer = models.BooleanField()
    n = models.IntegerField()
    dt = models.DateTimeField(auto_now_add=True, null=True)
