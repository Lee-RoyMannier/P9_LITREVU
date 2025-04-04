from django import forms
from . import models


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (0, "0 ⭐"),
        (1, "1 ⭐"),
        (2, "2 ⭐"),
        (3, "3 ⭐"),
        (4, "4 ⭐"),
        (5, "5 ⭐"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label="Note"
    )

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
