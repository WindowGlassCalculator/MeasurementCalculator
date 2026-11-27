
from django.shortcuts import render, redirect
from .models import CalculationHistory
from django.db.models import Q
from datetime import datetime


# =====================================================
# DORI CALCULATION
# =====================================================

def decimal_to_dori(value):
    value = float(value)
    inch = int(value)
    dori = round((value - inch) * 8, 1)

    if dori >= 8:
        inch += 1
        dori -= 8

    if dori % 1 == 0.5:
        return f"{inch}.{int(dori)}½"

    return f"{inch}.{int(dori)}"


# =====================================================
# DORI FORMAT -> HALF DORI UNITS
# =====================================================

def dori_to_units(value):
    value = str(value).strip()
    half = "½" in value
    value = value.replace("½", "")

    if "." in value:
        inch, dori = value.split(".", 1)
        inch = int(inch)
        dori = int(dori)
    else:
        inch = int(value)
        dori = 0

    units = inch * 16
    units += dori * 2

    if half:
        units += 1

    return units


# =====================================================
# HALF DORI UNITS -> DORI FORMAT
# =====================================================

def units_to_dori(units):
    units = int(units)

    inch = units // 16
    remaining = units % 16
    dori = remaining // 2
    half = remaining % 2

    if half:
        return f"{inch}.{dori}½"

    return f"{inch}.{dori}"


# =====================================================
# BEARING PATTI
# =====================================================

