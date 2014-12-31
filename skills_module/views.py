__author__ = 'brharden'

from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify

from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
from skills_module import app, lm
from models import User, Skills, db

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from forms import LoginForm, EditForm, SignupForm, SkillForm, RankSkill, SkillSearch

from read_skills import read_default_skill_list
import random

#from datetime import datetime
#import os

'''
@app.route('/')
def home():
    return render_template('index.html')
'''

# TODO: check skill strength input ranges to be 0 to 5


#
#   Some intelligence needs to be baked into these functions
#
@app.route('/skills/<engineer>', methods=['GET', 'POST'])
def skills(engineer):
    engineer = User.query.filter_by(engineer=engineer).first_or_404()
    skill_list = engineer.skills.all()

    # form = RankSkill()

    #if form.is_submitted():
     #   print "processing skill form for skill: ??? at strength of:", form.skill_strength
      #  print "form data", repr(form)
        #pass

    print "engineer: %s  skill_list: %s" % (engineer.engineer, skill_list)
    #return render_template('skills.html', title='Engineer Skills', engineer=engineer.engineer, skills=skill_list, form=form)

    return render_template('skills.html', title='Engineer Skills', engineer=engineer, skills=skill_list)


@app.route('/skill_search_result/')
def skill_search_result(requested_skill, requested_skill_level):
    request.args.get('requested_skill')
    request.args.get('requested_skill_level')
    matches = Skills.query.whoosh_search(requested_skill).all()

    print "requested skill level:", requested_skill_level
    print "matches", matches

    return render_template('skill_search_result.html', title='Engineer Capability Skill Search',
                           matches=matches, requested_skill=requested_skill, requested_skill_level=requested_skill_level)


@app.route('/skill_search', methods=['GET', 'POST'])
def skill_search():
    form = SkillSearch()

    if form.validate_on_submit():
        search_skill = form.skill_name.data
        requested_skill_level = form.requested_skill_level.data
        matches = Skills.query.whoosh_search(search_skill).all()

        print "requested skill level:", requested_skill_level
        print "matches:"
        for match in matches:
            print match.skill_engineer, match.skill_combined_names, match.skill_strength

        new_match_list = []
        for match in matches:
            print "Match skill name:", match.skill_name, " match skill strength:", match.skill_strength, " requested str", requested_skill_level
            if int(match.skill_strength) >= int(requested_skill_level):
                new_match_list.append(match)


        return render_template('skill_search_result.html', requested_skill=search_skill,
                               requested_skill_level=requested_skill_level,
                               title='Engineer Capability Skill Search', matches=new_match_list)

    return render_template('skill_search.html', title="Find Qualified Engineers", form=form)

@app.route('/add_skill/<engineer>', methods=['GET', 'POST'])
def add_skill(engineer):
    engineer = User.query.filter_by(engineer=engineer).first_or_404()

    form = SkillForm()

    if form.validate_on_submit():
        skill = Skills(skill_name=form.skill_name.data, skill_strength=form.skill_strength.data,
                       engineer=engineer, skill_engineer=engineer.engineer)

        print "skill is:" + repr(skill)

        db.session.add(skill)
        db.session.commit()
        skill_list = engineer.skills.all()
        return render_template('skills.html', title='Engineer Skills', engineer=engineer.engineer, skills=skill_list)

    return render_template('add_skill.html', title='Add a Skill', engineer=engineer.engineer, form=form)

@app.route('/update_skill_level/', methods=['POST'])
def update_skill_level():
    form_data = {key: value for key, value in request.form.items()}
    id = form_data['id']
    skill_level = form_data['skill_level']
    skill = Skills.query.filter_by(id=id).first()
    skill.skill_strength = skill_level
    db.session.commit()
    return skill_level

# use a range of 0 to 100 to generate a sort of non-linear distribution of scores from 0 to 5
def random_skill_strength():
    nim = random.randrange(0, 100)

    if nim >= 90:
        rand_strength = 5
    elif nim >= 75:
        rand_strength = 4
    elif nim >= 25:
        rand_strength = 3
    elif nim >= 15:
        rand_strength = 2
    elif nim >= 10:
        rand_strength = 1
    else:
        rand_strength = 0

    return rand_strength

