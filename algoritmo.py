from random import seed
from random import randint
from random import random
from nodo_puntaje import Nodo_Puntaje
from nodo import Nodo
import csv
import json
import time
import os

# CONSTANTES
notasCsv = []
bitacora = {}
bitacora['registro'] = []
valMin = -2
valMax = 2 
numeroPoblacion = 10
contadorGeneracion = 0
maximoGeneraciones = 30000
criterioValMinIgual = 0.5

"""
* Funcion que  carga o crea un archivo llamado bitacora para llevar el registro de las pruebas 
"""
def inicializarBitacora():
   global bitacora 
   if os.path.isfile('bitacora.json'):
      with open('bitacora.json') as file:
         bitacora = json.load(file)

def cargarArchivo(nombreDocumentoCsv):
   with open(nombreDocumentoCsv) as csvFile:
      reader = csv.DictReader(csvFile)
      for row in reader:
         resultados = Nodo_Puntaje(float(row['PROYECTO 1']),float(row['PROYECTO 2']),float(row['PROYECTO 3']),float(row['PROYECTO 4']),float(row['NOTA FINAL']),0)
         notasCsv.append(resultados)
"""
*  INICIALIZAR POBLACION
"""
def inicializarPoblacion():
   poblacion = []
   for i in range(numeroPoblacion):
      solucion = calcularSolucion() #devuelve un arreglo de 4 elementos
      individuo = Nodo(solucion,calcularFitness(solucion))
      poblacion.append(individuo)
   return poblacion

"""
*  VERIFICAR CRITERIO
"""
def verificarCriterio(poblacion, generacion,tipoCriterio):

   if tipoCriterio == 0: #Un valor Maximo o Minimo alcanzado por una solucion de la poblacion 
      for individuo in poblacion:
         if individuo.fitness <= criterioValMinIgual: # se evalua por un minimo estipulado
            return True
   elif tipoCriterio == 1: #maximo numero de generaciones
   #Un valor maximo o minimo alcanzado por una solucion de la poblacion
      if generacion >= maximoGeneraciones:
         return True
   
   return None


"""
*SELECCIONAR PADRES
"""
def seleccionarPadres(poblacion,seleccion_padres):
   padres = []
   if seleccion_padres == 0: #SELECCION DE LOS PADRES CON MEJOR FITNESS
      #Se ordena de menor a mayor para solo agarrar la mitad de los datos
      padres_ordenados = sorted(poblacion,key=lambda item: item.fitness, reverse=False)[:len(poblacion)]
      x= (int(numeroPoblacion/2)) # la mitad de la poblacion
      for i in range(0,x):
         padres.append(padres_ordenados[i])
   return padres

"""
* EMPAREJAR
"""
def emparejar(padres):
   poblacion = padres
   # se va a utlizar una seleccion al azar 
   for i in range(0,int(numeroPoblacion/2)): #numero de hijos que se van a generar
      #numero aleatorio sobre la capacidad de los padres
      pos1 = randint(0,len(padres)-1)
      pos2= randint(0,len(padres)-1)
      hijoN = Nodo()
      hijoN.solucion = cruzar(padres[pos1].solucion,padres[pos2].solucion)
      hijoN.solucion = mutar(hijoN.solucion)
      hijoN.fitness = calcularFitness(hijoN.solucion)
      poblacion.append(hijoN)
   return poblacion

"""
* MUTAR
"""
def mutar(solucion):
   #50% de mutar  y 50% de no
   x = randint(0,1)
   if x == 1 :  #muta
      for i in range(4):
         y = randint(0,1)
         if y == 1 : #elemento del individuo muta
            value = random()
            #valor entre -2 a 2
            valor = valMin + (value * (valMax - (valMin)))
            solucion[i] = float("{0:.2f}".format(valor)) #agregando el valor a solucion y limitando a 2 decimales

   return solucion

"""
* CRUZAR
"""
def cruzar(padre1,padre2):
   hijo = []
   for i in range(4):
      value = random()
      decision = 0 +(value * (1 - 0))
      if decision <= 0.60:
         hijo.append(padre1[i])
      elif decision > 0.60:
         hijo.append(padre2[i])
   return hijo

"""
* Funcion que Retorna un arreglo de 4 con los valores del vector de -x a x
"""
def calcularSolucion():
   solucion = []
   for _ in range(4): # cuatro valores del individuo
      value = random()
      #valor entre -2 a 2
      valor = valMin + (value * (valMax - (valMin)))
      solucion.append(float("{0:.2f}".format(valor))) #agregando el valor a solucion y limitando a 2 decimales
   return solucion

