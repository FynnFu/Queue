from django import forms


class QueueForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required': "Please Enter Queue Name"
        })
    password = forms.CharField(
        error_messages={
            'required': "Please Enter Queue Password"
        })
