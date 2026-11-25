from excepciones.dato_invalido_excepcion import DatoInvalidoExcepcion
from modelos.alimento import Alimento
from modelos.enumeraciones import CategoriaAlimento
from modelos.informacion_nutricional import InformacionNutricional

class Receta(Alimento):
    def __init__(self,id:str="",nombre:str="",categoria:CategoriaAlimento=CategoriaAlimento.OTRO):
        super().__init__(id,nombre,categoria)
        self._ingredientes={}   #id_alimento -> gramos
        self._aportes={}        #id_alimento -> nutrientes que aporta

    def get_ingredientes(self):return dict(self._ingredientes)
    def validar_gramos(self,valor):return self._a_numero(valor,"gramos",estricto=True)

    def agregar_ingrediente(self,alimento:Alimento,gramos:float)->None:
        gramos=self.validar_gramos(gramos)
        clave=alimento.get_id()
        if clave==self._id:raise DatoInvalidoExcepcion("ingrediente",clave)

        aporte=alimento.calcular_nutrientes(gramos)
        self._ingredientes[clave]=self._ingredientes.get(clave,0)+gramos
        self._aportes[clave]=self._aportes.get(clave,InformacionNutricional()).sumar(aporte)

    def calcular_peso_total(self)->float:return sum(self._ingredientes.values())

    def get_info_por_100g(self)->InformacionNutricional:
        total=InformacionNutricional()
        for aporte in self._aportes.values():total=total.sumar(aporte)
        peso=self.calcular_peso_total()
        return total.escalar(100/peso) if peso else total

    def validar(self)->None:
        self.validar_id(self._id)
        self.validar_nombre(self._nombre)
        self.validar_categoria(self._categoria)
        if not self._ingredientes:raise DatoInvalidoExcepcion("ingredientes","sin ingredientes")

    def __str__(self):
        detalle=", ".join(f"{i}: {g:g} g" for i,g in self._ingredientes.items())
        return f"{super().__str__()}\n    Receta de {self.calcular_peso_total():g} g -> {detalle}"