"""
* Funcion que calcula el valor fitness deacuerdo a los datos de entrada del archvio csv
* solucion : es el vector de con los valores random de -x a x
"""
def calcularFitness(solucion):
   # Paso 1 : obtener el valor de la notaCalculada
   acumulador = 0
   for notas in notasCsv:
      #formula NC = W1*P1 + W2*P2 + W3*P3 + W4*P4 ; pero aca de una vez lo registramos en notas calculada de los valores  tomados del excel
      resultado = solucion[0] * notas.p1 + solucion[1] * notas.p2 + solucion[2] * notas.p3 + solucion[3] * notas.p4
      notas.nota_calculada = float("{0:.2f}".format(resultado))
      acumulador += (notas.nota_real - (notas.nota_calculada)) ** 2
   error = (1/len(notasCsv))*acumulador
   return error



"""
* Funcionalidad del programa
"""
def ejecutar():
   #BITACORA
   inicializarBitacora()
   #GENERACIONES
   generacion = 0
   #CONFIGURANDO CARGA DE ARCHIVO CSV
   nombreDocumentoCsv = "Practica1_Entrada.csv"
   #ESCOGIENDO CREITERIO DE FINALIZACION
   criterio_finalizacion = 0
   """
   * CRITERIOS DE FINALIZACION
   0  :   VALOR MINIMO ALCANZADO POR UNA SOLUCION DE LA POBLACION
   1  :  MAXIMO NUMERO DE GENERACION
   2  :  VALOR FITNESS PROMEDIO DENTRO DE LA POBLACION
   """
   #ESCOGIENDO CRITERIO DE SELECCION
   criterio_seleccion = 0
   """
   * CRITERIOS DE SELECCION
   0  : SELECCION DE LOS PADRES CON MEJOR FITNESS
   1  : SELECCION POR TORNEO
   2  : SELECCION DE PADRES EN POSICIONES PARES 
   """

   cargarArchivo(nombreDocumentoCsv)
   poblacion = inicializarPoblacion() #retorna un arreglo de n individuos
   fin = verificarCriterio(poblacion,generacion,criterio_finalizacion)
   print('*************** GENERACION ', generacion, " ***************")
   for individuo in poblacion:
      print('individuo: ', individuo.solucion,' fitness: ', individuo.fitness)
   
   while(fin == None):
      padres = seleccionarPadres(poblacion,criterio_seleccion)
      poblacion = emparejar(padres)
      generacion +=1
      fin = verificarCriterio(poblacion,generacion,criterio_finalizacion)
      
      print('*************** GENERACION ', generacion, " ***************")
      for individuo in poblacion:
         print('individuo: ', individuo.solucion,' fitness: ', individuo.fitness)
   
   mejorIndividuo = sorted(poblacion,key=lambda item: item.fitness, reverse=False)[:1] #ordeno de mayor a menor
   
   print('\n\n*************** MEJOR INDIVIDUO***************')
   print('Individuo: ', mejorIndividuo[0].solucion, ' Fitness: ', mejorIndividuo[0].fitness)
   #registrando en la bitacora
   
   if criterio_finalizacion == 0:
      criterio_finalizacion = 'VALOR MINIMO ALCANZADO POR UNA SOLUCION DE LA POBLACION CON UN VALOR DE : ' + str(criterioValMinIgual) 
   elif criterio_finalizacion == 1:
      criterio_finalizacion = 'MAXIMO NUMERO DE GENERACION'
   
   if criterio_seleccion == 0:
      criterio_seleccion = 'SELECCION DE LOS PADRES CON MEJOR FITNESS'

   bitacora['registro'].append({
      'fecha_hora': time.strftime("%c"),
      'doc': nombreDocumentoCsv,
      'criterio_finalizacion': criterio_finalizacion,
      'criterio_seleccion': criterio_seleccion,
      'generaciones_generadas': generacion,
      'mejor_solucion': mejorIndividuo[0].solucion,
      'fitness': mejorIndividuo[0].fitness
   })
   with open('bitacora.json','w') as file:
      json.dump(bitacora,file,indent=4)

def ejecutar2():
   # with open('bitacora.json') as file:
   #    bitacora = json.load(file)
   inicializarBitacora()
   for info in bitacora['registro']:
      print('fecha: ',info['fecha_hora'])
ejecutar()


