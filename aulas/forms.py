# aulas/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Reserva, Curso

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['aula', 'curso', 'fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Recibimos el usuario desde la vista
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtrar cursos para mostrar solo los del profesor
        if self.user:
            self.fields['curso'].queryset = Curso.objects.filter(profesor=self.user)

    def clean(self):
        cleaned_data = super().clean()
        curso = cleaned_data.get('curso')

        # Validar que el curso pertenece al profesor
        if curso and self.user and curso.profesor != self.user:
            raise ValidationError("Solo puedes reservar aulas para tus propios cursos.")

        # Validación de horas y solapamiento (la que ya tienes)
        aula = cleaned_data.get('aula')
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

        if aula and fecha and hora_inicio and hora_fin:
            solapadas = Reserva.objects.filter(
                aula=aula,
                fecha=fecha
            ).exclude(pk=self.instance.pk).filter(
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            )
            if solapadas.exists():
                raise ValidationError("Ya existe una reserva que se solapa en esta aula para esa fecha.")

        return cleaned_data
