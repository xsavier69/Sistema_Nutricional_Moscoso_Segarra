from datetime import date
from modelos.objetivo import Objetivo
from modelos.persona import Persona

class ObjetivoPeso(Objetivo):
    def __init__(self,id:str="",fecha_inicio:date|None=None,fecha_fin:date|None=None,peso_meta_kg:float=0,tolerancia_kg:float=0):
        super().__init__(id,fecha_inicio,fecha_fin)
        self._peso_meta_kg=peso_meta_kg
        self._tolerancia_kg=tolerancia_kg

    def validar_peso_meta_kg(self,valor):return self._a_numero(valor,"peso meta",estricto=True)
    def validar_tolerancia_kg(self,valor):return self._a_numero(valor,"tolerancia")
    def validar(self)->None:
        super().validar()
        self.validar_peso_meta_kg(self._peso_meta_kg)
        self.validar_tolerancia_kg(self._tolerancia_kg)

    def _pesos(self,persona,desde,hasta):
        #pesos registrados dentro del periodo, en orden de fecha
        return [p for f,p in persona.get_historial_peso().items() if desde<=f<=hasta]

    def evaluar(self,persona:Persona,desde:date,hasta:date,buscar_alimento=None)->bool:
        pesos=self._pesos(persona,desde,hasta)
        return bool(pesos) and abs(pesos[-1]-self._peso_meta_kg)<=self._tolerancia_kg

    def calcular_cumplimiento(self,persona:Persona,desde:date,hasta:date,buscar_alimento=None)->float:
        """100 si el último peso está en la meta; si no, el avance desde el primer peso del periodo."""
        pesos=self._pesos(persona,desde,hasta)
        if not pesos:return 0.0
        if self.evaluar(persona,desde,hasta):return 100.0
        inicial=abs(pesos[0]-self._peso_meta_kg)
        return max(0.0,100*(1-abs(pesos[-1]-self._peso_meta_kg)/inicial)) if inicial else 0.0

    def __str__(self):
        return f"{super().__str__()} peso meta {self._peso_meta_kg:g} kg (±{self._tolerancia_kg:g})"
