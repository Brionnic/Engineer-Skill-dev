__author__ = 'Snoopy'

from skills_module import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    engineer = db.Column(db.String(12), index=True, unique=True)
    engineer_name_first = db.Column(db.String(26))
    engineer_name_last = db.Column(db.String(40))

    message = db.Column(db.String(255))

    #flights = db.relationship("Flights", backref='engineer', lazy='dynamic')
    skills = db.relationship("Skills", backref='engineer', lazy='dynamic')

    def __init__(self, engineer, engineer_name_first, engineer_name_last, message):
        self.engineer = engineer

        self.engineer_name_first = engineer_name_first
        self.engineer_name_last = engineer_name_last

        self.message = message

    def __repr__(self):
        return '<Engineer %r> <Motto %r>' % (self.engineer, self.message)

class Skills(db.Model):
    __searchable__ = ['skill_combined_names']

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    skill_engineer = db.Column(db.String(12))
    skill_name = db.Column(db.String(100))
    skill_strength = db.Column(db.Integer)
    desired_skill_strength = db.Column(db.Integer)

    #   Primary skill is the Master, there are 3-4 of these master categories
    #   Then there are 4 levels of sub category
    #
    skill_category_master = db.Column(db.String(100))
    skill_category_sublevel_one = db.Column(db.String(100))
    skill_category_sublevel_two = db.Column(db.String(100))
    skill_category_sublevel_three = db.Column(db.String(100))
    skill_category_sublevel_four = db.Column(db.String(100))
    skill_combined_names = db.Column(db.String(600))

    def set_combined_names(self, skill_name, skill_category_master, skill_category_sublevel_one, skill_category_sublevel_two, skill_category_sublevel_three):
        self.skill_combined_names = skill_name + "." + skill_category_master + "." + skill_category_sublevel_one + "." + skill_category_sublevel_two + "." + skill_category_sublevel_three

    # def __init__(self, skill_engineer, skill_name, skill_strength, desired_skill_strength,
    #              skill_category_master, skill_category_sublevel_one, skill_category_sublevel_two,
    #              skill_category_sublevel_three, engineer):
    #
    #     self.engineer = engineer
    #     self.skill_engineer = skill_engineer
    #     self.skill_name = skill_name
    #     self.skill_strength = skill_strength
    #     self.desired_skill_strength = desired_skill_strength
    #     self.skill_category_master = skill_category_master
    #     self.skill_category_sublevel_one = skill_category_sublevel_one
    #     self.skill_category_sublevel_two = skill_category_sublevel_two
    #     self.skill_category_sublevel_three = skill_category_sublevel_three
    #     self.skill_combined_names = skill_name + "." + skill_category_master + "." + skill_category_sublevel_one + "." + skill_category_sublevel_two + "." + skill_category_sublevel_three



    def __repr__(self):
        temp_string = ""
        temp_string += '<Engineer: %r>/n' % (self.skill_engineer)
        temp_string += '<Skill Name: %r>/n' % (self.skill_name)
        temp_string += '<Skill Strength: %r>/n' % (str(self.skill_strength))
        temp_string += '<Skill Category Master: %r>/n' % (self.skill_category_master)
        temp_string += '<Skill Subcategory 1: %r>/n' % (self.skill_category_sublevel_one)
        temp_string += '<Skill Subcategory 2: %r>/n' % (self.skill_category_sublevel_two)
        temp_string += '<Skill Subcategory 3: %r>/n' % (self.skill_category_sublevel_three)
        temp_string += '<Skill Subcategory 4: %r>/n' % (self.skill_category_sublevel_four)

        return temp_string

if enable_search:
    print "Whoosh enabled for 'skills'"
    whooshalchemy.whoosh_index(app, Skills)