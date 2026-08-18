from django.shortcuts import render


# =====================================================
# DORI CALCULATION
# =====================================================

def decimal_to_dori(value):
    """
    Decimal calculation result -> Inch.Dori format

    Example:
    23.75 -> 23.7½
    24.35 -> 24.3½
    25.3  -> 25.3
    """

    value = float(value)

    inch = int(value)

    # Decimal part ला dori मध्ये convert
    dori = round((value - inch) * 10, 1)

    # 8 dori = 1 inch
    if dori >= 8:
        inch += 1
        dori -= 8

    # Half dori
    if dori % 1 == 0.5:
        whole_dori = int(dori)

        if whole_dori == 7:
            return f"{inch}.7½"

        return f"{inch}.{whole_dori}½"

    return f"{inch}.{int(dori)}"


# =====================================================
# DORI FORMAT -> HALF DORI UNITS
# =====================================================

def dori_to_units(value):
    """
    Example:

    23.7½ -> units
    25.3  -> units
    """

    value = str(value).strip()

    half = "½" in value

    value = value.replace("½", "")

    if "." in value:

        inch, dori = value.split(".")

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

    # 8 dori = 1 inch = 16 half-dori

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

    value = float(value)

    # 6 inch वजा
    result = value - 6

    # 2 ने भाग
    result = result / 2

    return decimal_to_dori(result)


# =====================================================
# HANDLE INTERLOCK
# =====================================================

def handle_interlock(value):

    value = float(value)

    # 1.4 वजा
    result = value - 1.4

    return f"{result:.1f}"


# =====================================================
# GLASS - BEARING PATTI
# =====================================================

def glass_bearing(value):

    # आधी Bearing Patti
    bearing = bearing_patti(value)

    # Bearing Patti ला units मध्ये convert
    units = dori_to_units(bearing)

    # 4 dori = 8 half-dori
    units += 8

    # पुन्हा Dori format
    return units_to_dori(units)


# =====================================================
# GLASS - HANDLE INTERLOCK
# =====================================================

def glass_handle(value):

    # Handle Interlock
    handle = handle_interlock(value)

    result = float(handle)

    # 3 inch वजा
    result -= 3

    return f"{result:.1f}"


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

    if request.method == "POST":

        width = request.POST.get("width", "").strip()
        height = request.POST.get("height", "").strip()

        if width and height:

            # Bearing Patti
            bearing_result = bearing_patti(width)

            # Handle Interlock
            handle_result = handle_interlock(height)

            # Glass
            glass_bearing_result = glass_bearing(width)

            glass_handle_result = glass_handle(height)

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
        }
    )