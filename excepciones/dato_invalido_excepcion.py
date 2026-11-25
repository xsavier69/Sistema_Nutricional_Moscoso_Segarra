from excepciones.sistema_excepcion import SistemaExcepcion

class DatoInvalidoExcepcion(SistemaExcepcion):
    def __init__(self,campo:str,valor_recibido:str):
        super().__init__()
        self._campo=campo
        self._valor_recibido=valor_recibido
    def get_mensaje_usuario(self)->str:
        return f"Dato inválido en {self._campo}: '{self._valor_recibido}'"
