from django import forms


def validate_not_empty(text):
    if text == '':
        raise forms.ValidationError(
            'А это поле кто заполнять будет , Пушкин?',
            params={'text': text}
        )
