from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searchFor = StringField('What are you looking for?')
    orderBy = SelectField('Order By', choices=[('name', 'Product Name'), ('brand', 'Product Brand'),
                                               ('price', ' Product Price'), ('rating', 'Product Rating')])
