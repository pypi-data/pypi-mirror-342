#для работы с собственным свечением атмосферы. возможно, сюда можно досыпать поправку на радиопоток
import numpy as np
import matplotlib.pyplot as plt

from .solar_radio_flux import fluxdate
from .solar_radio_flux import fluxtime
from .solar_radio_flux import fluxobsflux

from .airglow_spectrum import wavelenght_kp, intensity_kp
from .modtran_default_kp_transparency import wavelenght_modtran_kp, trancparency_modtran_kp

#следующая функция для поправки на радиопоток, пока не используется
def radioflux(date, time): #date -- в формате строки 'дд.мм.гггг', time -- в формате строки 'чч:мм:сс'
    day, month, year = date.split('.')
    date = year + month + day
    hours, minutes, seconds = time.split(':')
    time = hours + minutes + seconds
    data_times = fluxtime[np.where(fluxdate==date)[0]]
    box = []
    for i in range(data_times.shape[0]):
        box.append(abs(int(data_times[i]) - int(time)))
    box = np.array(box)
    return float(fluxobsflux[np.argmin(box)])


def airglow_spectrum(wavelenght_airglow = wavelenght_kp, intensity_airglow = intensity_kp, wavelenght_atmosphere = wavelenght_modtran_kp, transparency_atmosphere = trancparency_modtran_kp):
    wavelenght = []
    intensity = []
    for i in range(wavelenght_airglow.shape[0]):
        for j in range(wavelenght_atmosphere.shape[0]):
            if wavelenght_airglow[i] == wavelenght_atmosphere[j]:
                wavelenght.append(wavelenght_airglow[i])
                intensity.append(intensity_airglow[i] / transparency_atmosphere[j])
    return(np.array(wavelenght), np.array(intensity) * 10**10 / (4 * np.pi)) #возвращает длину волны в нм и поток в фот / (сек м^2 ср нм)
#функция написана для спектра взятого от китт пик, прозрачность атмосферы взята из модтрана, параметры -- см. доклад, там прямо скрин. Прозрачность взята для 45 градусов, пересчитана в 30 градусов

from .solar_radio_flux import fluxdate


