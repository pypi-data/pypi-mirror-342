from astropy.coordinates import get_body, Galactic
from astropy.time import Time
import ephem
import numpy as np

from .zodiac import convolution, integral
from .albedo_of_planets import venus_alb_wl, venus_alb_rf, mars_alb_wl, mars_alb_rf, jupiter_alb_wl, jupiter_alb_rf, saturn_alb_wl, saturn_alb_rf
from .solar_spectrum import wavelenght_newguey2003, flux_newguey2003
from .band_V_data import wavelenght_band_V, trancparency_band_V


def coordinates_of_planet(body, date, time): #'mars', 'venus', 'saturn', 'jupyter'; 2023-11-03; 12:00:00; return galactic coordinates of planet
    datetime = date + ' ' + time
    time = Time(datetime)
    planet = get_body(body, time, ephemeris='builtin').transform_to(Galactic)
    l = planet.l.value
    b = planet.b.value
    return(l, b)

    
def magnitude_of_planet(body, date, time): #'mars', 'venus', 'saturn', 'jupiter'; 2023-11-03; 12:00:00';
    if body == 'venus':
        planet = ephem.Venus()
    elif body == 'mars':
        planet = ephem.Mars()
    elif body == 'jupiter':
        planet = ephem.Jupiter()
    elif body == 'saturn':
        planet = ephem.Saturn()
        
    # Устанавливаем дату наблюдения
    date = date.replace('-', '/')

    planet.compute(date)
    return planet.mag

def mag_to_phot(mag): #в полосе V
    F0 = 10**6
    F1 = F0 * 10 ** (- 0.4 * mag) # фот / (см^2 сек)
    F1 = F1 * 10**4 #/ (4 * np.pi) # фот / (м^2 сек ср) -- НАДО ЛИ ДЕЛИТЬ НА 4 ПИ?
    return F1


def venus_spectrum(date, time, Sun_sp_wl = wavelenght_newguey2003, Sun_sp_fx = flux_newguey2003, albedo_wl = venus_alb_wl, albedo_rf = venus_alb_rf, V_wl = wavelenght_band_V, V_tr = trancparency_band_V):
    body = 'venus'
    planet_wl, planet_sp = convolution(albedo_wl, albedo_rf, Sun_sp_wl, Sun_sp_fx) #вот тут получили спектр планеты
    planet_V_wl, planet_V_sp = convolution(planet_wl, planet_sp, V_wl, V_tr) #свернули с полосой V, фот / (сек ср м^2 нм)

    norm = integral(planet_V_wl, planet_V_sp) # фот / (сек ср м^2)
    
    #делаем так, чтобы эта норма была равна F1
    mag = magnitude_of_planet(body, date, time)
    F1 = mag_to_phot(mag)
    A = F1 / norm
    planet_sp = A * planet_sp
    
    #########################################################################
#     planet_V_wl, planet_V_sp = convolution(planet_wl, planet_sp, V_wl, V_tr)
#     integr = integral(planet_V_wl, planet_V_sp)
#     print('Техническая проверка на совпадение двух чисел:', integr, F1)
    #########################################################################
    
    return planet_wl, planet_sp

def mars_spectrum(date, time, Sun_sp_wl = wavelenght_newguey2003, Sun_sp_fx = flux_newguey2003, albedo_wl = mars_alb_wl, albedo_rf = mars_alb_rf, V_wl = wavelenght_band_V, V_tr = trancparency_band_V):
    body = 'mars'
    planet_wl, planet_sp = convolution(albedo_wl, albedo_rf, Sun_sp_wl, Sun_sp_fx) #вот тут получили спектр планеты
    planet_V_wl, planet_V_sp = convolution(planet_wl, planet_sp, V_wl, V_tr) #свернули с полосой V, фот / (сек ср м^2 нм)

    norm = integral(planet_V_wl, planet_V_sp) # фот / (сек ср м^2)
    
    #делаем так, чтобы эта норма была равна F1
    mag = magnitude_of_planet(body, date, time)
    F1 = mag_to_phot(mag)
    A = F1 / norm
    planet_sp = A * planet_sp
    
    #########################################################################
#     planet_V_wl, planet_V_sp = convolution(planet_wl, planet_sp, V_wl, V_tr)
#     integr = integral(planet_V_wl, planet_V_sp)
#     print('Техническая проверка на совпадение двух чисел:', integr, F1)
    #########################################################################
    
    return planet_wl, planet_sp

def jupiter_spectrum(date, time, Sun_sp_wl = wavelenght_newguey2003, Sun_sp_fx = flux_newguey2003, albedo_wl = jupiter_alb_wl, albedo_rf = jupiter_alb_rf, V_wl = wavelenght_band_V, V_tr = trancparency_band_V):
    body = 'jupiter'
    planet_wl, planet_sp = convolution(albedo_wl, albedo_rf, Sun_sp_wl, Sun_sp_fx) #вот тут получили спектр планеты
    planet_V_wl, planet_V_sp = convolution(planet_wl, planet_sp, V_wl, V_tr) #свернули с полосой V, фот / (сек ср м^2 нм)

    norm = integral(planet_V_wl, planet_V_sp) # фот / (сек ср м^2)
    
    #делаем так, чтобы эта норма была равна F1
    mag = magnitude_of_planet(body, date, time)
    F1 = mag_to_phot(mag)
    A = F1 / norm
    planet_sp = A * planet_sp
    
    #########################################################################
#     planet_V_wl, planet_V_sp = convolution(planet_wl, planet_sp, V_wl, V_tr)
#     integr = integral(planet_V_wl, planet_V_sp)
#     print('Техническая проверка на совпадение двух чисел:', integr, F1)
    #########################################################################
    
    return planet_wl, planet_sp

def saturn_spectrum(date, time, Sun_sp_wl = wavelenght_newguey2003, Sun_sp_fx = flux_newguey2003, albedo_wl = saturn_alb_wl, albedo_rf = saturn_alb_rf, V_wl = wavelenght_band_V, V_tr = trancparency_band_V):
    body = 'saturn'
    planet_wl, planet_sp = convolution(albedo_wl, albedo_rf, Sun_sp_wl, Sun_sp_fx) #вот тут получили спектр планеты
    planet_V_wl, planet_V_sp = convolution(planet_wl, planet_sp, V_wl, V_tr) #свернули с полосой V, фот / (сек ср м^2 нм)

    norm = integral(planet_V_wl, planet_V_sp) # фот / (сек ср м^2)
    
    #делаем так, чтобы эта норма была равна F1
    mag = magnitude_of_planet(body, date, time)
    F1 = mag_to_phot(mag)
    A = F1 / norm
    planet_sp = A * planet_sp
    
    #########################################################################
#     planet_V_wl, planet_V_sp = convolution(planet_wl, planet_sp, V_wl, V_tr)
#     integr = integral(planet_V_wl, planet_V_sp)
#     print('Техническая проверка на совпадение двух чисел:', integr, F1)
    #########################################################################
    
    return planet_wl, planet_sp
    
# Внутри основной функции: если планета попадает в поле зрения (через coordinates_of_planet(.....)),
# ищем ее спектр venus_spectrum(.....)
    
    