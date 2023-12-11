import io
import os

import matplotlib.pyplot as plt
import pandas as pd
import requests
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from .forms import PageReviewForm, HealthDataForm, IndexDataForm
from .models import Pages, PageReview


def index(request):
    custom_order = [4, 2, 3, 7, 6, 5, 1]
    paginator = Paginator(Pages.objects.filter(pk__in=custom_order).order_by("pk"), 3)
    page_number = request.GET.get("page")
    pages = paginator.get_page(page_number)

    for page in pages:
        count = PageReview.objects.filter(title_id=page.pk).count()
        setattr(page, "review_count", count)
    reviews = PageReview.objects.all().order_by("-data_created")

    return render(request, "index.html", {"pages": pages, "reviews": reviews})


def add_review(request, pk):
    page = get_object_or_404(Pages, pk=pk)

    if request.method == "POST":
        form = PageReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.title = page
            review.save()
            return redirect("single_page_view", pk=pk)  # redict to page by pk
    else:
        form = PageReviewForm()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def single_page_view(request, pk):
    page = Pages.objects.get(pk=pk)
    pages = Pages.objects.all()
    content_paragraphs = page.content.split("<p>")
    text_paragraphs = page.text.split("<p>")
    review_form = PageReviewForm()
    page_reviews = page.pagereview_set.filter(title_id=page.pk)

    return render(
        request,
        "single-page.html",
        {
            "review_form": review_form,
            "page": page,
            "content_paragraphs": content_paragraphs,
            "text_paragraphs": text_paragraphs,
            "pages": pages,
            "page_reviews": page_reviews,
        },
    )