def bearing_patti(value):
    value = str(value).strip()

    if "." in value:
        inch_part, dori_part = value.split(".", 1)
    else:
        inch_part = value
        dori_part = "0"

    inch = int(inch_part)
    dori = int(dori_part)

    if dori < 0 or dori > 8:
        raise ValueError("Dori must be between 0 and 8")

    inch = inch - 6

    total_dori = (inch * 8) + dori
    result_dori = total_dori / 2

    result_inch = int(result_dori // 8)
    remaining_dori = result_dori % 8

    if remaining_dori == int(remaining_dori):
        return f"{result_inch}.{int(remaining_dori)}"

    whole_dori = int(remaining_dori)
    return f"{result_inch}.{whole_dori}½"


# =====================================================
# HANDLE INTERLOCK
# =====================================================

def handle_interlock(value):
    value = str(value).strip()

    if "." in value:
        inch_part, dori_part = value.split(".", 1)
        inch = int(inch_part)
        dori = int(dori_part)
    else:
        inch = int(value)
        dori = 0

    inch = inch - 1
    dori = dori - 4

    if dori < 0:
        inch = inch - 1
        dori = dori + 8

    return f"{inch}.{dori}"


# =====================================================
# GLASS - BEARING PATTI
# =====================================================

def glass_bearing(value):
    bearing = bearing_patti(value)

    half = "½" in bearing
    bearing = bearing.replace("½", "")

    if "." in bearing:
        inch_part, dori_part = bearing.split(".", 1)
        inch = int(inch_part)
        dori = int(dori_part)
    else:
        inch = int(bearing)
        dori = 0

    units = inch * 16
    units += dori * 2

    if half:
        units += 1

    units += 8

    return units_to_dori(units)


# =====================================================
# GLASS - HANDLE INTERLOCK
# =====================================================

def glass_handle(value):
    handle = handle_interlock(value)

    if "." in handle:
        inch_part, dori_part = handle.split(".", 1)
        inch = int(inch_part)
        dori = int(dori_part)
    else:
        inch = int(handle)
        dori = 0

    inch = inch - 3

    return f"{inch}.{dori}"


# =====================================================
# LANGUAGE TEXT
# =====================================================

def get_ui(request):

    language = request.session.get("language", "en")

    if language == "mr":
        return {
            "language": "mr",
            "app_name": "विंडो ग्लास कॅल्क्युलेटर",
            "subtitle": "विंडो मोजमाप कॅल्क्युलेटर",
            "measurement": "विंडोचे मोजमाप",
            "width": "रुंदी",
            "height": "उंची",
            "enter_width": "रुंदी टाका",
            "enter_height": "उंची टाका",
            "calculate": "गणना करा",
            "result": "गणनेचा निकाल",
            "bearing": "बेअरिंग पट्टी",
            "handle": "हँडल इंटरलॉक",
            "glass": "ग्लास",
            "glass_bearing": "ग्लास बेअरिंग पट्टी",
            "glass_handle": "ग्लास हँडल इंटरलॉक",
            "new_calculation": "नवीन गणना",
            "history": "गणनेचा इतिहास",
            "menu": "मेनू",
            "change_language": "भाषा बदला",
            "date": "दिनांक",
            "time": "वेळ",
            "no_history": "अजून कोणताही इतिहास उपलब्ध नाही.",
            "search_placeholder": "रुंदी, उंची किंवा तारीख शोधा...",
            "search_button": "शोधा",
            "back": "कॅल्क्युलेटरवर परत जा",
            "error": "कृपया योग्य मोजमाप टाका.",
        }

    return {
        "language": "en",
        "app_name": "Window Glass Calculator",
        "subtitle": "Window Measurement Calculator",
        "measurement": "Window Measurement",
        "width": "Width",
        "height": "Height",
        "enter_width": "Enter Width",
        "enter_height": "Enter Height",
        "calculate": "Calculate",
        "result": "Calculation Result",
        "bearing": "Bearing Patti",
        "handle": "Handle Interlock",
        "glass": "Glass",
        "glass_bearing": "Glass Bearing Patti",
        "glass_handle": "Glass Handle Interlock",
        "new_calculation": "New Calculation",
        "history": "Calculation History",
        "menu": "Menu",
        "change_language": "Change Language",
        "date": "Date",
        "time": "Time",
        "no_history": "No calculation history available.",
        "search_placeholder": "Search width, height or date...",
        "search_button": "Search",
        "back": "Back to Calculator",
        "error": "Please enter valid measurement.",
    }


# =====================================================
# LANGUAGE SELECTION
# =====================================================

def language_selection(request):
    return render(request, "language.html")


def set_language(request):

    if request.method == "POST":

        language = request.POST.get("language")

        if language in ["mr", "en"]:
            request.session["language"] = language

        return redirect("calculator")

    return redirect("language_selection")


# =====================================================
# MAIN CALCULATOR
# =====================================================

def calculator(request):

    if not request.session.get("language"):
        return redirect("language_selection")

    width = ""
    height = ""

    bearing_result = None
    handle_result = None
    glass_bearing_result = None
    glass_handle_result = None

    error = None

    if request.method == "POST":

        width = request.POST.get("width", "").strip()
        height = request.POST.get("height", "").strip()

        if width and height:

            try:
                bearing_result = bearing_patti(width)
                handle_result = handle_interlock(height)
                glass_bearing_result = glass_bearing(width)
                glass_handle_result = glass_handle(height)

                CalculationHistory.objects.create(
                    width=width,
                    height=height,
                    bearing_patti=bearing_result,
                    handle_interlock=handle_result,
                    glass_bearing_patti=glass_bearing_result,
                    glass_handle_interlock=glass_handle_result
                )

            except (ValueError, TypeError):
                error = get_ui(request)["error"]

    return render(
        request,
        "calculator.html",
        {
            "width": width,
            "height": height,
            "bearing_result": bearing_result,
            "handle_result": handle_result,
            "glass_bearing_result": glass_bearing_result,
            "glass_handle_result": glass_handle_result,
            "error": error,
            "ui": get_ui(request),
        }
    )


# =====================================================
# CALCULATION HISTORY
# =====================================================

def calculation_history(request):

    if not request.session.get("language"):
        return redirect("language_selection")

    history = CalculationHistory.objects.all()
    search_query = request.GET.get("q", "").strip()

    if search_query:

        history = history.filter(
            Q(width__icontains=search_query) |
            Q(height__icontains=search_query) |
            Q(bearing_patti__icontains=search_query) |
            Q(handle_interlock__icontains=search_query) |
            Q(glass_bearing_patti__icontains=search_query) |
            Q(glass_handle_interlock__icontains=search_query)
        )

        try:
            search_date = datetime.strptime(search_query, "%d-%m-%Y").date()
            history = CalculationHistory.objects.filter(
                created_at__date=search_date
            )
        except ValueError:
            try:
                search_date = datetime.strptime(search_query, "%Y-%m-%d").date()
                history = CalculationHistory.objects.filter(
                    created_at__date=search_date
                )
            except ValueError:
                pass

    return render(request, "history.html", {
        "history": history,
        "ui": get_ui(request),
        "search_query": search_query,
    })
