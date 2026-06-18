from django import forms
from cars.models import Brand, Car

    
class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
    
    def clean_value(self):
        value = self.cleaned_data['value']
        if value < 20000:
            raise forms.ValidationError('O valor deve ser maior que 20 mil reais.')
        return value
