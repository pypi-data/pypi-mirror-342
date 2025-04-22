def celsius_ke_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_ke_celsius(f):
    return (f - 32) * 5/9

def celsius_ke_kelvin(c):
    return c + 273.15

def kelvin_ke_celsius(k):
    return k - 273.15

def fahrenheit_ke_kelvin(f):
    return celsius_ke_kelvin(fahrenheit_ke_celsius(f))

def kelvin_ke_fahrenheit(k):
    return celsius_ke_fahrenheit(kelvin_ke_celsius(k))
