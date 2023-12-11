from .models import PageReview
from django import forms


class PageReviewForm(forms.ModelForm):
    class Meta:
        model = PageReview
        fields = ["reviewer", "content"]


class HealthDataForm(forms.Form):
    STATE_CHOICES = (
        ("BE", "Belgium"),
        ("BG", "Bulgaria"),
        ("CZ", "Czechia"),
        ("DK", "Denmark"),
        ("DE", "Germany"),
        ("EE", "Estonia"),
        ("IE", "Ireland"),
        ("EL", "Greece"),
        ("ES", "Spain"),
        ("FR", "France"),
        ("HR", "Croatia"),
        ("IT", "Italy"),
        ("CY", "Cyprus"),
        ("LV", "Latvia"),
        ("LT", "Lithuania"),
        ("LU", "Luxembourg"),
        ("HU", "Hungary"),
        ("MT", "Malta"),
        ("NL", "Netherlands"),
        ("AT", "Austria"),
        ("PL", "Poland"),
        ("PT", "Portugal"),
        ("RO", "Romania"),
        ("SI", "Slovenia"),
        ("SK", "Slovakia"),
        ("FI", "Finland"),
        ("NO", "Norway"),
        ("SE", "Sweden"),
        ("IS", "Iceland"),
        ("CH", "Switzerland"),
    )
    REPORT_CHOICES = (
        ("HLY_0", "Healthy life years in absolute value at birth"),
        ("LE_0", "Life expectancy in absolute value at birth"),
        ("HLY_50", "Healthy life years in absolute value at 50"),
        ("LE_50", "Life expectancy in absolute value at 50"),
        ("HLY_65", "Healthy life years in absolute value at 65"),
        ("LE_65", "Life expectancy in absolute value at 65"),
    )

    TIME_CHOICES = (
        (2010, 2010),
        ("2011", "2011"),
        ("2012", "2012"),
        ("2013", "2013"),
        ("2014", "2014"),
        ("2015", "2015"),
        ("2016", "2016"),
        ("2017", "2017"),
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
    )

    select_field = forms.MultipleChoiceField(
        choices=STATE_CHOICES
    )  # Choose state/states
    select_field2 = forms.MultipleChoiceField(
        choices=REPORT_CHOICES
    )  # Choose report type/types
    select_field3 = forms.ChoiceField(
        choices=TIME_CHOICES
    )  # Choose Healthy life years year

    def __init__(self, *args, **kwargs):
        super(HealthDataForm, self).__init__(*args, **kwargs)
        all_state_choices = [("all", "Select All")] + list(self.STATE_CHOICES)
        self.fields["select_field"].choices = all_state_choices
        self.fields["select_field"].widget.attrs["size"] = 7
        self.fields["select_field"].widget.attrs["style"] = "width: 100px;"

        all_report_choices = [("all", "Select All")] + list(self.REPORT_CHOICES)
        self.fields["select_field2"].choices = all_report_choices
        self.fields["select_field2"].widget.attrs["size"] = 7
        self.fields["select_field2"].widget.attrs["style"] = "width: 350px;"

        self.fields["select_field3"].widget.attrs["class"] = "custom-select"
        self.fields["select_field3"].widget.attrs["style"] = "width: 150px;"

    def clean_select_field(self):
        data = self.cleaned_data["select_field"]
        if "all" in data:
            return [choice[0] for choice in self.STATE_CHOICES if choice[0] != "all"]
        return data

    def clean_select_field2(self):
        data = self.cleaned_data["select_field2"]
        if "all" in data:
            return [choice[0] for choice in self.REPORT_CHOICES if choice[0] != "all"]
        return data


class IndexDataForm(forms.Form):
    STATE_CHOICES = (
        ("BE", "Belgium"),
        ("BG", "Bulgaria"),
        ("CZ", "Czechia"),
        ("DK", "Denmark"),
        ("DE", "Germany"),
        ("EE", "Estonia"),
        ("IE", "Ireland"),
        ("EL", "Greece"),
        ("ES", "Spain"),
        ("FR", "France"),
        ("HR", "Croatia"),
        ("IT", "Italy"),
        ("CY", "Cyprus"),
        ("LV", "Latvia"),
        ("LT", "Lithuania"),
        ("LU", "Luxembourg"),
        ("HU", "Hungary"),
        ("MT", "Malta"),
        ("NL", "Netherlands"),
        ("AT", "Austria"),
        ("PL", "Poland"),
        ("PT", "Portugal"),
        ("RO", "Romania"),
        ("SI", "Slovenia"),
        ("SK", "Slovakia"),
        ("FI", "Finland"),
        ("NO", "Norway"),
        ("SE", "Sweden"),
        ("IS", "Iceland"),
        ("CH", "Switzerland"),
    )

    TIME_CHOICES = (
        ("2010", "2010"),
        ("2011", "2011"),
        ("2012", "2012"),
        ("2013", "2013"),
        ("2014", "2014"),
        ("2015", "2015"),
        ("2016", "2016"),
        ("2017", "2017"),
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
        ("2021", "2021"),
    )

    select_field = forms.MultipleChoiceField(
        choices=TIME_CHOICES
    )  # European People's Health Indexses period
    select_field2 = forms.MultipleChoiceField(
        choices=STATE_CHOICES
    )  # Choose state/states

    def __init__(self, *args, **kwargs):
        super(IndexDataForm, self).__init__(*args, **kwargs)
        all_state_choices = [("all", "Select All")] + list(self.TIME_CHOICES)
        self.fields["select_field"].choices = all_state_choices
        self.fields["select_field"].widget.attrs["size"] = 7
        self.fields["select_field"].widget.attrs["style"] = "width: 100px;"

        all_report_choices = [("all", "Select All")] + list(self.STATE_CHOICES)
        self.fields["select_field2"].choices = all_report_choices
        self.fields["select_field2"].widget.attrs["size"] = 7
        self.fields["select_field2"].widget.attrs["style"] = "width: 150px;"

    def clean_select_field(self):
        data = self.cleaned_data["select_field"]
        if "all" in data:
            return [choice[0] for choice in self.TIME_CHOICES if choice[0] != "all"]
        return data

    def clean_select_field2(self):
        data = self.cleaned_data["select_field2"]
        if "all" in data:
            return [choice[0] for choice in self.STATE_CHOICES if choice[0] != "all"]
        return data
