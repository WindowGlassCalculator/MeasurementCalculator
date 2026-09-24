from django.shortcuts import render


# =====================================================
# DORI CALCULATION
# =====================================================

def decimal_to_dori(value):
    """
    Decimal calculation result -> Inch.Dori format

    8 dori = 1 inch
    """

    value = float(value)

    inch = int(value)

    # Decimal part ला 8 dori मध्ये convert
    dori = round((value - inch) * 8, 1)

    # 8 dori पूर्ण झाले तर 1 inch
    if dori >= 8:
        inch += 1
        dori -= 8

    # Half dori
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

    # 1 inch = 16 half-dori
    units = inch * 16

    # 1 dori = 2 half-dori
    units += dori * 2

    if half:
        units += 1

    return units


# =====================================================
# HALF DORI UNITS -> DORI FORMAT
# =====================================================

def units_to_dori(units):

    units = int(units)

    # 1 inch = 16 half-dori
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
    """
    Bearing Patti

    Rule:
    8 dori = 1 inch

    Example:

    45
    45 - 6 = 39
    39 / 2 = 19.5

    Example:

    27.2
    27.2 - 6 = 21.2

    21 inch = 168 dori
    + 2 dori = 170 dori

    170 / 2 = 85 dori

    85 dori = 10 inch 5 dori

    Answer = 10.5
    """

    value = str(value).strip()

    # ---------------------------------------------
    # Width मधून inch आणि dori वेगळे करणे
    # ---------------------------------------------

    if "." in value:

        inch_part, dori_part = value.split(".", 1)

    else:

        inch_part = value
        dori_part = "0"

    inch = int(inch_part)
    dori = int(dori_part)

    # ---------------------------------------------
    # Dori validation
    # ---------------------------------------------

    if dori < 0 or dori > 8:
        raise ValueError("Dori must be between 0 and 8")

    # ---------------------------------------------
    # 6 inch कमी
    # ---------------------------------------------

    inch = inch - 6

    # ---------------------------------------------
    # पूर्ण measurement Dori मध्ये
    # ---------------------------------------------

    total_dori = (inch * 8) + dori

    # ---------------------------------------------
    # 2 ने भाग
    # ---------------------------------------------

    result_dori = total_dori / 2

    # ---------------------------------------------
    # Result पुन्हा inch + dori मध्ये
    # ---------------------------------------------

    result_inch = int(result_dori // 8)

    remaining_dori = result_dori % 8

    # ---------------------------------------------
    # Half dori
    # ---------------------------------------------

    if remaining_dori == int(remaining_dori):

        return f"{result_inch}.{int(remaining_dori)}"

    else:

        whole_dori = int(remaining_dori)

        return f"{result_inch}.{whole_dori}½"


# =====================================================
# HANDLE INTERLOCK
# =====================================================

def handle_interlock(value):
    """
    Handle Interlock

    58 - 1.4 = 56.6
    48.2 - 1.4 = 46.8

    येथे .1, .2 ... हे dori आहेत.
    """

    value = str(value).strip()

    if "." in value:

        inch_part, dori_part = value.split(".", 1)

        inch = int(inch_part)
        dori = int(dori_part)

    else:

        inch = int(value)
        dori = 0

    # ---------------------------------------------
    # 1 inch 4 dori कमी
    # ---------------------------------------------

    inch = inch - 1
    dori = dori - 4

    # Dori negative असल्यास 1 inch borrow
    if dori < 0:

        inch = inch - 1
        dori = dori + 8

    return f"{inch}.{dori}"


# =====================================================
# GLASS - BEARING PATTI
# =====================================================

def glass_bearing(value):
    """
    Glass Bearing Patti

    Bearing Patti मध्ये 4 dori add.
    """

    bearing = bearing_patti(value)

    # ---------------------------------------------
    # Bearing result parse करणे
    # ---------------------------------------------

    half = "½" in bearing

    bearing = bearing.replace("½", "")

    if "." in bearing:

        inch_part, dori_part = bearing.split(".", 1)

        inch = int(inch_part)
        dori = int(dori_part)

    else:

        inch = int(bearing)
        dori = 0

    # ---------------------------------------------
    # Half dori units
    # ---------------------------------------------

    units = inch * 16

    units += dori * 2

    if half:
        units += 1

    # ---------------------------------------------
    # Glass साठी 4 dori add
    # 4 dori = 8 half-dori
    # ---------------------------------------------

    units += 8

    return units_to_dori(units)


# =====================================================
# GLASS - HANDLE INTERLOCK
# =====================================================

def glass_handle(value):

    # आधी Handle Interlock
    handle = handle_interlock(value)

    # ---------------------------------------------
    # Handle result parse
    # ---------------------------------------------

    if "." in handle:

        inch_part, dori_part = handle.split(".", 1)

        inch = int(inch_part)
        dori = int(dori_part)

    else:

        inch = int(handle)
        dori = 0

    # ---------------------------------------------
    # 3 inch कमी
    # ---------------------------------------------

    inch = inch - 3

    return f"{inch}.{dori}"


# =====================================================
# MAIN CALCULATOR
# =====================================================

def calculator(request):

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

                # -----------------------------------------
                # Bearing Patti
                # -----------------------------------------

                bearing_result = bearing_patti(width)

                # -----------------------------------------
                # Handle Interlock
                # -----------------------------------------

                handle_result = handle_interlock(height)

                # -----------------------------------------
                # Glass Bearing Patti
                # -----------------------------------------

                glass_bearing_result = glass_bearing(width)

                # -----------------------------------------
                # Glass Handle Interlock
                # -----------------------------------------

                glass_handle_result = glass_handle(height)

            except (ValueError, TypeError):

                error = "Please enter valid measurement."

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
        }
    )