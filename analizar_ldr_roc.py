#!/usr/bin/env python3
"""Curvas ROC y precisión-recall para la práctica LDR + Qt Designer.

Lee CSV generados por app_ldr.py con las columnas:
    ensayo,hora,led_referencia,adc_ldr,umbral_adc,decision_detectado,categoria

IMPORTANTE: usa solo led_referencia y adc_ldr para construir curvas; NO reutiliza
la clasificación hecha con el umbral de la primera práctica.

Ejemplos:
    python analizar_ldr_roc.py seleccion_equipo1.csv
    python analizar_ldr_roc.py seleccion_equipo1.csv --umbral 530 \
        --validacion validacion_equipo1.csv

Requisitos: numpy y matplotlib. No requiere scikit-learn.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def leer_csv(ruta: Path) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve referencias binarias y lecturas ADC, con validaciones."""
    ref: list[int] = []
    adc: list[int] = []
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        necesarias = {"led_referencia", "adc_ldr"}
        if not lector.fieldnames or not necesarias.issubset(lector.fieldnames):
            raise ValueError(
                f"Faltan columnas en {ruta.name}: se requieren {sorted(necesarias)}"
            )
        for numero, fila in enumerate(lector, start=2):
            try:
                r = int(fila["led_referencia"])
                a = int(fila["adc_ldr"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Fila {numero}: referencia o ADC no es entero") from exc
            if r not in (0, 1):
                raise ValueError(f"Fila {numero}: led_referencia debe ser 0 o 1")
            if not 0 <= a <= 1023:
                raise ValueError(f"Fila {numero}: adc_ldr fuera de 0..1023")
            ref.append(r)
            adc.append(a)

    if not ref:
        raise ValueError("El CSV no contiene ensayos")
    y = np.asarray(ref, dtype=int)
    puntaje = np.asarray(adc, dtype=int)
    if len(np.unique(y)) < 2:
        raise ValueError(
            "Se requieren al menos un ensayo con LED encendido y uno apagado "
            "para calcular ROC y sensibilidad/especificidad."
        )
    return y, puntaje


def metricas(y: np.ndarray, adc: np.ndarray, umbral: int) -> dict:
    """Usa estrictamente la regla del Qt original: DETECTADO si ADC > umbral."""
    pred = adc > umbral
    vp = int(np.sum((y == 1) & pred))
    fn = int(np.sum((y == 1) & ~pred))
    fp = int(np.sum((y == 0) & pred))
    vn = int(np.sum((y == 0) & ~pred))
    sensibilidad = vp / (vp + fn)
    especificidad = vn / (vn + fp)
    precision = vp / (vp + fp) if vp + fp else float("nan")
    return {
        "umbral": umbral,
        "VP": vp,
        "FN": fn,
        "FP": fp,
        "VN": vn,
        "sensibilidad": sensibilidad,
        "especificidad": especificidad,
        "FPR": 1 - especificidad,
        "precision": precision,
        "recall": sensibilidad,
        "F1": (2 * vp / (2 * vp + fp + fn)) if 2 * vp + fp + fn else float("nan"),
    }


def tabla_umbrales(y: np.ndarray, adc: np.ndarray) -> list[dict]:
    # Todos los umbrales admitidos por Qt (0..1023).
    return [metricas(y, adc, u) for u in range(1024)]


def escribir_tabla(ruta: Path, filas: list[dict]) -> None:
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)


def curvas(y: np.ndarray, adc: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float, float]:
    # Incluimos -1 (detecta todo) y 1023 (no detecta nada) para completar
    # extremos. Recorremos de umbral alto a bajo: FPR y TPR no decrecen.
    puntos = [metricas(y, adc, u) for u in range(1023, -2, -1)]
    fpr = np.array([d["FPR"] for d in puntos])
    tpr = np.array([d["sensibilidad"] for d in puntos])
    precisiones = np.array([
        d["precision"] if np.isfinite(d["precision"]) else 1.0
        for d in puntos
    ])
    recall = tpr.copy()
    if hasattr(np, "trapezoid"):
        auc = float(np.trapezoid(tpr, x=fpr))
    else:
        auc = float(np.trapz(tpr, x=fpr))
    # Average precision: incremento de recall ponderado por precisión.
    # Usamos 1.0 en recall=0 sin positivos predichos (convención de trazado).
    ap = float(np.sum(np.diff(recall) * precisiones[1:]))
    return fpr, tpr, recall, precisiones, auc, ap


def graficar(y: np.ndarray, adc: np.ndarray, salida: Path) -> tuple[float, float]:
    fpr, tpr, recall, prec, auc, ap = curvas(y, adc)
    salida.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6.1, 4.8))
    ax.step(fpr, tpr, where="post", lw=2.0, color="#176E96", label=f"ROC (AUC={auc:.3f})")
    ax.plot([0, 1], [0, 1], "--", lw=1, color="gray", label="Azar")
    ax.set(xlabel="Tasa de falsos positivos (1 - especificidad)",
           ylabel="Sensibilidad", title="Curva ROC", xlim=(0, 1), ylim=(0, 1.02))
    ax.grid(alpha=0.2)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(salida / "curva_roc.png", dpi=180)
    plt.close(fig)

    proporcion = float(np.mean(y))
    fig, ax = plt.subplots(figsize=(6.1, 4.8))
    ax.step(recall, prec, where="post", lw=2.0, color="#24765F", label=f"PR (AP={ap:.3f})")
    ax.axhline(proporcion, ls="--", color="gray", lw=1,
               label=f"Fracción positiva = {proporcion:.2f}")
    ax.set(xlabel="Recall (sensibilidad)", ylabel="Precisión (VP / [VP + FP])",
           title="Curva precisión-recall", xlim=(0, 1), ylim=(0, 1.02))
    ax.grid(alpha=0.2)
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(salida / "curva_pr.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.hist(adc[y == 0], bins=np.arange(0, 1076, 50), alpha=0.7,
            label="LED apagado (0)", color="#CE8B33")
    ax.hist(adc[y == 1], bins=np.arange(0, 1076, 50), alpha=0.6,
            label="LED encendido (1)", color="#176E96")
    ax.set(xlabel="Lectura de la LDR (cuentas ADC)", ylabel="Número de ensayos",
           title="Distribución de la respuesta del sensor", xlim=(0, 1023))
    ax.legend()
    fig.tight_layout()
    fig.savefig(salida / "distribucion_adc.png", dpi=180)
    plt.close(fig)
    return auc, ap


