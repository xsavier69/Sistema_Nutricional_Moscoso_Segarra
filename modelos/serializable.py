import math
from datetime import date
from excepciones.dato_invalido_excepcion import DatoInvalidoExcepcion

class Serializable:
    """Interfaz de las entidades persistentes; reúne la conversión de datos de entrada."""

    def _a_texto(self,valor,campo):
        texto=str(valor or "").strip()
        if not texto:raise DatoInvalidoExcepcion(campo,texto)
        return texto

    def _a_numero(self,valor,campo,minimo=0,estricto=False):
        try:numero=float(str(valor).strip().replace(",","."))
        except ValueError:raise DatoInvalidoExcepcion(campo,str(valor)) from None

        if not math.isfinite(numero) or numero<minimo or (estricto and numero==minimo):
            raise DatoInvalidoExcepcion(campo,str(valor))
        return numero
    def _a_fecha(self,valor,campo):
        if isinstance(valor,date):return valor
        try:return date.fromisoformat(str(valor).strip())
        except ValueError:raise DatoInvalidoExcepcion(campo,str(valor)) from None

    def _a_opcion(self,valor,enumeracion,campo):
        #acepta el miembro, su nombre o su número de menú (desde 1)
        if isinstance(valor,enumeracion):return valor
        texto=str(valor).strip().upper()
        for numero,miembro in enumerate(enumeracion,1):
            if texto in (miembro.name,str(numero)):return miembro
        raise DatoInvalidoExcepcion(campo,str(valor))
