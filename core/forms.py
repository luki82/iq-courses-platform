from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Spam trap: hidden from people, but simple bots fill in every field.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}))

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "topic", "message"]
        labels = {"name": "Your name", "email": "Your email", "topic": "What is it about?", "message": "Message"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "maxlength": 100, "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
            "topic": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 6, "maxlength": 5000}),
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write a little more so we can help (at least 10 characters).")
        if len(message) > 5000:
            raise forms.ValidationError("Please keep your message under 5,000 characters.")
        return message

    def is_spam(self) -> bool:
        return bool(self.cleaned_data.get("website"))
