from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class EntryForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(message="Le nom est obligatoire")])
    amount = FloatField("Montant", validators=[
        DataRequired(message="Le montant est obligatoire"),
        NumberRange(min=0, message="Le montant doit être positif")
    ])
    category = StringField("Catégorie", validators=[Optional()])
    submit = SubmitField("Enregistrer")