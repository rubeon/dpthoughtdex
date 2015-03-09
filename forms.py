from django import forms

class IrssiUploadForm(forms.Form):
    title = forms.CharField(max_length=255, label="Channel Name")
    file = forms.FileField(label="Choose logfile")
    source_name = forms.CharField(max_length=255, label="Source Name (e.g., Freenode)")
    
