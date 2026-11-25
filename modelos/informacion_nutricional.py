from modelos.serializable import Serializable
from modelos.enumeraciones import TipoNutriente

class InformacionNutricional(Serializable):
    def __init__(self,calorias:float=0,proteinas:float=0,carbohidratos:float=0,grasas:float=0,azucares:float=0,fibra:float=0,sodio_mg:float=0):
        self._calorias=calorias
        self._proteinas=proteinas
        self._carbohidratos=carbohidratos
        self._grasas=grasas
        self._azucares=azucares
        self._fibra=fibra
        self._sodio_mg=sodio_mg

    def validar_calorias(self,valor):return self._a_numero(valor,"calorías")
    def validar_proteinas(self,valor):return self._a_numero(valor,"proteínas")
    def validar_carbohidratos(self,valor):return self._a_numero(valor,"carbohidratos")
    def validar_grasas(self,valor):return self._a_numero(valor,"grasas")
    def validar_azucares(self,valor):return self._a_numero(valor,"azúcares")
    def validar_fibra(self,valor):return self._a_numero(valor,"fibra")
    def validar_sodio_mg(self,valor):return self._a_numero(valor,"sodio")

    def obtener(self,nutriente:TipoNutriente)->float:return getattr(self,"_"+nutriente.value)

    def sumar(self,otra:InformacionNutricional)->InformacionNutricional:
        return InformacionNutricional(*(self.obtener(n)+otra.obtener(n) for n in TipoNutriente))
    def escalar(self,factor:float)->InformacionNutricional:
        return InformacionNutricional(*(self.obtener(n)*factor for n in TipoNutriente))

    def __str__(self):
        return (f"{self._calorias:.1f} kcal | proteínas {self._proteinas:.1f} g | carbohidratos {self._carbohidratos:.1f} g | "
                f"grasas {self._grasas:.1f} g | azúcares {self._azucares:.1f} g | fibra {self._fibra:.1f} g | sodio {self._sodio_mg:.1f} mg")
