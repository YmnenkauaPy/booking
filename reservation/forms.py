from django import forms


class FilterForm(forms.Form):
    FILTER_CHOICES = [
        ('increase', "За зростанням"),
        ('decrease', "За спаданням"),
    ]

    filter = forms.ChoiceField(choices=FILTER_CHOICES, required=False, initial='increase')
