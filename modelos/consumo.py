from datetime import date
from excepciones.dato_invalido_excepcion import DatoInvalidoExcepcion
from modelos.serializable import Serializable
from modelos.enumeraciones import TipoComida
from modelos.alimento import Alimento
from modelos.informacion_nutricional import InformacionNutricional

class Consumo(Serializable):
    def __init__(self,id:str="",id_alimento:str="",fecha:date|None=None,cantidad_gramos:float=0,tipo_comida:TipoComida=TipoComida.DESAYUNO):
        self._id=id
        self._id_alimento=id_alimento
        self._fecha=fecha or date.today()
        self._cantidad_gramos=cantidad_gramos
        self._tipo_comida=tipo_comida

    def get_id(self):return self._id
    def get_id_alimento(self):return self._id_alimento
    def get_fecha(self):return self._fecha
    def get_cantidad_gramos(self):return self._cantidad_gramos
    def get_tipo_comida(self):return self._tipo_comida

    def validar_id(self,valor):return self._a_texto(valor,"id")
    def validar_id_alimento(self,valor):return self._a_texto(valor,"id de alimento")
    def validar_fecha(self,valor):
        fecha=self._a_fecha(valor,"fecha")
        if fecha>date.today():raise DatoInvalidoExcepcion("fecha",str(valor))
        return fecha
    def validar_cantidad_gramos(self,valor):return self._a_numero(valor,"cantidad en gramos",estricto=True)
    def validar_tipo_comida(self,valor):return self._a_opcion(valor,TipoComida,"tipo de comida")

    def validar(self)->None:
        self.validar_id(self._id)
        self.validar_id_alimento(self._id_alimento)
        self.validar_fecha(self._fecha)
        self.validar_cantidad_gramos(self._cantidad_gramos)
        self.validar_tipo_comida(self._tipo_comida)

    def calcular_nutrientes(self,alimento:Alimento)->InformacionNutricional:
        return alimento.calcular_nutrientes(self._cantidad_gramos)

    def __str__(self):
        return f"[{self._id}] {self._fecha} {self._tipo_comida.name}: {self._cantidad_gramos:g} g del alimento '{self._id_alimento}'"
