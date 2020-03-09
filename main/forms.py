from django import forms


class TagsForm(forms.Form):
    word = forms.CharField(
        label='タグ',
        max_length=50,
        required=True,
        widget=forms.TextInput()
    )
    score = forms.IntegerField(
        label='スコア',
        max_value=1000,
        required=True,
        widget=forms.NumberInput()
    )
