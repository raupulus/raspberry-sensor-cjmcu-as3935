#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# @author     Raúl Caro Pastorino
# @email      dev@fryntiz.es
# @web        https://fryntiz.es
# @gitlab     https://gitlab.com/fryntiz
# @github     https://github.com/fryntiz
# @twitter    https://twitter.com/fryntiz
# @telegram   https://t.me/fryntiz

# Create Date: 2020
# Project Name:
# Description:
#
# Dependencies:
#
# Revision 0.01 - File Created
# Additional Comments:

# @copyright  Copyright © 2020 Raúl Caro Pastorino
# @license    https://wwww.gnu.org/licenses/gpl.txt

# Copyright (C) 2020  Raúl Caro Pastorino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Guía de estilos aplicada: PEP8

# #           Descripción           # #
# Modelo que implementa las clases básicas para el detector de rayo CJMCU-3935
# usando el chip AS3935 por i2c en raspberry


from RPi_AS3935 import RPi_AS3935
import datetime
import time
from AbstractModel import AbstractModel

class CJMCU_3935(AbstractModel):
    table_name = 'table_lightning'
    sensor = None

    def __init__(self, address=0x03, bus=1, mode_debug=False, indoor=True,
                 pin=25):
        self.sensor = RPi_AS3935(address, bus)
        self.mode_debug = mode_debug

        self.sensor.set_indoors(indoor)
        self.sensor.set_noise_floor(0)
        self.sensor.calibrate(tun_cap=0x0F)

        self.pin = pin

        ## Inicio Callback para en cada detección registrar rayo
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self.handle_interrupt)

        print("Waiting for lightning - or at least something that looks like it")

    def handle_interrupt(self, channel):
        """
        Función que se ejecuta cuando detecta un rayo para registrarlo
        en el array de objetos con los datos registrados.
        :return:
        """
        time.sleep(0.003)
        sensor = self.sensor

        reason = sensor.get_interrupt()
        if reason == 0x01:
            print ("Noise level too high - adjusting")
            sensor.raise_noise_floor()
        elif reason == 0x04:
            print ("Disturber detected - masking")
            sensor.set_mask_disturber(True)
        elif reason == 0x08:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            distance = sensor.get_distance()
            print("We sensed lightning!")
            print("It was " + str(distance) + "km away. (%s)" % now)
            print("")

    def get_all_datas(self):
        """
        Devuelve un diccionario con todas las lecturas si se han podido tomar.
        :return:
        """
        if self.???:
            return {
                "x": self.read_x(),
            }

        return None

    def tablemodel(self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
        return {
            'strike': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'distance': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'type': {
                'type': 'Numeric',
                'params': {
                    'precision': 15,
                    'asdecimal': True,
                    'scale': 4
                },
                'others': None,
            },
            'energy': {
                'type': 'Numeric',
                'params': {
                    'precision': 22,
                    'asdecimal': True,
                    'scale': 11
                },
                'others': None,
            },
            'created_at': {
                'type': 'DateTime',
                'params': None,
                'others': {
                    'default': datetime.datetime.utcnow
                },
            },
        }

    def debug(self):
        """
        Función para depurar funcionamiento del modelo proyectando datos por
        consola.
        """
        datas = self.get_all_datas()

        if datas:
            print('Pintando debug para CJMCU 3935')

            for sensor, data in datas.items():
                print('Valor del sensor ' + str(sensor) + ': ' + str(data))