from datetime import datetime

class SistemaExcepcion(Exception):
    def __init__(self,mensaje:str=""):
        super().__init__(mensaje)
        self._mensaje=mensaje
        self._fecha_hora=datetime.now()

    def get_mensaje_usuario(self)->str:return self._mensaje
