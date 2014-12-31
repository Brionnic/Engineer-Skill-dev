__author__ = 'brharden'

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Required
from wtforms.validators import DataRequired, Length
from models import Skills, db

class LoginForm(Form):
    engineer_id = StringField('engineer_id', validators=[DataRequired()])

    print "***"
    print "LoginForm->engineer_id", repr(engineer_id)
    print "***"

    remember_me = BooleanField('remember_me', default=False)

    def __repr__(self):
        return '<engineer_id %r> <remember_me %r>' % (self.engineer_id, str(self.remember_me))


class EditForm(Form):
    message = StringField('message', validators=[DataRequired()])

class SignupForm(Form):
    engineer_id = StringField('engineer_id', validators=[DataRequired()])
    engineer_name_first = StringField('engineer_name_first', validators=[DataRequired()])
    engineer_name_last = StringField('engineer_name_last', validators=[DataRequired()])

    message = StringField('engineer_id', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SkillForm(Form):
    skill_name = StringField('skill_name', validators=[DataRequired()])
    skill_strength = IntegerField('skill_strength', validators=[DataRequired()])

class RankSkill(Form):
    skill_strength = IntegerField('skill_strength', validators=[DataRequired()])

class SkillSearch(Form):
    #skill_name = StringField('skill_name', validators=[DataRequired()])
    skills = [(skill[0], skill[0]) for skill in db.session.query(Skills.skill_name).distinct()]
    skill_name = SelectField(u'skill_name', choices=skills)
    requested_skill_level = IntegerField('requested_skill_level', validators=[DataRequired()])


