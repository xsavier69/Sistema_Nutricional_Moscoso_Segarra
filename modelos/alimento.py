from modelos.serializable import Serializable
from modelos.enumeraciones import CategoriaAlimento,TipoNutriente
from modelos.informacion_nutricional import InformacionNutricional

class Alimento(Serializable):

    def __init__(self,id:str="",nombre:str="",categoria:CategoriaAlimento=CategoriaAlimento.OTRO,info:InformacionNutricional|None=None):
        self._id=id
        self._nombre=nombre
        self._categoria=categoria
        self._info=info or InformacionNutricional()

    def get_id(self):return self._id
    def get_nombre(self):return self._nombre
    def get_categoria(self):return self._categoria

    def validar_id(self,valor):return self._a_texto(valor,"id")
    def validar_nombre(self,valor):return self._a_texto(valor,"nombre")
    def validar_categoria(self,valor):return self._a_opcion(valor,CategoriaAlimento,"categoría")

    def validar(self)->None:
        self.validar_id(self._id)
        self.validar_nombre(self._nombre)
        self.validar_categoria(self._categoria)
        for n in TipoNutriente:
            getattr(self._info,"validar_"+n.value)(self._info.obtener(n))

    def get_info_por_100g(self)->InformacionNutricional:return self._info
    def calcular_nutrientes(self,gramos:float)->InformacionNutricional:
        return self.get_info_por_100g().escalar(gramos/100)

    def __str__(self):
        return f"[{self._id}] {self._nombre} ({self._categoria.name}) por 100 g: {self.get_info_por_100g()}"
