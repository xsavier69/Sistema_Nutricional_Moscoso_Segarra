from datetime import date
from excepciones.dato_invalido_excepcion import DatoInvalidoExcepcion
from modelos.serializable import Serializable

class Objetivo(Serializable):
    def __init__(self,id:str="",fecha_inicio:date|None=None,fecha_fin:date|None=None):
        self._id=id
        self._fecha_inicio=fecha_inicio or date.today()
        self._fecha_fin=fecha_fin or date.today()

    def get_id(self):return self._id

    def validar_id(self,valor):return self._a_texto(valor,"id")
    def validar_fecha_inicio(self,valor):return self._a_fecha(valor,"fecha de inicio")
    def validar_fecha_fin(self,valor,fecha_inicio):
        fecha=self._a_fecha(valor,"fecha de fin")
        if fecha<fecha_inicio:raise DatoInvalidoExcepcion("fecha de fin",str(valor))
        return fecha

    def validar(self)->None:
        self.validar_id(self._id)
        self.validar_fecha_fin(self._fecha_fin,self.validar_fecha_inicio(self._fecha_inicio))

    def esta_vigente(self,fecha:date)->bool:return self._fecha_inicio<=fecha<=self._fecha_fin

    #buscar_alimento es una función id_alimento -> Alimento que entrega el controlador
    def evaluar(self,persona,desde:date,hasta:date,buscar_alimento)->bool:
        raise NotImplementedError
    def calcular_cumplimiento(self,persona,desde:date,hasta:date,buscar_alimento)->float:
        raise NotImplementedError

    def generar_mensaje(self,persona,buscar_alimento)->str:
        hasta=min(self._fecha_fin,date.today())
        porcentaje=self.calcular_cumplimiento(persona,self._fecha_inicio,hasta,buscar_alimento)
        return f"{persona.get_nombre()}: {self} | cumplimiento {porcentaje:.0f}%"

    def __str__(self):
        return f"[{self._id}] del {self._fecha_inicio} al {self._fecha_fin}"
