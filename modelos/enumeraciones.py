from enum import Enum,auto

class NivelActividad(Enum):
    SEDENTARIO=1.2
    LIGERO=1.375
    MODERADO=1.55
    INTENSO=1.725
    def get_factor(self)->float:return self.value

class TipoComida(Enum):
    DESAYUNO=auto()
    ALMUERZO=auto()
    CENA=auto()
    REFRIGERIO=auto()


class CategoriaAlimento(Enum):
    FRUTA=auto()
    VERDURA=auto()
    CEREAL=auto()
    PROTEINA=auto()
    LACTEO=auto()
    GRASA=auto()
    BEBIDA=auto()
    OTRO=auto()

class TipoNutriente(Enum):
    #el valor es el nombre del atributo en InformacionNutricional, en el orden de su constructor
    CALORIAS="calorias"
    PROTEINAS="proteinas"
    CARBOHIDRATOS="carbohidratos"
    GRASAS="grasas"
    AZUCARES="azucares"
    FIBRA="fibra"
    SODIO="sodio_mg"

class TipoRegla(Enum):
    LIMITE_MAXIMO=auto()
    LIMITE_MINIMO=auto()
    BALANCE_CALORICO=auto()
    COMIDAS_MINIMAS=auto()
