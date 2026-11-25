from excepciones.sistema_excepcion import SistemaExcepcion

class PersistenciaExcepcion(SistemaExcepcion):

    def __init__(self,ruta_archivo:str,detalle:str=""):
        super().__init__(detalle)
        self._ruta_archivo=ruta_archivo
    def get_mensaje_usuario(self)->str:
        return f"Error de archivo en '{self._ruta_archivo}': {self._mensaje}"
