from django import forms 

class NodeCreationForm(forms.Form):
    name = forms.CharField( 
        label="Name", max_length=225, required = True,
        widget=forms.TextInput( attrs={'class': ''} ),
        error_messages={ 'required': 'The name should not be empty' }
    )   