def prepopulate_skills(engineer):
    skills_to_add = read_default_skill_list()

    for add_a_skill in skills_to_add:
        # get some random seeds
        rand_skill_strength = random_skill_strength()
        rand_desired_skill_strength = random_skill_strength()

        # if the desired skill is less than the current skill swap them so desired is higher
        if rand_desired_skill_strength < rand_skill_strength:
            temp = rand_skill_strength
            rand_skill_strength = rand_desired_skill_strength
            rand_desired_skill_strength = temp

        new_skill = Skills(skill_name=add_a_skill[4], skill_strength=rand_skill_strength,
                           desired_skill_strength=rand_desired_skill_strength,
                           skill_engineer=engineer.engineer, engineer=engineer,
                           skill_category_master=add_a_skill[0], skill_category_sublevel_one=add_a_skill[1],
                           skill_category_sublevel_two=add_a_skill[2], skill_category_sublevel_three=add_a_skill[3])

        new_skill.set_combined_names(skill_name=new_skill.skill_name,
                                     skill_category_master=new_skill.skill_category_master,
                                     skill_category_sublevel_one=new_skill.skill_category_sublevel_one,
                                     skill_category_sublevel_two=new_skill.skill_category_sublevel_two,
                                     skill_category_sublevel_three=new_skill.skill_category_sublevel_three)

        # print "adding skill: ", add_a_skill, "to engineer: ", engineer
        db.session.add(new_skill)

    db.session.commit()

    '''
    skill_category_master = db.Column(db.String(100))
    skill_category_sublevel_one = db.Column(db.String(100))
    skill_category_sublevel_two = db.Column(db.String(100))
    skill_category_sublevel_three = db.Column(db.String(100))
    skill_category_sublevel_four = db.Column(db.String(100))
    '''



#
#   Basic but essential stuff
#
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user

    return render_template('index.html',
                           title='Home',
                           user=user)

@lm.user_loader
def load_user(id):
    print "running load_user(" + id + ") --->  return User.query.get(int(id))"
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user

    if g.user.is_authenticated():
        # do something like add timestamp but currently don't care
        #g.user.last_seen = datetime.utcnow()
        #db.session.add(g.user)
        #db.session.commit()
        print "would have sent to message page for logged in"

        # TODO:  Redirect back to logged in url
        #return redirect(url_for('message', engineer=g.user.engineer))
        pass


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('message', engineer=g.user.engineer))

    form = LoginForm()

    #print "***"
    #print "login->form:", repr(form)
    #print "***"

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data

        # Try to get the engineer, if it doesn't exist then go to the signup page
        user = User.query.filter_by(engineer=form.engineer_id.data).first()

        # If there is a user then an engineer already exists, get their info
        if user is not None:
            return redirect(url_for('message', engineer=user.engineer))

        #   otherwise an engineer DOESN'T already exist so we need to make one
        else:
            return redirect(url_for('signup'))

        #user = User.query.filter_by(engineer='Recoil Air').first_or_404()

    return render_template('login.html',
                           title='Sign in engineer',
                           form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():

        #   Take the form data and see if there is already an existing engineer by that name
        user = User.query.filter_by(engineer=form.engineer_id.data).first()

        print "signup user, if it is 'None' then it's a new user >>> ", repr(user)
        #   that engineer already exists
        if user is not None:
            return redirect(url_for('signup'))

        #   that engineer doesn't already exist, make a new User, then add it to the db
        else:
            # make a new user
            new_engineer = User(engineer=form.engineer_id.data, engineer_name_first=form.engineer_name_first.data,
                                engineer_name_last=form.engineer_name_last.data, message=form.message.data)

            # database stuff
            db.session.add(new_engineer)
            db.session.commit()

            prepopulate_skills(new_engineer)

            # send to new homepage
            return redirect(url_for('message', engineer=new_engineer.engineer))

    return render_template('signup.html', title="Register a new engineer", form=form)

@app.route('/message/<engineer>')
def message(engineer):
    '''
    if not 'username' in session:
        return abort(403)
    return render_template('message.html', username=session['username'], message=session['message'])'''

    user = User.query.filter_by(engineer=engineer).first_or_404()

    temp_skill_url = "skills(" + engineer + ")"
    print "skill_url=", temp_skill_url

    return render_template('message.html',
                           title='motto',
                           engineer=user.engineer,
                           message=user.message,
                           skill_url=temp_skill_url)
