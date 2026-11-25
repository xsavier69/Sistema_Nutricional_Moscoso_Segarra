from datetime import date
from excepciones.dato_invalido_excepcion import DatoInvalidoExcepcion
from modelos.objetivo import Objetivo
from modelos.enumeraciones import TipoNutriente
from modelos.persona import Persona

class ObjetivoNutricional(Objetivo):
    def __init__(self,id:str="",fecha_inicio:date|None=None,fecha_fin:date|None=None,nutriente:TipoNutriente=TipoNutriente.CALORIAS,valor_minimo:float=0,valor_maximo:float=0):
        super().__init__(id,fecha_inicio,fecha_fin)
        self._nutriente=nutriente
        self._valor_minimo=valor_minimo
        self._valor_maximo=valor_maximo

    def validar_nutriente(self,valor):return self._a_opcion(valor,TipoNutriente,"nutriente")
    def validar_valor_minimo(self,valor):return self._a_numero(valor,"valor mínimo")
    def validar_valor_maximo(self,valor,valor_minimo):
        return self._a_numero(valor,"valor máximo",minimo=valor_minimo)

    def validar(self)->None:
        super().validar()
        self.validar_nutriente(self._nutriente)
        self.validar_valor_maximo(self._valor_maximo,self.validar_valor_minimo(self._valor_minimo))

    def calcular_cumplimiento(self,persona:Persona,desde:date,hasta:date,buscar_alimento)->float:
        """Porcentaje de días con consumos, dentro del objetivo, que quedan en el rango."""
        dias={c.get_fecha() for c in persona.obtener_consumos(max(desde,self._fecha_inicio),min(hasta,self._fecha_fin))}
        if not dias:return 0.0
        cumplidos=sum(self._valor_minimo<=persona.calcular_totales_dia(d,buscar_alimento).obtener(self._nutriente)<=self._valor_maximo for d in dias)
        return 100*cumplidos/len(dias)

    def evaluar(self,persona:Persona,desde:date,hasta:date,buscar_alimento)->bool:
        return self.calcular_cumplimiento(persona,desde,hasta,buscar_alimento)==100

    def __str__(self):
        return f"{super().__str__()} {self._nutriente.name} diario entre {self._valor_minimo:g} y {self._valor_maximo:g}"
