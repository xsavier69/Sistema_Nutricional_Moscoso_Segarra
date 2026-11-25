from datetime import date
from excepciones.dato_invalido_excepcion import DatoInvalidoExcepcion
from modelos.serializable import Serializable
from modelos.enumeraciones import TipoNutriente,TipoRegla
from modelos.alerta import Alerta
from modelos.persona import Persona

class ReglaAlerta(Serializable):
    SEVERIDAD_MINIMA=1
    SEVERIDAD_MAXIMA=5

    def __init__(self,nombre:str="",tipo:TipoRegla=TipoRegla.LIMITE_MAXIMO,nutriente:TipoNutriente|None=None,limite:float=0,nivel_severidad:int=1):
        self._nombre=nombre
        self._tipo=tipo
        self._nutriente=nutriente
        self._limite=limite
        self._nivel_severidad=nivel_severidad

    def get_nombre(self):return self._nombre

    def validar_nombre(self,valor):return self._a_texto(valor,"nombre")
    def validar_tipo(self,valor):return self._a_opcion(valor,TipoRegla,"tipo de regla")
    def validar_nutriente(self,valor):return self._a_opcion(valor,TipoNutriente,"nutriente")
    def validar_limite(self,valor):return self._a_numero(valor,"límite")
    def validar_nivel_severidad(self,valor):
        texto=str(valor).strip()
        validos={str(n) for n in range(self.SEVERIDAD_MINIMA,self.SEVERIDAD_MAXIMA+1)}
        if texto not in validos:raise DatoInvalidoExcepcion("nivel de severidad",texto)
        return int(texto)

    def usa_nutriente(self,tipo:TipoRegla)->bool:
        return tipo in (TipoRegla.LIMITE_MAXIMO,TipoRegla.LIMITE_MINIMO)

    def validar(self)->None:
        self.validar_nombre(self._nombre)
        if self.usa_nutriente(self.validar_tipo(self._tipo)):self.validar_nutriente(self._nutriente)
        self.validar_limite(self._limite)
        self.validar_nivel_severidad(self._nivel_severidad)

    def evaluar(self,persona:Persona,fecha:date,buscar_alimento)->Alerta|None:
        """Devuelve la alerta generada, o None si la regla se cumple ese día."""
        mensaje=None
        match self._tipo:
            case TipoRegla.LIMITE_MAXIMO|TipoRegla.LIMITE_MINIMO:
                valor=persona.calcular_totales_dia(fecha,buscar_alimento).obtener(self._nutriente)
                maximo=self._tipo==TipoRegla.LIMITE_MAXIMO
                if (valor>self._limite if maximo else valor<self._limite):
                    mensaje=f"{self._nutriente.name} {valor:.1f} {'supera el máximo' if maximo else 'no llega al mínimo'} de {self._limite:g}"
            case TipoRegla.BALANCE_CALORICO:
                balance=persona.calcular_totales_dia(fecha,buscar_alimento).obtener(TipoNutriente.CALORIAS)-persona.calcular_requerimiento_calorico()
                if abs(balance)>self._limite:
                    mensaje=f"balance calórico de {balance:+.0f} kcal fuera del margen de {self._limite:g}"
            case TipoRegla.COMIDAS_MINIMAS:
                comidas=persona.contar_comidas(fecha)
                if comidas<self._limite:mensaje=f"{comidas} comidas, menos del mínimo de {self._limite:g}"
        return Alerta(fecha,mensaje,self._nivel_severidad,self._nombre) if mensaje else None

    def __str__(self):
        nutriente=f" {self._nutriente.name}" if self._nutriente else ""
        return f"{self._nombre}: {self._tipo.name}{nutriente} límite {self._limite:g} (severidad {self._nivel_severidad})"
