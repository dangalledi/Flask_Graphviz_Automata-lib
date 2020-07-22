from flask import Flask, render_template
import base64
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz-2.38/release/bin/'

from funciones import draw

import graphviz as gv

from automata.fa.dfa import DFA   #Libreria Automata
from automata.fa.nfa import NFA

app = Flask(__name__)

@app.route('/')
def img():

    dfa = DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q2', '1': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)

    automata = draw(dfa, False)
    automata = base64.b64encode(automata).decode('utf-8')

    return render_template('image.html', automata=automata)

if __name__ == '__main__':
    app.run(debug=True) 
