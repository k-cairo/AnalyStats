from django import template

register = template.Library()


# E5
def average(value1: any, value2: any) -> float:
    # Remove % from values
    value1 = str(value1).replace("%", "")
    value2 = str(value2).replace("%", "")

    # Convert to float
    value1 = float(value1)
    value2 = float(value2)

    # Return value
    return round(((value1 + value2) / 2), 2)


# E5
def get_percentage(value1: any, value2: any) -> float:
    # Remove % from values
    value1 = str(value1).replace("%", "")
    value2 = str(value2).replace("%", "")

    # Convert to float
    value1 = float(value1)
    value2 = float(value2)

    # Return value
    return round(((value1 / value2) * 100), 2)


register.filter("average", average)
register.filter("get_percentage", get_percentage)
