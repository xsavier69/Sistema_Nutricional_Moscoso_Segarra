from datetime import date
from modelos.serializable import Serializable

class Alerta(Serializable):
    def __init__(self,fecha:date,mensaje:str,nivel_severidad:int,origen:str):
        self._fecha=fecha
        self._mensaje=mensaje
        self._nivel_severidad=nivel_severidad
        self._origen=origen

    def __str__(self):
        return f"{self._fecha} [severidad {self._nivel_severidad}] {self._origen}: {self._mensaje}"
