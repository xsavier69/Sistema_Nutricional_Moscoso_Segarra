from datetime import date
from excepciones.dato_invalido_excepcion import DatoInvalidoExcepcion
from modelos.serializable import Serializable
from modelos.enumeraciones import NivelActividad
from modelos.informacion_nutricional import InformacionNutricional
from modelos.alerta import Alerta
from modelos.consumo import Consumo
from modelos.objetivo import Objetivo

class Persona(Serializable):
    def __init__(self,id:str="",nombre:str="",fecha_nacimiento:date|None=None,sexo:str="M",altura_cm:float=0,peso_actual_kg:float=0,nivel_actividad:NivelActividad=NivelActividad.SEDENTARIO):
        self._id=id
        self._nombre=nombre
        self._fecha_nacimiento=fecha_nacimiento or date.today()
        self._sexo=sexo
        self._altura_cm=altura_cm
        self._peso_actual_kg=peso_actual_kg
        self._nivel_actividad=nivel_actividad
        #el peso inicial queda registrado para que un peso antiguo no reemplace al actual
        self._historial_peso={date.today():peso_actual_kg} if peso_actual_kg else {}
        self._consumos=[]
        self._objetivos=[]
        self._alertas=[]

    def get_id(self):return self._id
    def get_nombre(self):return self._nombre
    def get_peso_actual_kg(self):return self._peso_actual_kg
    def get_historial_peso(self):return dict(sorted(self._historial_peso.items()))
    def get_objetivos(self):return list(self._objetivos)

    def validar_id(self,valor):return self._a_texto(valor,"id")
    def validar_nombre(self,valor):return self._a_texto(valor,"nombre")
    def validar_fecha_nacimiento(self,valor):return self._no_futura(valor,"fecha de nacimiento")
    def validar_fecha_peso(self,valor):return self._no_futura(valor,"fecha del peso")
    def validar_sexo(self,valor):
        sexo=str(valor).strip().upper()
        if sexo not in ("M","F"):raise DatoInvalidoExcepcion("sexo",str(valor))
        return sexo
    def validar_altura_cm(self,valor):return self._a_numero(valor,"altura en cm",estricto=True)
    def validar_peso_actual_kg(self,valor):return self._a_numero(valor,"peso en kg",estricto=True)
    def validar_nivel_actividad(self,valor):return self._a_opcion(valor,NivelActividad,"nivel de actividad")

    def _no_futura(self,valor,campo):
        fecha=self._a_fecha(valor,campo)
        if fecha>date.today():raise DatoInvalidoExcepcion(campo,str(valor))
        return fecha

    def validar(self)->None:
        self.validar_id(self._id)
        self.validar_nombre(self._nombre)
        self.validar_fecha_nacimiento(self._fecha_nacimiento)
        self.validar_sexo(self._sexo)
        self.validar_altura_cm(self._altura_cm)
        self.validar_peso_actual_kg(self._peso_actual_kg)
        self.validar_nivel_actividad(self._nivel_actividad)

    def calcular_edad(self)->int:
        hoy,nac=date.today(),self._fecha_nacimiento
        return hoy.year-nac.year-((hoy.month,hoy.day)<(nac.month,nac.day))

    def calcular_imc(self)->float:return self._peso_actual_kg/(self._altura_cm/100)**2

    def calcular_tmb(self)->float:  #Mifflin-St Jeor
        base=10*self._peso_actual_kg+6.25*self._altura_cm-5*self.calcular_edad()
        return base+(5 if self._sexo=="M" else -161)

    def calcular_requerimiento_calorico(self)->float:
        return self.calcular_tmb()*self._nivel_actividad.get_factor()

    def registrar_peso(self,fecha:date,peso_kg:float)->None:
        fecha=self.validar_fecha_peso(fecha)
        self._historial_peso[fecha]=self.validar_peso_actual_kg(peso_kg)
        self._peso_actual_kg=self._historial_peso[max(self._historial_peso)]

    def conservar_registros(self,anterior:Persona)->None:
        """Al modificar una persona, traspasa lo registrado en la versión anterior."""
        self._historial_peso=dict(anterior._historial_peso)
        if self._peso_actual_kg!=anterior._peso_actual_kg:
            self._historial_peso[date.today()]=self._peso_actual_kg
        self._consumos=anterior._consumos
        self._objetivos=anterior._objetivos
        self._alertas=anterior._alertas

    def agregar_consumo(self,consumo:Consumo)->None:self._consumos.append(consumo)
    def eliminar_consumo(self,id_consumo:str)->None:
        self._consumos=[c for c in self._consumos if c.get_id()!=id_consumo]

    def obtener_consumos(self,desde:date,hasta:date)->list[Consumo]:
        return sorted((c for c in self._consumos if desde<=c.get_fecha()<=hasta),key=lambda c:c.get_fecha())

    def calcular_totales_dia(self,fecha:date,buscar_alimento)->InformacionNutricional:
        total=InformacionNutricional()
        for c in self.obtener_consumos(fecha,fecha):
            total=total.sumar(c.calcular_nutrientes(buscar_alimento(c.get_id_alimento())))
        return total

    def contar_comidas(self,fecha:date)->int:
        return len({c.get_tipo_comida() for c in self.obtener_consumos(fecha,fecha)})

    def agregar_objetivo(self,objetivo:Objetivo)->None:self._objetivos.append(objetivo)
    def eliminar_objetivo(self,id_objetivo:str)->None:
        self._objetivos=[o for o in self._objetivos if o.get_id()!=id_objetivo]
    def obtener_objetivos_activos(self)->list[Objetivo]:
        return [o for o in self._objetivos if o.esta_vigente(date.today())]

    def agregar_alerta(self,alerta:Alerta)->None:
        #detectar dos veces la misma situación no duplica la alerta
        if str(alerta) not in map(str,self._alertas):self._alertas.append(alerta)

    def __str__(self):
        return (f"[{self._id}] {self._nombre} ({self._sexo}, {self.calcular_edad()} años) {self._altura_cm:g} cm, {self._peso_actual_kg:g} kg, "
                f"{self._nivel_actividad.name} | IMC {self.calcular_imc():.1f} | TMB {self.calcular_tmb():.0f} kcal | "
                f"requerimiento {self.calcular_requerimiento_calorico():.0f} kcal")
