
#This is my custom trig calculator using taylor series.
#IMPORTANT: MAKE SURE terms = 50. Only change this value if you know what you are doing!
#IMPORTANT: Remember to round outputs of functions to 5DP to get accurate values!
#EXAMPLE CORRECT USAGE: e.g sin_X = round(sin_Deg(angle, 50), 5)
#Code owner KallaxenC

def radians(value):
    PI = 3.141592653589793238462643383279
    radians = value / 360 * (2*PI)
    return  radians

def sin_Deg(value, terms):
    value = radians(value)
    result = 0
    for i in range(terms):
        sign = (-1)**i
        power = 1 + (2*i)
        if i == 0:
            factorial = 1
        else:
            factorial = factorial * (2*i) * (2*i+1)
        result = result + ((sign*(value**power)) / factorial)
        if len(str(result)) > 15:
            result = round(result, 15)
    return(result)

def cos_Deg(value, terms):
    value = radians(value)
    result = 0

    for i in range(terms):
        sign = (-1)**i
        power = (2*i)
        if i == 0:
            factorial = 1
        else:
            factorial = factorial * (2*i-1) * (2*i)

        result = result + ((sign*(value**power)) / factorial)
        if len(str(result)) > 15:
            result = round(result, 15)
    return(result)

def sin_Rad(value, terms):
    result = 0
    for i in range(terms):
        sign = (-1)**i
        power = 1 + (2*i)
        if i == 0:
            factorial = 1
        else:
            factorial = factorial * (2*i) * (2*i+1)
        result = result + ((sign*(value**power)) / factorial)
        if len(str(result)) > 15:
            result = round(result, 15)
    return(result)

def cos_Rad(value, terms):
    result = 0

    for i in range(terms):
        sign = (-1)**i
        power = (2*i)
        if i == 0:
            factorial = 1
        else:
            factorial = factorial * (2*i-1) * (2*i)

        result = result + ((sign*(value**power)) / factorial)
        if len(str(result)) > 15:
            result = round(result, 15)
    return(result)

#We can just use tan(x) = sin(x) / cos(x) which is nice
def tan_Deg(value, terms):
    value = radians(value)
    try:
        result = sin_Rad(value, terms) / cos_Rad(value, terms)
    except ZeroDivisionError:
        return "error"
    
    return result

def tan_Rad(value, terms):
    try:
        result = sin_Rad(value, terms) / cos_Rad(value, terms)
    except ZeroDivisionError:
        return "error"
    
    return result

