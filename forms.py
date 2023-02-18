from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList,FormField, RadioField,IntegerField 
from wtforms.fields import EmailField

class UserForm(Form):
    matricula=StringField('Matricula')
    nombre=StringField('Nombre')
    apaterno=StringField('Apaterno')
    amanterno=StringField('Amaterno')
    email=StringField('Correo')

class BoxForm(Form):
    numCant = IntegerField('Ingresa el número de cajas a realizar')
    num = FieldList(StringField('Ingresa el número'))