from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from math import log


class dos_rayos(APIView):

    def get(self, request, format=None):
        potencia_tx = int(request.query_params['potencia_tx'])
        ganancia_tx = int(request.query_params['ganancia_tx'])
        altura_antena_tx = int(request.query_params['altura_antena_tx'])
        ganancia_rx = int(request.query_params['ganancia_rx'])
        altura_antena_rx = int(request.query_params['altura_antena_rx'])
        distancia = int(request.query_params['distancia'])
        base_logaritmica = int(request.query_params['base_logaritmica'])

        potencia_recibida = (potencia_tx * ganancia_rx * ganancia_tx * (altura_antena_tx ** 2) * (altura_antena_rx ** 2)) / (distancia ** 4)
        propagacion_perdida = 40 * log(distancia, base_logaritmica) - (10 * log(ganancia_tx, base_logaritmica) + 10 * log(ganancia_rx, base_logaritmica) + 20 * log(altura_antena_tx, base_logaritmica) + 20 * log(altura_antena_rx, base_logaritmica))
        respuesta = {
            'potencia_recibida_W': potencia_recibida,
            'propagacion_perdida_DB': propagacion_perdida
        }

        return Response(respuesta)

class okumura(APIView):

    def get(self, request, format=None):
        atenuacion_esplibre = int(request.query_params['atenuacion_esplibre'])
        atenuacion_relpromedio = int(request.query_params['atenuacion_relpromedio'])
        altura_antena_tx = int(request.query_params['altura_antena_tx'])
        ganancia_tx = int(request.query_params['ganancia_tx'])
        ganancia_rx = int(request.query_params['ganancia_rx'])
        ganancia_de_ambiente = int(request.query_params['ganancia_de_ambiente'])
        frecuencia = int(request.query_params['frecuencia'])
        base_logaritmica = int(request.query_params['base_logaritmica'])

        if frecuencia >= 150 and frecuencia <= 1920:
            if ganancia_tx > 30 and ganancia_tx < 1000 :
                altura_antena_rx = 20 * log((ganancia_tx / 200), base_logaritmica)
            elif ganancia_rx < 3:
                altura_antena_rx = 10 * log((ganancia_tx / 3), base_logaritmica)
            elif ganancia_rx > 3 and ganancia_rx < 10:
                altura_antena_rx = 20 * log((ganancia_tx / 3), base_logaritmica)
            propagacion_perdida = atenuacion_esplibre + atenuacion_relpromedio - altura_antena_tx - altura_antena_rx - ganancia_de_ambiente
            print(f'Propagacion perdida segun el modelo Okumura en DB: {propagacion_perdida}')
            respuesta = {
                'propagacion_perdida': propagacion_perdida
            }

            return Response(respuesta)
        else:
            respuesta = {
                'error': 'Frecuencia invalida, tiene que ser una frecuencia entre 150 y 1920 Mhz.'
            }
            return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)


class okumura_hata(APIView):

    def get(self, request, format=None):
        atenuacion_esplibre = int(request.query_params['atenuacion_esplibre'])
        factor_correccion = int(request.query_params['factor_correccion'])
        atenuacion_relpromedio = int(request.query_params['atenuacion_relpromedio'])
        altura_antena_tx = int(request.query_params['altura_antena_tx'])
        altura_antena_rx = int(request.query_params['altura_antena_rx'])
        ganancia_tx = int(request.query_params['ganancia_tx'])
        ganancia_rx = int(request.query_params['ganancia_rx'])
        frecuencia = int(request.query_params['frecuencia'])
        base_logaritmica = int(request.query_params['base_logaritmica'])
        distancia = int(request.query_params['distancia'])

        if frecuencia > 150 and frecuencia < 1500:
            if altura_antena_tx > 1 and altura_antena_tx < 10:
                if altura_antena_rx > 30 and altura_antena_rx < 200:
                    perdida_urbana = 69.55 + 26.16 * log(frecuencia, base_logaritmica) - 13.82 * log(ganancia_tx, base_logaritmica) - factor_correccion + ((44.9 - 6.55 * log(distancia, base_logaritmica)) * 2.8)
                else:
                    respuesta = {
                        'error': 'La antena transmisora no esta en rango, tiene que ser una altura entre 30 y 200 metros.'
                    }
                    return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)
            else:
                respuesta = {
                        'error': 'La antena receptora no esta en rango, tiene que ser una altura entre 1 y 10 metros.'
                    }
                return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)
        else:
            respuesta = {
                'error': 'Frecuencia invalida, tiene que ser una frecuencia entre 150 y 1920 Mhz.'
            }
            return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

        factor_correccion_CG = (8.29 * log(1.54 * ganancia_rx, base_logaritmica) ** 2) - 1.1
        factor_correccion_CCM = (1.1 * log(frecuencia, base_logaritmica) - 0.7) - (1.56 * log(frecuencia, base_logaritmica) - 0.8)
        factor_correccion_R = perdida_urbana - (4.78 * log(frecuencia, base_logaritmica) ** 2) + (18.33 * log(frecuencia, base_logaritmica)) - 40.94
        if frecuencia < 300:
            factor_correccion_SU = 'Para este tipo de opcion la frecuancia debe de ser menos de 300 Mhz.'
        else:
            factor_correccion_SU = perdida_urbana - (2 * log(frecuencia / 28, base_logaritmica) ** 2) - 5.4

        print(f'Urban loss (Okumura-Hata model): {perdida_urbana}')
        respuesta = {
            'perdida_urbana': perdida_urbana,
            'factor_correccion_CG': factor_correccion_CG,
            'factor_correccion_CCM': factor_correccion_CCM,
            'factor_correccion_R': factor_correccion_R,
            'factor_correccion_SU': factor_correccion_SU,

        }

        return Response(respuesta)
