#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, execute
from qiskit.visualization import plot_histogram
import argparse,sys, time

def simon_qc(n:int)->object:
    simon_circ = QuantumCircuit(2*n)
    return simon_circ

def hadamard_gates(s:str,simon_circ:object,barr:bool)->object:
    if barr:
        simon_circ.barrier()
    return simon_circ.h(range(len(s)))

def query2qubit(s:str,simon_circ:object,barr:bool)->None:
    simon_circ.cx(0,len(s)+0)
    simon_circ.cx(0,len(s)+1)
    simon_circ.cx(1,len(s)+0)
    simon_circ.cx(1,len(s)+1)
    if barr:
        simon_circ.barrier()

def mess(s:str,simon_circ:object)->None:
    simon_circ.h(range(len(s)))
    simon_circ.measure_all()

def draw_figure_and_save(simon_circ:object)->None:
    fig = simon_circ.draw(output='mpl')
    fig.savefig(fname='blatt_4_aufgabe_4_altenschmidt.png')

def main():
    des="Implemeting Quantum Simon Circuit"
    epi="Built by Qu@ntumCyb3rW01f/Qu@ntumH@ck3r Thi Altenschmidt"
    parser=argparse.ArgumentParser(description=des,epilog=epi)
    parser.add_argument("--str","-s",action="store",dest="string",type=str,
            help="Specify the s string in Simon Problem. Default 0000",default="0000")
    parser.add_argument("--num","-n",action="store",dest="num",type=int,
            help="Specify the dimension. Default n = 4.",default=4)
    parser.add_argument("--meas","-m",action="store",dest="meas",type=int,
            help="Specify number of rounds. Default 1000",default=1000)
    given_args=parser.parse_args()
    string=given_args.string
    
    try:
        num=int(given_args.num)
        meas=int(given_args.meas)
    except ValueError as val_err:
        print("[-] Illegal input of dimension or number of rounds")
        sys.exit(-1)

    if(num <= 0) or (meas <= 0):
        print("[!] Dimension/Number of rounds must be positive")
        sys.exit(-1)

    print("Usage: {} --help/-h for more information".format(sys.argv[0]))
    time.sleep(0.5)
    print("We use by default s = 0000. Since we didn't solve part III of Exercise 3")
    barr = True
    sc = simon_qc(num)
    hadamard_gates(string,sc,barr)
    query2qubit(string,sc,barr)
    mess(string,sc)
    backend=BasicAer.get_backend('qasm_simulator')
    res=execute(sc,backend=backend,shots=meas).result()
    ans=res.get_counts()
    draw_figure_and_save(sc)
    ans_plt={}
    for m in ans.keys():
        m_input = m[len(string):]
        if m_input in ans_plt:
            ans_plt[m_input]+=ans[m]
        else:
            ans_plt[m_input]=ans[m]

    print(ans_plt)
    plt = plot_histogram(ans_plt)
    plt.savefig(fname="blatt_4_aufgabe_4_altenschmidt_plt_histogram.png")

if __name__ == "__main__":
    main()

