#!/usr/bin/python3

# This file contains all the mongoengine models used in the application

from mongoengine import Document, StringField, FileField
class Documents(Document):
    candidate_id = StringField(required=True)
    resume = FileField()
    national_id_copy = FileField()
    photo = FileField()
    application_letter = FileField()
    degree_copy = FileField()