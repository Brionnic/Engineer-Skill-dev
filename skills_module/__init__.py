__author__ = 'Snoopy'

from flask import Flask, render_template, request, redirect, url_for, abort, session
from flask.ext.login import LoginManager

# from flask_assets import Environment
# from webassets.loaders import PythonLoader as PythonAssetsLoader

# from flask_sqlalchemy import SQLAlchemy
# from config import basedir

import os
#import assets

app = Flask(__name__)

app.config.from_object('config')
app.config['SECRET_KEY'] = "qsceszwsxasd123"

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from skills_module import views, models

# ...

# assets_env = Environment(app)
# assets_loader = PythonAssetsLoader(assets)
# for name, bundle in assets_loader.load_bundles().iteritems():
#     assets_env.register(name, bundle)

# ...

# env = os.environ.get('EXAMPLE_ENV', 'prod')
# app.config.from_objects('example.settings.%sConfig' % env.capitalize())
# app.config['ENV'] = env



if __name__ == '__main__':
    app.run()



