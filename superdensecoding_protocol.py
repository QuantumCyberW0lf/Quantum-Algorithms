#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from qiskit import *

def init_ver(qc:object,b_0:int,b_1:int)->None:
    qc.h(b_0) #h-gate auf das erste qubit
    qc.cx(b_0,b_1) #CNOT

def enc_msg(qc:object,qubit:int,msg:str)->None:
    if msg == "10": qc.x(qubit) #X-Gate fuer 10
    elif msg == "01": qc.z(qubit) #Z-Gate fuer 01
    elif msg == "11":
        qc.z(qubit)
        qc.x(qubit)
    else:
        print("[-] 00 ist eine ungueltige Nachricht")

def dec_msg(qc:object,b_0:int,b_1:int)->None:
    qc.cx(b_0,b_1)
    qc.h(b_0)


def main():
    """
    Initialisierung eines verschraenkten Zustandes
    """
    qc = QuantumCircuit(2)
    init_ver(qc,0,1) # 0 -> Alice, 1 -> Bob
    msg_comb = ["10","01","11","00"]
    for msg in msg_comb:
        enc_msg(qc,0,msg)
        qc.barrier()
        dec_msg(qc,0,1)
        qc.measure_all()
        figure_msg=qc.draw(output="mpl")
        figure_msg.savefig(fname="blatt_2_aufgabe_5_altenschmidt"+msg)

if __name__ == "__main__":
    main()
