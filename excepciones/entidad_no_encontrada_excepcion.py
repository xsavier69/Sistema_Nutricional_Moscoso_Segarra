from excepciones.sistema_excepcion import SistemaExcepcion


class EntidadNoEncontradaExcepcion(SistemaExcepcion):
    def __init__(self,tipo_entidad:str,id:str):
        super().__init__()
        self._tipo_entidad=tipo_entidad
        self._id=id

    def get_mensaje_usuario(self)->str:
        return f"No se encontró {self._tipo_entidad} con id '{self._id}'"
