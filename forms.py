from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, TextAreaField, \
        SubmitField
from wtforms.validators import Required, NumberRange

class ParticipantForm(Form):
    first_name = StringField('First Name', [Required()])
    last_name = StringField('Last Name', [Required()])
    age =  IntegerField('Age', [Required(), \
            NumberRange(min=13, max=100)], \
            description="How old are you?")
    major = StringField('Major', [Required()], \
            description="What is your major?")
    college_name = SelectField('College', [Required()], \
            choices=[('Arts and Letters', 'Arts and Letters'), \
            ('Business and Public Administration', 'Business and Public \
                Administration'),\
            ('Education', 'Education'), \
            ('Natural Sciences', 'Natural Sciences'), \
            ('Social and Behavioral Sciences', 'Social and Behavioral Sciences'),
            ('Extended Learning', 'Extended Learning'), \
            ('I do not know the name', 'I do not know the name')])
    academic_year = SelectField(
        'What is your academic year?',
        [Required()],
        choices=[
            (1, 'Freshman'),
            (2, 'Sophomore'),
            (3, 'Junior'),
            (4, 'Senior-first year'),
            (5, 'Senior-second year'),
            (6, 'Graduate student'),
            (7, 'Other')
        ],
        coerce=int
    )
    submit = SubmitField('Submit Information')

class SecondRoundForm(Form):
    parachute_cord = TextAreaField('Parachute cord')
    duct_tape = TextAreaField('Duct tape')
    plastic_tarp = TextAreaField('Plastic tarp')
    metal_skewers = TextAreaField('Metal skewers')

class ResearcherInfoForm(Form):
    researchers_first_name = StringField('Researcher First Name', [Required()])
    university = StringField('University Name', [Required()])
    research_id_number = IntegerField('Participant Research ID#', [Required()])
    other_id_numbers = StringField('Who is the participant playing against? Enter their research id numbers below (separate by commas)')
    #submit = SubmitField('Submit Information')

class EliminationForm(Form):
    player = SelectField(
            'Select a player for elimination:', [Required()],
             description="Active players appear in the list.",
             choices=[]
             )
    reason = TextAreaField('Why did you choose this player?', \
             [Required()], \
             description="Reason for voting to eliminate chosen player.")
    
