from django import forms
import datetime
from django.core.exceptions import ValidationError

class RenovarLivroForm(forms.Form):
    data_renovacao = forms.DateField(help_text="Entre com uma data entre agora e 4 semanas (default 3).")

    def validar_data_renovacao(self):

        data = self.cleaned_data['data_renovacao']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError('Data inválida - renovação no passado.')

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Data inválida - renovação com mais de 4 semanas.')

        # Remember to always return the cleaned data.
        return data
        