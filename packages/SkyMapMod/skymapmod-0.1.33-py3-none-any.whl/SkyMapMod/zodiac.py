import numpy as np
import matplotlib.pyplot as plt
import random

#коэффициент пересчета из единиц S10 в количество фотонов от Солнца
#вычислен на основе спектра АЧТ от звезды класса A0, солнечного спектра и факта, что 1 ед. S10 соответствует 100 фотонов от звезды класса A0


#переопределяю тригонометрические функции, чтобы работать с градусами
def cos(x):
    return np.cos(x * np.pi / 180)

def sin(x):
    return np.sin(x * np.pi / 180)

def tan(x):
    return np.tan(x * np.pi / 180)

def acos(x):
    return np.arccos(x) * 180 / np.pi

def asin(x):
    return np.arcsin(x) * 180 / np.pi

def atan(x):
    return np.arctan(x) * 180 / np.pi

#переопределяю прочие функции для красоты записи
def exp(x):
    return np.exp(x)

def sqrt(x):
    return np.sqrt(x)

#функция Хевисайда (в контексте статьи определяется именно так)
def u(x):
    if x <= 0:
        return 0
    elif x > 0:
        return 1
    
#функции для перехода из одной СК в другую
#сферические в декартовы
def spheral_to_decart(r, lmbd, beta):
    x = r * cos(lmbd) * cos(beta)
    y = r * sin(lmbd) * cos(beta)
    z = r * sin(beta)
    return (x, y, z)

#декартовы в сферические
def decart_to_spheral(x, y, z):
    r = sqrt(x**2 + y**2 + z**2)
    lmbd = atan(y/(x + 1e-30))
    beta = asin(z/r)
    return(r, lmbd, beta)

#функция для поворота эклиптических координат
def rotate_ekl(lmbd, beta, lmbd0, beta0):
    x, y, z = spheral_to_decart(1, lmbd-lmbd0, beta)
    x1 = x * cos(beta0) + z * sin(beta0) 
    z1 = - x * sin(beta0) + z * cos(beta0)
    y1 = y
    r, lmbd2, beta2 = decart_to_spheral(x1, y1, z1)
    return(lmbd2, beta2)

#Далее идут функции, которые входят в общую формулу для расчета зод. света
#Компонента S
def S(lmbd, beta, lmbd_sun, Omega):
    c = cos(lmbd - lmbd_sun) * cos(beta)
    eps = acos(c)
    first = 6 * abs(sin(lmbd_sun - Omega))
    second = ((1-u(eps-90)) * (sin(eps) + 1e-30)**(-2.3) + u(eps - 90) * sin(eps))
    #third = (1 - u(Omega - lmbd_sun) / 4 + 2 * (1-u(eps-90)) * c)
    third = (1 - (1-u(lmbd_sun - Omega))/4 + 2*(1-u(eps-90)) * c)
    #equap = ((u(Omega - lmbd_sun) - u(lmbd_sun - Omega)) * beta + 5) / 10
    equap = ((1 - u(lmbd_sun - Omega) - u(lmbd_sun - Omega)) * beta + 5) / 10
    fourth = max(0, min(equap, 1))
    S = first * second * third * fourth
    return S

#Компонента D -- "эмпирический вклад в форме гантели"
def D(lmbd, beta, lmbd_sun):
    
    d = abs(lmbd - lmbd_sun) / 6.5 - abs(beta) + 15 + 5 * u(beta)
    eps = acos(cos(lmbd - lmbd_sun) * cos(beta))
    if beta > 0:
        lmbd1, beta1 = rotate_ekl(lmbd, beta, lmbd_sun, 21)
    elif beta <= 0:
        lmbd1, beta1 = rotate_ekl(lmbd, beta, lmbd_sun, -15)
    gamma1 = atan(sin(lmbd1)/( 1e-30 + tan(beta1)))
    eps1 = acos(cos(lmbd1) * cos(beta1))
    h = gamma1 * (1 - u(beta)) + (gamma1) * u(beta)  
    A = (1 + 0.5 * (1 - u(beta))) * (1-u(eps-90)) * ((1-u(eps-75)) + u(eps - 75) * exp(-(eps - 75)**2 / 120))
#     f = 60 * exp(- eps1 / 16) * (0.15 + 0.85 * exp(-6 * cos(0.6 * h)**4))
    f = 60 * exp(- eps1 / 16) * (0.85 + 0.15 * exp(-6 * cos(0.6 * h)**4))
    g = 25 * exp(- acos(cos(2 * lmbd1) * cos(0.7 * beta1)) / 10)
    D = A * ((f * np.exp(-d / 10) + g * np.exp(-d / 8)) * u(d) + (f + g) * (1 - u(d)))
    return D

#Компонента E -- остаточная, не учитывалась
def E(lmbd, beta):
    return 0

#Компонента F -- остаточная, не учитывалась
def F(lmbd, beta, lmbd_sun):
    return 0

#Компонента G -- антисолнечная точка
def G(lmbd, beta, lmbd_sun):
    lmbd_tild = lmbd - lmbd_sun - 180
    if lmbd_tild > 180:
        lmbd_tild = lmbd_tild - 360
    elif lmbd_tild < -180:
        lmbd_tild = lmbd_tild + 360        
    eps_tild = 180 - acos(cos(lmbd_tild + 180) * cos(beta))    
    G_b         = 7.5 * exp(-eps_tild / 4) + 39.5 * exp(-eps_tild / 25)
    G_lmbd_tild = 7.5 * exp(-eps_tild / 4) + 39.5 * exp(-eps_tild / 35)  
    first = 1 - 0.02 * beta * lmbd_tild**2 / (eps_tild**3 + 1e-300)
    second = (beta**2 * G_b + lmbd_tild**2 * G_lmbd_tild) / (eps_tild**2 + 1e-300)
    third = (1 - u(eps_tild - 60) * (1 - exp(-(eps_tild - 60)**2 / 300)))
    G = first * second * third
    return G

