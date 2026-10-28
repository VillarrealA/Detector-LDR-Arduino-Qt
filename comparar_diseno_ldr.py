#!/usr/bin/env python3
"""Comparación de dos configuraciones ópticas para la práctica LDR.

Uso:
    python comparar_diseno_ldr.py diseno_A.csv diseno_B.csv
    python comparar_diseno_ldr.py diseno_A.csv diseno_B.csv --salida comparacion

Cada CSV debe contener led_referencia (0/1) y adc_ldr (0..1023).
No compara el umbral de Qt: AUC/AP se obtienen de las lecturas ADC.
"""
import argparse
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def leer(path):
    y, x = [], []
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            y.append(int(row['led_referencia']))
            x.append(int(row['adc_ldr']))
    y, x = np.array(y), np.array(x)
    if not len(y) or not {0, 1}.issubset(set(y)):
        raise ValueError(f'{path}: debe tener ensayos de ambas clases')
    if not set(y).issubset({0, 1}) or np.any((x < 0) | (x > 1023)):
        raise ValueError(f'{path}: valores de referencia o ADC inválidos')
    return y, x


def evaluar(y, x):
    thresholds = [np.inf] + sorted(set(x), reverse=True)
    fpr, tpr, precision = [], [], []
    pos, neg = np.sum(y == 1), np.sum(y == 0)
    for t in thresholds:
        p = x >= t
        vp, fp = np.sum(p & (y == 1)), np.sum(p & (y == 0))
        fpr.append(fp / neg)
        tpr.append(vp / pos)
        precision.append(vp/(vp+fp) if vp+fp else 1.)
    fpr, tpr, precision = map(np.array, (fpr, tpr, precision))
    auc = float(np.trapz(tpr, x=fpr))
    ap = float(np.sum(np.diff(tpr) * precision[1:]))
    return fpr, tpr, precision, auc, ap


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('diseno_a', type=Path)
    parser.add_argument('diseno_b', type=Path)
    parser.add_argument('--salida', type=Path, default=Path('comparacion_disenos'))
    args = parser.parse_args()
    data = [(name, *leer(path)) for name, path in [('A (original)',args.diseno_a),('B (modificado)',args.diseno_b)]]
    args.salida.mkdir(parents=True, exist_ok=True)
    figroc, axroc = plt.subplots(figsize=(6.2, 5))
    figpr, axpr = plt.subplots(figsize=(6.2, 5))
    print('Diseño\tN\tpositivos\tAUC ROC\tAP')
    for name, y, x in data:
        fpr, tpr, pr, auc, ap = evaluar(y, x)
        print(f'{name}\t{len(y)}\t{sum(y)}\t{auc:.3f}\t{ap:.3f}')
        axroc.step(fpr, tpr, where='post', label=f'{name}: AUC={auc:.3f}')
        axpr.step(tpr, pr, where='post', label=f'{name}: AP={ap:.3f}')
    axroc.plot([0,1],[0,1],'--',color='gray',label='Azar')
    axroc.set(xlim=(0,1), ylim=(0,1.03), xlabel='1 - especificidad (FPR)',ylabel='Sensibilidad (TPR)',title='Comparación de curvas ROC')
    axroc.grid(alpha=.2); axroc.legend(); figroc.tight_layout()
    figroc.savefig(args.salida/'comparacion_roc.png',dpi=180)
    axpr.set(xlim=(0,1), ylim=(0,1.03), xlabel='Recall (sensibilidad)', ylabel='Precisión (VPP)',title='Comparación de curvas PR')
    axpr.grid(alpha=.2); axpr.legend(); figpr.tight_layout()
    figpr.savefig(args.salida/'comparacion_pr.png',dpi=180)
    plt.close('all')
    if np.mean(data[0][1]) != np.mean(data[1][1]):
        print('ADVERTENCIA: distinta proporción de positivos; comparar AP/PR con cuidado.')
    print('Archivos creados en',args.salida)

if __name__ == '__main__':
    main()
