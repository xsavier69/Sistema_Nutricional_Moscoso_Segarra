import csv
import os
from excepciones.dato_invalido_excepcion import DatoInvalidoExcepcion
from excepciones.persistencia_excepcion import PersistenciaExcepcion

class Reporte:
    def __init__(self,titulo:str,encabezados:list[str]):
        self._titulo=titulo
        self._encabezados=list(encabezados)
        self._filas=[]

    def agregar_fila(self,valores:list[str])->None:
        if len(valores)!=len(self._encabezados):raise DatoInvalidoExcepcion("fila",str(valores))
        self._filas.append([str(v) for v in valores])

    def exportar_csv(self,ruta:str)->None:
        try:
            os.makedirs(os.path.dirname(ruta) or ".",exist_ok=True)
            with open(ruta,"w",newline="",encoding="utf-8-sig") as archivo:
                csv.writer(archivo).writerows([self._encabezados,*self._filas])
        except OSError as e:
            raise PersistenciaExcepcion(ruta,str(e)) from e

    def __str__(self):
        tabla=[self._encabezados,*self._filas]
        anchos=[max(map(len,columna)) for columna in zip(*tabla)]
        lineas=[" | ".join(v.ljust(a) for v,a in zip(fila,anchos)) for fila in tabla]
        if not self._filas:lineas.append("(sin datos)")
        return "\n".join([self._titulo,*lineas])
