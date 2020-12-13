from random import seed
from random import randint
from random import random
from nodo_puntaje import Nodo_Puntaje
from nodo import Nodo
import csv

# CONSTANTES
notasCsv = []
valMin = -2
valMax = 2 
numeroPoblacion = 10
contadorGeneracion = 0
maximoGeneraciones = 30000
criterioValMinIgual = 0.5

def cargarArchivo():
   with open('Practica1_Entrada.csv') as csvFile:
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
   #Un valor maximo o minimo alcanzado por una solucion de la poblacion
   if generacion >= maximoGeneraciones:
      return True
   #se va a evaluar por por un fitnes a criterio personal
   for individuo in poblacion:
      if individuo.fitness <= criterioValMinIgual:
         return True
   return None


"""
*SELECCIONAR PADRES
"""
def seleccionarPadres(poblacion):
   padres = []
   #Selección de los padres con mejor valor fitness
   
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
   generacion = 0
   cargarArchivo()
   poblacion = inicializarPoblacion() #retorna un arreglo de n individuos
   fin = verificarCriterio(poblacion,generacion,0)
   print('*************** GENERACION ', generacion, " ***************")
   for individuo in poblacion:
      print('individuo: ', individuo.solucion,' fitness: ', individuo.fitness)
   # padres = seleccionarPadres(poblacion)
   # print('tamanio: ',len(padres))
   # for nodo in padres:
   #    print('fitness:',nodo.fitness,'solucion:',nodo.solucion)
   
   while(fin == None):
      padres = seleccionarPadres(poblacion)
      poblacion = emparejar(padres)
      generacion +=1
      fin = verificarCriterio(poblacion,generacion,0)
      
      print('*************** GENERACION ', generacion, " ***************")
      for individuo in poblacion:
         print('individuo: ', individuo.solucion,' fitness: ', individuo.fitness)
   
   mejorIndividuo = sorted(poblacion,key=lambda item: item.fitness, reverse=False)[:1] #ordeno de mayor a menor
   
   print('\n\n*************** MEJOR INDIVIDUO***************')
   print('Individuo: ', mejorIndividuo[0].solucion, ' Fitness: ', mejorIndividuo[0].fitness)
   # sol = calcularSolucion()
   # for solucion in sol:
   #    print(solucion)

ejecutar()