def resumen(m: dict) -> str:
    p = "no definida" if not np.isfinite(m["precision"]) else f'{m["precision"]:.1%}'
    return (f'umbral={m["umbral"]} | VP={m["VP"]}, FN={m["FN"]}, '
            f'FP={m["FP"]}, VN={m["VN"]} | '
            f'Se={m["sensibilidad"]:.1%}, Sp={m["especificidad"]:.1%}, '
            f'precisión={p}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seleccion", type=Path, help="CSV usado para elegir umbral")
    parser.add_argument("--umbral", type=int, help="Umbral final entre 0 y 1023, elegido ANTES de validar")
    parser.add_argument("--validacion", type=Path, help="CSV de ensayos nuevos y separados")
    parser.add_argument("--salida", type=Path, default=Path("resultados_roc"),
                        help="Carpeta para curvas y tabla de umbrales")
    args = parser.parse_args()
    if args.umbral is not None and not 0 <= args.umbral <= 1023:
        parser.error("--umbral debe estar entre 0 y 1023")
    if args.validacion is not None and args.umbral is None:
        parser.error("Para evaluar --validacion debe fijar --umbral")
    if args.validacion is not None and args.validacion.resolve() == args.seleccion.resolve():
        parser.error("Selección y validación deben ser archivos diferentes")

    y, adc = leer_csv(args.seleccion)
    args.salida.mkdir(parents=True, exist_ok=True)
    filas = tabla_umbrales(y, adc)
    escribir_tabla(args.salida / "tabla_umbrales.csv", filas)
    auc, ap = graficar(y, adc, args.salida)
    print(f"Selección: {args.seleccion} ({len(y)} ensayos, {sum(y)} positivos, {sum(y == 0)} negativos)")
    print(f"AUC ROC={auc:.3f}; average precision (AP)={ap:.3f}")
    print("Se generaron tres PNG y tabla_umbrales.csv en", args.salida)
    print("Ejemplos para explorar; NO constituyen selección automática de umbral:")
    for u in (300, 400, 500, 600, 700):
        print(" ", resumen(filas[u]))

    if args.umbral is not None:
        m_sel = filas[args.umbral]
        print("\nUmbral decidido por el equipo: ", resumen(m_sel))
        if args.validacion is not None:
            y_v, adc_v = leer_csv(args.validacion)
            m_val = metricas(y_v, adc_v, args.umbral)
            print("Validación sin reajuste:      ", resumen(m_val))
            comparacion = []
            for nombre, m, ys in (("seleccion", m_sel, y), ("validacion", m_val, y_v)):
                d = {"conjunto": nombre, "n": len(ys), "positivos": int(sum(ys)), **m}
                comparacion.append(d)
            escribir_tabla(args.salida / "comparacion_seleccion_validacion.csv", comparacion)
            print("Se guardó comparacion_seleccion_validacion.csv")


if __name__ == "__main__":
    main()
