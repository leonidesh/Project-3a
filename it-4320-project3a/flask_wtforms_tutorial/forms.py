"""Form class declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length
import csv


class StockForm(FlaskForm):
    """Generate Your Graph."""

    #THIS IS WHERE YOU WILL IMPLEMENT CODE TO POPULATE THE SYMBOL FIELD WITH STOCK OPTIONS
    #using the alphavantage api ---if doesn't work, use a json or a csv file--
    symbol = SelectField("Choose Stock Symbol",[DataRequired()],
        #用csv读取nyse-listed.csv
        choices=[(row[0],row[0]) for row in csv.reader(open('nyse-listed.csv'))]
    )
    #     choices=[
    #         ("IBM", "IBM"),
    #         ("GOOGL", "GOOGL"),
    #     ],
    # )
    #如果choice不是7个以内的大写字母，就报错

    chart_type = SelectField("Select Chart Type",[DataRequired()],
        choices=[
            ("1", "1. Bar"),
            ("2", "2. Line"),
        ],
    )

    time_series = SelectField("Select Time Series",[DataRequired()],
        choices=[
            ("1", "1. Intraday"),
            ("2", "2. Daily"),
            ("3", "3. Weekly"),
            ("4", "4. Monthly"),
        ],
    )

    start_date = DateField("Enter Start Date")
    end_date = DateField("Enter End Date")
    submit = SubmitField("Submit")



