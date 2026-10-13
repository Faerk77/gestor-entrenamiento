# Gestor de Entrenamiento

App de escritorio en Python + Tkinter para gestionar rutinas, series,
repeticiones, descansos con cronómetro y progresión de pesos por perfil de atleta.

## Requisitos

- Python 3.10+ (solo librería estándar, sin dependencias)
- Windows (el sonido de la alarma usa `winsound`; en otros sistemas la app
  funciona igual pero sin sonido)

## Uso

```bash
python Entrenamiento.py
```

Los datos se guardan en `entrenamiento_perfiles_multi.json` junto al script
(ignorado por git: son datos personales).