#Общая формула для зод. света
def zodiacal_light(lmbd, beta, lmbd_sun):
    b = 1.5 * (sqrt(1 + (beta / 1.5)**2) - 1)
    c = cos(lmbd - lmbd_sun) * cos(beta)
    eps = acos(c)
    eps_tild = 180 - eps
    lmbd_tild = lmbd - lmbd_sun - 180
    abs_gm = abs(atan(sin(lmbd - lmbd_sun) / (tan(beta) + 1e-30)))
    Omega = 78.25
    first = 7 + 8 * (1 - cos(b)) + 6 * exp(- beta**2 / 512)
    second_1 = (1-u(eps-90)) * (65 + 120 * c - 185 * c**2 + 65 * c**3) * (sin(eps) + 1e-30)**(-2.3)
    second_2 = u(eps - 90) * (65 + 120 * c + 154 * c**2 + 88 * c**3)
    second_mult = 10 ** (- sin(b) / (0.009 * (eps + 40)))  
    third = (1-u(eps-90)) * (30 * ((sin(eps) + 1e-30)**(-2.3) - 1) * cos(b))
    fourth = (8800 * exp((1 - sqrt(1 + ((abs_gm - 90)/3)**2))/10) - 1200) * exp(-eps/10)
    zod = first  + (second_1 + second_2) * second_mult + third + fourth + S(lmbd, beta, lmbd_sun, Omega) + D(lmbd, beta, lmbd_sun) + E(lmbd, beta) + F(lmbd, beta, lmbd_sun) + G(lmbd, beta, lmbd_sun)
    return zod/0.415 #деление на 0.415 осуществляет переход из ед. ADU в ед. S10

##Пересчет S10 в количество фотонов от Солнца

#Импортирую нужные спектры
from .solar_spectrum import wavelenght_newguey2003, flux_newguey2003
from .band_V_data import wavelenght_band_V, trancparency_band_V

#Функция для спектра АЧТ, по которому расчитаем спектр от звезды класса A0
#на вход -- массив длин волн и температура. На выходе -- массив значений в Вт/(м^2   м)
def black_body(lmbd, T):
    h = 6.63e-34 #Дж * сек
    c = 3e8 # м / сек
    k = 1.38e-23 # Дж / К
    lmbd = lmbd * 1e-9 # м
    u = 2 * h * c**2 / (lmbd**5) / (np.exp(h * c / (lmbd) / k / T) - 1)
    return u 

#спектр АЧТ в фотонах
def black_body_phot(lmbd, T):
    h = 6.63e-34 #Дж * сек
    c = 3e8 # м / сек
    k = 1.38e-23 # Дж / К
    lmbd = lmbd * 1e-9 # м
    u = 2 * c / (lmbd**4) / (np.exp(h * c / (lmbd) / k / T) - 1)
    return u #уже в фотонах/сек (поделено на hc/lambda)

#универсальная функция для свертки двух спектров
def convolution(array_1, meaning_1, array_2, meaning_2):
    array = []
    meaning = []
    for i in range(array_1.shape[0]):
        for j in range(array_2.shape[0]):
            if array_1[i] == array_2[j]:
                array.append(array_1[i])
                meaning.append(meaning_1[i] * meaning_2[j])
    return np.array(array), np.array(meaning)

def integral(wl, spec):
    shape = wl.shape[0]
    result = 0
    for i in range(shape - 1):
        result += (spec[i] + spec[i+1]) / 2 * (wl[i+1] - wl[i])
    return result

def zodiacal_spectrum(lmbd, beta, lmbd_sun, Sun_sp_wl = wavelenght_newguey2003, Sun_sp_fx = flux_newguey2003, V_wl = wavelenght_band_V, V_tr = trancparency_band_V):
    #коэффициент пересчета из единиц S10 в количество фотонов от Солнца
    #вычислен на основе спектра АЧТ от звезды класса A0, солнечного спектра и факта, что 1 ед. S10 соответствует 100 фотонов от звезды класса A0
    #вот столько фотонов/(см^2 сек) от Солнца несет 1 ед S10:
    N_S10 = 100.6 
    N_S10 = N_S10 * 10**4 / (4 * np.pi) # фот / (м^2 сек ср) -- НАДО ЛИ ДЕЛИТЬ НА 4 ПИ?
    S10 = zodiacal_light(lmbd, beta, lmbd_sun) 
    Sun_V_wl, Sun_V_sp = convolution(Sun_sp_wl, Sun_sp_fx, V_wl, V_tr) #свертка Солнечного спектра с полосой V
    integr = integral(Sun_V_wl, Sun_V_sp)
    A = S10 * N_S10 / integr
    
    
    #############################################
    a, b = convolution(Sun_sp_wl, A * Sun_sp_fx, V_wl, V_tr)
    c = integr = integral(a, b)
    print('Техническая проверка: S10*N_S10 =', S10 * N_S10)
    print('А при нормировке и интекрированию получается:', c)
    #############################################
    
    return Sun_sp_wl, A * Sun_sp_fx #нм, фот / (м^2 сек нм ср)
    
    