class SinglePageView(FormMixin, generic.DetailView):
    model = Pages
    template_name = "single_page.html"
    form_class = PageReviewForm

    def get_success_url(self):
        return reverse("single_page_view", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = self.get_form()
        context["reviews"] = PageReview.objects.filter(title=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review = form.save(commit=False)
            review.title = self.object
            review.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def health_data_form(request):
    if request.method == "POST":
        form = HealthDataForm(request.POST)
        if form.is_valid():
            # we will create a csv file from the provided data and prepare it for the user to download
            data = generate_csv_data(form.cleaned_data)
            response = HttpResponse(data, content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="health_data.csv"'
            return response
    else:
        form = HealthDataForm()

    return render(request, "health_form_template.html", {"form": form})


def generate_csv_data(form_data):
    base_url = "https://ec.europa.eu/eurostat/api/dissemination"
    service = "statistics"
    version = "1.0"
    response_type = "data"
    dataset_code = "hlth_hlye"
    format_type = "format=JSON"
    lang = "lang=EN"

    # Add info to filters
    filters = f"time={form_data['select_field3']}&unit=YR&sex=T&lang=en"

    for el in form_data["select_field"]:
        filters += f"&geo={el}"
    for el in form_data["select_field2"]:
        filters += f"&indic_he={el}"

    # Create JSON url adress
    url = f"{base_url}/{service}/{version}/{response_type}/{dataset_code}?{format_type}&{filters}"
    response = requests.get(url)

    # get info from JSON
    if response.status_code == 200:
        data = response.json()
        values = data["value"]
        countries = data["dimension"]["geo"]["category"]["label"]
        health_indicator = data["dimension"]["indic_he"]["category"]["label"]

        # create DataFrame
        column_name = list(countries)
        row_name = list(health_indicator)
        df = pd.DataFrame(index=row_name, columns=column_name)

        for i, row in enumerate(row_name):
            for j, col in enumerate(column_name):
                x = str(i * len(column_name) + j)
                if x in list(values):
                    df.at[row, col] = values[x]
                else:
                    df.at[row, col] = "None"

        df = df.transpose()
        csv_output = io.StringIO()

        # write to csv file
        df.to_csv(csv_output)

        return csv_output.getvalue()

    return "An error occurred while fetching the data. Please try again later or contact support."


def index_data_form(request):
    if request.method == "POST":
        # we call the form
        form = IndexDataForm(request.POST)
        if form.is_valid():
            # we will create a csv file from the provided data and prepare it for the user to download
            data = generate_index_data(form.cleaned_data)
            response = HttpResponse(data, content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="index_data.csv"'
            # return render(request, 'index_form_template.html', {'form': form})
            return index_data_results(request)
        else:
            pass
    else:
        form = IndexDataForm()

    return render(request, "index_form_template.html", {"form": form})


def generate_index_data(form_data):
    base_url = "https://ec.europa.eu/eurostat/api/dissemination"
    service = "statistics"
    version = "1.0"
    response_type = "data"
    dataset_code = "hlth_hlye"
    format_type = "format=JSON"
    lang = "lang=EN"

    # Add info to filters
    REPORT_CHOICES = ("HLY_0", "LE_0", "HLY_50", "LE_50", "HLY_65", "LE_65")
    new_df = pd.DataFrame(
        index=form_data["select_field2"], columns=form_data["select_field"]
    )
    for el in form_data["select_field"]:
        filters = ""
        filters += f"time={el}&"
        filters = filters + "unit=YR&sex=T&lang=en"
        for el1 in form_data["select_field2"]:
            filters += f"&geo={el1}"
        for el2 in REPORT_CHOICES:
            filters += f"&indic_he={el2}"

        # Create JSON url adress
        url = f"{base_url}/{service}/{version}/{response_type}/{dataset_code}?{format_type}&{filters}"
        response = requests.get(url)

        # get info from JSON
        if response.status_code == 200:
            data = response.json()
            values = data["value"]
            countries = data["dimension"]["geo"]["category"]["label"]
            health_indicator = data["dimension"]["indic_he"]["category"]["label"]

            # create DataFrame
            column_name = list(countries)
            row_name = list(health_indicator)
            df = pd.DataFrame(index=row_name, columns=column_name)

        for i, row in enumerate(row_name):
            for j, col in enumerate(column_name):
                x = str(i * len(column_name) + j)
                if x in list(values):
                    df.at[row, col] = values[x]
                else:
                    df.at[row, col] = "None"

        df = df.transpose()

        # Calculate index for each country
        for country in df.index:
            HLY_0 = df.at[country, "HLY_0"]
            LE_0 = df.at[country, "LE_0"]
            HLY_50 = df.at[country, "HLY_50"]
            LE_50 = df.at[country, "LE_50"]
            HLY_65 = df.at[country, "HLY_65"]
            LE_65 = df.at[country, "LE_65"]

            # Check if any value is 'None' (string) or actual None, if so, set the index as None
            if any(
                v == "None" or v is None
                for v in [HLY_0, LE_0, HLY_50, LE_50, HLY_65, LE_65]
            ):
                new_df.at[country, el] = None
            else:
                try:
                    HLY_0_LE_0 = float(HLY_0) / float(LE_0)
                    HLY_50_LE_50 = float(HLY_50) / float(LE_50)
                    HLY_65_LE_65 = float(HLY_65) / float(LE_65)
                    index_value = round(
                        ((HLY_0_LE_0 + HLY_50_LE_50 + HLY_65_LE_65) / 3), 2
                    )
                    new_df.at[country, el] = index_value
                except ValueError:
                    new_df.at[
                        country, el
                    ] = None  # If conversion to float fails, set index as None

    index_csv = os.path.join(settings.MEDIA_ROOT, "index.csv")
    new_df.to_csv(index_csv, index=True)


def index_data_results(request):
    index_csv = os.path.join(settings.MEDIA_ROOT, "index.csv")
    df1 = pd.read_csv(index_csv)
    df_html = df1.to_html(classes="table table-striped", index=True)
    # Calculating our averages
    df = df1.drop(columns=df1.columns[0], axis=1, inplace=False)
    print(df)
    df["Average"] = df.mean(axis=1)
    # make column with index names ant values:
    df["Plot"] = df1.iloc[:, 0].astype(str)
    print(df["Plot"])
    # great plot
    plt.figure(figsize=(8, 6))
    plt.bar(df.index, df["Average"])
    for i, value in enumerate(df["Average"]):
        plt.text(i, value + 0.05, f"{value:.2f}", ha="center")
    plt.xlabel("Index")
    plt.ylabel("Average")
    plt.xticks(df1.index, df["Plot"], rotation=90)
    plt.tight_layout()
    # Save the plot
    plot_file_path = os.path.join(
        settings.BASE_DIR, "media", "media", "img", "plot.png"
    )
    plot_file_url = os.path.join(settings.MEDIA_ROOT, "img", "plot.png")

    plt.savefig(plot_file_path)

    return render(
        request,
        "index_form_results.html",
        {"form": df_html, "plot_file": plot_file_url},
    )
