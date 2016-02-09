from django import forms


class AddForm(forms.Form):
    mainimage = forms.ImageField(label='mainimage',required=False)
    sentence = forms.CharField(label='sentence',max_length=500,required=False)
    author = forms.CharField(label='author',max_length=100,required=False)
    
class LikeForm(forms.Form):
    liked_item = forms.IntegerField(label="liked_item")