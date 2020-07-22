from automata.fa.dfa import DFA   #Libreria Automata
from automata.fa.nfa import NFA
import graphviz as gv

# Todos los parámetros son listas o tuplas
# donde:
#  * alfabeto:  es el alfabeto aceptado por el 
#               autómata.
#  * estados:   es una lista de estados aceptados
#               por el autómata.
#  * inicio:    Son los estados de inicio del fsm.
#  * trans:     Es una tupla de funciones de transición
#               con tres elementos que son: (a,b,c) donde
#               (a,b) son los estados de partida y llegada;
#               mientras que c es la letra que acepta.
#  * final      Son los estados finales del autómata.

# https://github.com/caleb531/automata

def AFNDtoAFD (automata, tipo):
  if tipo:
    dfa = DFA.from_nfa(automata) 
    minimal_dfa = dfa.minify()
    return minimal_dfa, False
  else: 
    return automata, tipo  

def AFDtoAFND (automata, tipo):
  if tipo==False:
    nfa = NFA.from_dfa(automata) 
    return nfa, True
  else: 
    return automata, tipo 
    

def union (automata1, tipo1, automata2, tipo2):
  # Crear un estado inicial y juntar 2 automatas
  simbolos = []
  for i in automata1.input_symbols:
    simbolos.append(i)
  for a in automata2.input_symbols:
    simbolos.append(a)
  simbolos.append('')
  
  estados = []
  for i in automata1.states:
    estados.append(i)
  for a in automata2.states:
    estados.append(a)
  estados.append('inicio')

  final = []
  for i in automata1.final_states:
    final.append(i)
  for a in automata2.final_states:
    final.append(a)

  dic1 = automata1.transitions.copy()
  dic2 = automata2.transitions.copy()
  dic1.update(dic2)

  if tipo1 == tipo2: # acepta 2 afnd 
    if tipo1:
      dic1['inicio'] = {'': {automata1.initial_state, automata2.initial_state}}

      automata = NFA(
        states=set(estados),
        input_symbols= set(simbolos),
        transitions=dic1,
        initial_state='inicio',
        final_states= set(final)
        )
      return automata, tipo1
# Formato dfa:  'q0': {'0': 'q0', '1': 'q1'},
# Formato nfa:  'q1': {'0': {'q1'}, '1': {'q2'}},
    else:
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      return union (automata1, tipo1, automata2, tipo2)

  else:
    if tipo1:
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      return union (automata1, tipo1, automata2, tipo2)
      
    if tipo2:
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      return union (automata1, tipo1, automata2, tipo2)

def complemento (automata, tipo):  
  #intercambiar estados finales por estados
  if tipo == False :
    
    fin = []
    final= automata.final_states
    estados = automata.states

    for i in estados:
      for l in final:
        if i != l:
          fin.append(i)
    
    finales = set(fin)

    automata = DFA(
      states=automata.states,
      input_symbols=automata.input_symbols,
      transitions=automata.transitions,
      initial_state=automata.initial_state,
      final_states= finales
    )
    return automata , tipo
  
  else: 
    ADF = NFA.from_dfa(automata)
    complemento(ADF,False)

def concatenacion(automata1, tipo1, automata2, tipo2):  # entran 2 NFA y no se saca la chucha :)

  simbolos = []
  #Saca Los simbolos de el automata 1 y 2
  for i in automata1.input_symbols:
    simbolos.append(i)
  for a in automata2.input_symbols:
    simbolos.append(a)
  simbolos.append('')
  sim = set(simbolos)

  estados = []
  #Saca los estados de los automatas 1 y 2
  for i in automata1.states:
    estados.append(i)
  for a in automata2.states:
    estados.append(a)
  esta2=set(estados)

  dic1 = automata1.transitions.copy()
  dic2 = automata2.transitions.copy()
  dic1.update(dic2)

  if tipo1 == tipo2:
    if tipo1:
      dic1[str(automata1.final_states)[2:4]][''] = {str(automata2.initial_state)}

      automata = NFA(
        states=esta2,
        input_symbols= sim,
        transitions=dic1,
        initial_state=automata1.initial_state,
        final_states= set(automata2.final_states)
        )
      return automata, tipo1

    else:
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      return concatenacion(automata1, tipo1, automata2, tipo2)
  else:
    if tipo1:
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      return concatenacion(automata1, tipo1, automata2, tipo2)
      
    if tipo2:
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      return concatenacion(automata1, tipo1, automata2, tipo2)
    

def interseccion (automata1, tipo1, automata2, tipo2): # ingresan 2 automatas afd y salen 1 afnd 
  if tipo1 == tipo2:
    if tipo1 == False:
      automata1, tipo1 = complemento (automata1, tipo1)
      automata1, tipo1 = AFDtoAFND (automata1, tipo1)
      automata2, tipo2 = complemento (automata2, tipo2)
      automata2, tipo2 = AFDtoAFND (automata2, tipo2)
      automata3, tipo3 = union (automata1, tipo1, automata2, tipo2)
      automata3, tipo3 = AFNDtoAFD (automata3, tipo3)
      automata3, tipo3 = complemento (automata3, tipo3)
      return automata3, tipo3
    else:
      automata1, tipo1 = AFNDtoAFD (automata1, tipo1)
      automata2, tipo2 = AFNDtoAFD (automata2, tipo2)
      return interseccion (automata1, tipo1, automata2, tipo2)
  else:
    if tipo1:
      automata2, tipo2 = AFNDtoAFD (automata2, tipo2)
      return interseccion (automata1, tipo1, automata2, tipo2)
      
    if tipo2:
      automata1, tipo1 = AFNDtoAFD (automata1, tipo1)
      return interseccion (automata1, tipo1, automata2, tipo2)
  

#Funciones para graficar automata
def imprimirAutomata(automata):

  print ('initial_state : ', automata.initial_state)
  print ('final_states : ', automata.final_states)
  print ('states : ', automata.states)  
  print ('input_symbols : ', automata.input_symbols)
  print ('transitions : ', automata.transitions)


def draw(automata, tipo):

    listaTransicion = []
    if tipo == False: #dfa
        for k,v in automata.transitions.items():
            for i in v:
                listaTransicion.append(( k, v[i], i))

    else:  #nfa
        for k,v in automata.transitions.items():
            for i in v:
                for j in v[i]:
                    listaTransicion.append(( k,j, i))
    
    g = gv.Digraph()
    g.graph_attr['rankdir'] = 'LR'
    g.node('ini', shape="point")
    
    for e in list(automata.states):
        if e in list(automata.final_states):
            g.node(e, shape="doublecircle")
        else:
            g.node(e)
        if e in [automata.initial_state]:
            g.edge('ini',e)

    for t in listaTransicion:
        if t[2] not in list(automata.input_symbols):
            return 0
        g.edge(t[0], t[1], label=str(t[2]))
    
    return g.pipe(format='png')

  