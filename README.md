# Gestor de Entrenamiento

App de escritorio en Python + Tkinter para llevar tu entrenamiento de fuerza de forma simple y ordenada: gestiona rutinas, series, repeticiones, descansos con cronómetro y progresión de pesos por perfil de atleta.

Ideal si entrenas con división por grupos musculares y quieres saber cuándo subir carga sin adivinar: la app registra pesos, calcula promedios de repeticiones y te avisa cuando estás en rango para aumentar.

## Características

- **Perfiles de atleta:** crea múltiples perfiles, cada uno con su nombre, peso corporal y rutinas propias. Ideal para compartir la PC o llevar varios objetivos.
- **Rutinas por grupo muscular:** crea rutinas para Empuje, Tracción, Piernas, FullBody, Torso, Brazo, Cardio o cualquier nombre custom que escribas. Las pestañas se pueden reordenar arrastrando.
- **Ejercicios propios:** agrega tus propios ejercicios en cada rutina, con objetivo de repeticiones, descanso y peso inicial. También puedes eliminarlos cuando quieras.
- **Series flexibles:** cada ejercicio parte de una base (por defecto 3) y puedes agregar más series hasta 6 con el botón `+ Serie`. Contador `hechas/total`, marcas visuales ✔/○ y reinicio por ejercicio o por rutina completa.
- **Modo Series/Segundos:** cada ejercicio tiene botón `⏱ Modo` para medir en repeticiones o en segundos (ej. plancha). Cambia etiquetas a `Segundos`, base de 8 a 20, carga a `Segundos Actuales` y registros/promedios a `segs`.
- **Sesión persistente por día:** lo finalizado queda en verde `FINALIZADO ✔` aunque cierres la app. Solo se reinicia con `↻` o al abrir en un día nuevo.
- **Conteo de repeticiones:** registra las repes hechas en cada serie con spinbox (0-200). Al finalizar se guarda fecha, peso, detalle por serie y promedio.
- **Registro de peso y promedio por ejercicio:** panel lateral `Registro` con último peso, promedio, detalle de series, historial de los últimos 4 registros y ciclo congelado del último bloque de 4 al mismo peso.
- **Aviso de aumentar carga:** si completas 4 registros seguidos al mismo peso con promedio entre 10 y 12 repeticiones, muestra `⬆ Aumentar carga`.
- **Peso corporal con historial:** coloca tu peso actual y actualízalo cuando quieras. Guarda fecha y un registro de los últimos 5 pesos para compararlo a lo largo del tiempo, con vista de historial y opción de borrar registro.
- **Cronómetro de descanso:** temporizador configurable por ejercicio (minutos/segundos), con alarma sonora en Windows y aviso al terminar.
- **Datos locales:** todo se guarda en `entrenamiento_perfiles_multi.json` junto al script (ignorado por git: son datos personales). Sin cuentas, sin internet.

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
