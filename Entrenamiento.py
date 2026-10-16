import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, simpledialog, ttk

DATA_FILE = "entrenamiento_perfiles_multi.json"

__version__ = "1.4.0"


class SeleccionPerfilWindow:

  def __init__(self, root, on_perfil_seleccionado):
    self.root = root
    self.win = tk.Toplevel(root)
    self.win.title("Seleccionar Perfil - Gestor de Entrenamiento")
    self.win.geometry("400x450")
    self.win.resizable(False, False)
    self.win.grab_set()

    self.win.update_idletasks()
    w, h = 400, 450
    x = (self.win.winfo_screenwidth() // 2) - (w // 2)
    y = (self.win.winfo_screenheight() // 2) - (h // 2)
    self.win.geometry(f"{w}x{h}+{x}+{y}")

    self.on_perfil_seleccionado = on_perfil_seleccionado
    self.datos_globales = self.cargar_todos_los_datos()

    frame = ttk.Frame(self.win, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(
        frame,
        text="Selecciona tu Perfil de Atleta",
        font=("Arial", 14, "bold"),
    ).pack(pady=10)

    self.listbox_perfiles = tk.Listbox(frame, height=8, font=("Arial", 11))
    self.listbox_perfiles.pack(fill=tk.BOTH, expand=True, pady=10)
    self.actualizar_lista_perfiles()

    btn_ingresar = ttk.Button(
        frame, text="Ingresar con este Perfil", command=self.ingresar_perfil
    )
    btn_ingresar.pack(fill=tk.X, pady=5)

    btn_nuevo = ttk.Button(
        frame, text="+ Crear Nuevo Perfil", command=self.crear_nuevo_perfil
    )
    btn_nuevo.pack(fill=tk.X, pady=5)

    btn_eliminar = ttk.Button(
        frame, text="🗑 Eliminar Perfil Seleccionado", command=self.eliminar_perfil
    )
    btn_eliminar.pack(fill=tk.X, pady=5)

  def cargar_todos_los_datos(self):
    if os.path.exists(DATA_FILE):
      try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
          return json.load(f)
      except Exception:
        return {}
    return {}

  def actualizar_lista_perfiles(self):
    self.listbox_perfiles.delete(0, tk.END)
    for nombre_perfil in self.datos_globales.keys():
      self.listbox_perfiles.insert(tk.END, nombre_perfil)

  def ingresar_perfil(self):
    seleccion = self.listbox_perfiles.curselection()
    if not seleccion:
      messagebox.showwarning(
          "Aviso", "Por favor selecciona un perfil de la lista.", parent=self.win
      )
      return

    nombre_perfil = self.listbox_perfiles.get(seleccion[0])
    perfil_data = self.datos_globales[nombre_perfil]
    self.win.destroy()
    self.on_perfil_seleccionado(nombre_perfil, perfil_data)

  def crear_nuevo_perfil(self):
    self.win.withdraw()
    SetupPerfilWindow(
        self.root, self.datos_globales, self, self.on_perfil_seleccionado
    )

  def eliminar_perfil(self):
    seleccion = self.listbox_perfiles.curselection()
    if not seleccion:
      messagebox.showwarning(
          "Aviso", "Selecciona un perfil para eliminar.", parent=self.win
      )
      return

    nombre_perfil = self.listbox_perfiles.get(seleccion[0])
    if messagebox.askyesno(
        "Confirmar",
        f"¿Estás seguro de eliminar el perfil '{nombre_perfil}' y todo su"
        " historial?",
        parent=self.win,
    ):
      del self.datos_globales[nombre_perfil]
      try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
          json.dump(self.datos_globales, f, indent=4, ensure_ascii=False)
      except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=self.win)
      self.actualizar_lista_perfiles()


class SetupPerfilWindow:

  def __init__(
      self, root, datos_globales, ventana_seleccion_anterior, callback_guardar
  ):
    self.root = root
    self.ventana_seleccion_anterior = ventana_seleccion_anterior

    self.win = tk.Toplevel(root)
    self.win.title("Crear Nuevo Perfil")
    self.win.geometry("450x660")
    self.win.resizable(False, False)
    self.win.grab_set()

    self.win.update_idletasks()
    w, h = 450, 660
    x = (self.win.winfo_screenwidth() // 2) - (w // 2)
    y = (self.win.winfo_screenheight() // 2) - (h // 2)
    self.win.geometry(f"{w}x{h}+{x}+{y}")

    self.datos_globales = datos_globales
    self.callback_guardar = callback_guardar

    frame = ttk.Frame(self.win, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    top_setup_bar = ttk.Frame(frame)
    top_setup_bar.pack(fill=tk.X, pady=(0, 5))

    btn_atras = ttk.Button(
        top_setup_bar, text="← Atrás", command=self.volver_a_seleccion
    )
    btn_atras.pack(side=tk.LEFT)

    ttk.Label(
        frame, text="Configuración de Nuevo Perfil", font=("Arial", 12, "bold")
    ).pack(pady=5)

    ttk.Label(frame, text="Tu Nombre:").pack(anchor=tk.W, pady=(5, 0))
    self.ent_nombre = ttk.Entry(frame, width=30)
    self.ent_nombre.pack(fill=tk.X, pady=5)

    ttk.Label(frame, text="Peso Corporal Actual (kg):").pack(
        anchor=tk.W, pady=(5, 0)
    )
    self.ent_peso = ttk.Entry(frame, width=30)
    self.ent_peso.pack(fill=tk.X, pady=5)
    self.ent_peso.insert(0, "70.0")

    ttk.Label(
        frame, text="Días de Rutina Seleccionados:", font=("Arial", 10, "bold")
    ).pack(anchor=tk.W, pady=(10, 5))

    self.rutinas_seleccionadas = ["Empuje", "Tracción", "Piernas", "FullBody"]

    list_frame = ttk.Frame(frame)
    list_frame.pack(fill=tk.X, pady=5)

    self.listbox_rutinas = tk.Listbox(
        list_frame, height=4, font=("Arial", 10)
    )
    self.actualizar_listbox()
    self.listbox_rutinas.pack(
        side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5)
    )

    btn_quitar = ttk.Button(
        list_frame, text="Quitar Seleccionada", command=self.quitar_rutina
    )
    btn_quitar.pack(side=tk.RIGHT, anchor=tk.N)

    ttk.Label(
        frame, text="Agregar Rutina (Desplegable o Escribir Custom):"
    ).pack(anchor=tk.W, pady=(10, 2))

    add_frame = ttk.Frame(frame)
    add_frame.pack(fill=tk.X, pady=5)

    self.opciones_default = [
        "Empuje",
        "Tracción",
        "FullBody",
        "Piernas",
        "Torso",
        "Brazo",
        "Cardio",
    ]
    self.combo_rutina = ttk.Combobox(
        add_frame, values=self.opciones_default, state="normal", width=18
    )
    self.combo_rutina.pack(side=tk.LEFT, padx=(0, 5))
    self.combo_rutina.set("Empuje")

    btn_agregar_lista = ttk.Button(
        add_frame, text="Agregar a la lista", command=self.agregar_rutina_lista
    )
    btn_agregar_lista.pack(side=tk.LEFT)

    custom_frame = ttk.Frame(frame)
    custom_frame.pack(fill=tk.X, pady=8)

    ttk.Label(custom_frame, text="Rutina customizada:").pack(
        anchor=tk.W, pady=(0, 2)
    )
    sub_custom = ttk.Frame(custom_frame)
    sub_custom.pack(fill=tk.X)

    self.ent_custom_rutina = ttk.Entry(sub_custom, width=22)
    self.ent_custom_rutina.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)

    btn_agregar_custom = ttk.Button(
        sub_custom,
        text="Añadir Custom",
        command=self.agregar_rutina_customizada,
    )
    btn_agregar_custom.pack(side=tk.LEFT)

    btn_guardar = ttk.Button(
        frame, text="Guardar y Comenzar", command=self.procesar_setup
    )
    btn_guardar.pack(pady=15)

  def volver_a_seleccion(self):
    self.win.destroy()
    if self.ventana_seleccion_anterior:
      self.ventana_seleccion_anterior.datos_globales = (
          self.ventana_seleccion_anterior.cargar_todos_los_datos()
      )
      self.ventana_seleccion_anterior.actualizar_lista_perfiles()
      self.ventana_seleccion_anterior.win.deiconify()
      self.ventana_seleccion_anterior.win.grab_set()

  def actualizar_listbox(self):
    self.listbox_rutinas.delete(0, tk.END)
    for r in self.rutinas_seleccionadas:
      self.listbox_rutinas.insert(tk.END, r)

  def agregar_rutina_lista(self):
    nueva = self.combo_rutina.get().strip()
    if nueva:
      if nueva not in self.rutinas_seleccionadas:
        self.rutinas_seleccionadas.append(nueva)
        self.actualizar_listbox()
        if nueva not in self.opciones_default:
          self.opciones_default.append(nueva)
          self.combo_rutina["values"] = self.opciones_default
      else:
        messagebox.showwarning(
            "Aviso", "Esa rutina ya está en la lista.", parent=self.win
        )

  def agregar_rutina_customizada(self):
    nueva = self.ent_custom_rutina.get().strip()
    if nueva:
      if nueva not in self.rutinas_seleccionadas:
        self.rutinas_seleccionadas.append(nueva)
        self.actualizar_listbox()
        if nueva not in self.opciones_default:
          self.opciones_default.append(nueva)
          self.combo_rutina["values"] = self.opciones_default
        self.ent_custom_rutina.delete(0, tk.END)
      else:
        messagebox.showwarning(
            "Aviso", "Esa rutina ya está en la lista.", parent=self.win
        )
    else:
      messagebox.showwarning(
          "Aviso",
          "Por favor escribe un nombre para la rutina custom.",
          parent=self.win,
      )

  def quitar_rutina(self):
    seleccion = self.listbox_rutinas.curselection()
    if seleccion:
      idx = seleccion[0]
      del self.rutinas_seleccionadas[idx]
      self.actualizar_listbox()
    else:
      messagebox.showwarning(
          "Aviso", "Selecciona una rutina de la lista para quitar.", parent=self.win
      )

  def procesar_setup(self):
    nombre = self.ent_nombre.get().strip()
    if not nombre:
      messagebox.showerror(
          "Error", "Debes ingresar un nombre para el perfil.", parent=self.win
      )
      return

    if nombre in self.datos_globales:
      messagebox.showerror(
          "Error", "Ya existe un perfil con ese nombre.", parent=self.win
      )
      return

    try:
      peso = float(self.ent_peso.get())
    except ValueError:
      messagebox.showerror(
          "Error", "El peso corporal debe ser un número válido.", parent=self.win
      )
      return

    if not self.rutinas_seleccionadas:
      messagebox.showerror(
          "Error", "Debes tener al menos una rutina en la lista.", parent=self.win
      )
      return

    perfil_data = {
        "nombre": nombre,
        "peso_corporal": peso,
        "configuracion_default": {"series": 3, "repes": "10-12", "descanso": 120},
        "atajo_tecla": "<space>",
        "rutinas": {dia: {} for dia in self.rutinas_seleccionadas},
    }

    self.datos_globales[nombre] = perfil_data
    try:
      with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(self.datos_globales, f, indent=4, ensure_ascii=False)
    except Exception as e:
      messagebox.showerror(
          "Error", f"No se pudo guardar: {e}", parent=self.win
      )
      return

    self.win.destroy()
    if self.ventana_seleccion_anterior:
      try:
        self.ventana_seleccion_anterior.win.destroy()
      except Exception:
        pass
    self.callback_guardar(nombre, perfil_data)


class AppEntrenamiento:

  def __init__(self, root):
    self.root = root
    self.root.title(f"Gestor de Entrenamiento y Progresión v{__version__}")

    # Ventana fija, centrada y no redimensionable.
    ANCHO, ALTO = 880, 700
    self.root.geometry(f"{ANCHO}x{ALTO}")
    self.root.update_idletasks()
    x = (self.root.winfo_screenwidth() // 2) - (ANCHO // 2)
    y = (self.root.winfo_screenheight() // 2) - (ALTO // 2)
    self.root.geometry(f"{ANCHO}x{ALTO}+{x}+{y}")
    self.root.resizable(False, False)

    self.nombre_perfil_actual = None
    self.datos_perfil = None
    # Estado de sesión por rutina: refs de tarjetas y ejercicio activo.
    # refs_por_rutina[rutina][ej] = {series_hechas, marca_labels, reps_widgets,
    #   iniciar/detener_crono, card_frame, base_title, lbl_contador, botones...}
    self.refs_por_rutina = {}
    self.vars_activas_por_rutina = {}
    self.canvas_por_rutina = {}
    self.notebook_rutinas = None
    self._drag_tab = None

    self.root.withdraw()
    SeleccionPerfilWindow(self.root, self.on_perfil_seleccionado)

  def on_perfil_seleccionado(self, nombre_perfil, perfil_data):
    self.nombre_perfil_actual = nombre_perfil
    self.datos_perfil = perfil_data
    self.root.deiconify()
    self.iniciar_interfaz_principal()

  def _scroll_rueda(self, event):
    # Rueda del mouse en toda la ventana: desplaza la rutina visible,
    # solo si hay contenido fuera de vista.
    try:
      if self.root.grab_current() is not None:
        return
      if self.notebook_rutinas is None or not self.notebook_rutinas.tabs():
        return
      rutina = self._rutina_activa()
      cv = self.canvas_por_rutina.get(rutina) if rutina else None
      if cv is None:
        return
      try:
        region = str(cv.cget("scrollregion") or "").split()
        alto_contenido = float(region[3]) if len(region) == 4 else 0.0
      except Exception:
        return
      if alto_contenido <= cv.winfo_height() + 1:
        return
      cv.yview_scroll(int(-1 * (event.delta / 120)), "units")
    except Exception:
      pass

  def _tab_press(self, event):
    try:
      idx = self.notebook_rutinas.index(f"@{event.x},{event.y}")
      self._drag_tab = {"idx": idx}
    except Exception:
      self._drag_tab = None

  def _tab_motion(self, event):
    if not self._drag_tab:
      return
    try:
      destino = self.notebook_rutinas.index(f"@{event.x},{event.y}")
    except Exception:
      return
    origen = self._drag_tab["idx"]
    if destino == origen:
      return
    try:
      hijo = self.notebook_rutinas.tabs()[origen]
      self.notebook_rutinas.insert(destino, hijo)
      self._drag_tab["idx"] = destino
    except Exception:
      pass

  def _tab_release(self, event):
    if not self._drag_tab:
      return
    self._drag_tab = None
    # Persistir el nuevo orden sin reconstruir (conserva la sesión).
    try:
      orden = [
          self.notebook_rutinas.tab(t, option="text")
          for t in self.notebook_rutinas.tabs()
      ]
      rut = self.datos_perfil.get("rutinas", {})
      nuevo = {k: rut[k] for k in orden if k in rut}
      for k in rut:
        if k not in nuevo:
          nuevo[k] = rut[k]
      self.datos_perfil["rutinas"] = nuevo
      self.guardar_datos_actuales()
    except Exception:
      pass

  def _rutina_activa(self):
    try:
      if self.notebook_rutinas is None or not self.notebook_rutinas.tabs():
        rutinas = list(self.datos_perfil.get("rutinas", {}).keys())
        return rutinas[0] if rutinas else None
      actual = self.notebook_rutinas.select()
      if not actual:
        return None
      return self.notebook_rutinas.tab(actual, option="text")
    except Exception:
      return None

  @staticmethod
  def _modo_info(info):
    # Modo por ejercicio: 'repes' (Series) o 'segs' (Segundos).
    # Compatibilidad: sin campo => repes.
    # En modo segs la carga pasa a ser tiempo: 'Segundos Actuales' en vez de
    # 'Peso Actual', y los registros guardan segundos en el mismo campo 'peso'.
    es_segs = info.get("modo", "repes") == "segs"
    if es_segs:
      return {
          "es_segs": True,
          "sing": "Segundos",
          "plur": "Segundos",
          "default_val": 20,
          "unidad": "segs",
          "carga_nombre": "Segundos",
          "carga_unidad": "segs",
          "carga_titulo": "Segundos Actuales (segs):",
          "carga_boton": "Registrar Segundos",
      }
    return {
        "es_segs": False,
        "sing": "Serie",
        "plur": "Series",
        "default_val": 8,
        "unidad": "repes",
        "carga_nombre": "Peso",
        "carga_unidad": "kg",
        "carga_titulo": "Peso Actual (kg):",
        "carga_boton": "Registrar Peso",
    }

  def _toggle_modo(self, rutina_nombre, ej_nombre):
    try:
      info = self.datos_perfil["rutinas"][rutina_nombre][ej_nombre]
    except Exception:
      return
    actual = info.get("modo", "repes")
    nuevo = "segs" if actual != "segs" else "repes"
    info["modo"] = nuevo
    # Ajustar objetivo por defecto al cambiar (preserva customs).
    if nuevo == "segs" and info.get("repes") == "10-12":
      info["repes"] = "20"
    elif nuevo == "repes" and info.get("repes") == "20":
      info["repes"] = "10-12"
    self.guardar_datos_actuales()
    self.iniciar_interfaz_principal()

  @staticmethod
  def _hoy_str():
    return datetime.now().strftime("%Y-%m-%d")

  def _marcar_sesion_finalizada(self, info, valores):
    # Persiste finalizado del día: sobrevive a cerrar/abrir la app el mismo día.
    # Solo se limpia con reset manual o al abrir en fecha distinta.
    info["estado_sesion"] = {
        "fecha": self._hoy_str(),
        "finalizado": True,
        "valores": list(valores),
    }

  def _limpiar_sesion(self, info):
    # Devuelve True si había algo que limpiar.
    if "estado_sesion" in info:
      info.pop("estado_sesion", None)
      return True
    return False

  def _sesion_finalizada_hoy(self, info, num_series):
    # True solo si está finalizado y la fecha es la de hoy. Día distinto => reinicia.
    try:
      est = info.get("estado_sesion", {})
      if not est.get("finalizado"):
        return False, []
      if est.get("fecha") != self._hoy_str():
        return False, []
      vals = est.get("valores", [])
      if len(vals) != int(num_series):
        return False, []
      return True, list(vals)
    except Exception:
      return False, []

  def _actualizar_ciclo_congelado(self, info):
    # Congela el último ciclo completado (4 registros seguidos al mismo peso).
    hist = info.get("historial_series", [])
    if not hist:
      return
    peso_nuevo = hist[-1].get("peso", 0)
    racha = 0
    for r in reversed(hist):
      if r.get("peso", 0) == peso_nuevo:
        racha += 1
      else:
        break
    if racha == 4:
      recs = hist[-4:]
      proms = []
      for r in recs:
        p = r.get("promedio", None)
        if p is None:
          rr = r.get("repes", [])
          p = round(sum(rr) / len(rr), 1) if rr else 0
        proms.append(p)
      prom_total = round(sum(proms) / len(proms), 1) if proms else 0
      info["ciclo_congelado"] = {
          "peso": peso_nuevo,
          "registros": 4,
          "promedio": prom_total,
      }

  def comprobar_y_avanzar_ejercicio(self, rutina_nombre, ej_nombre):
    refs_rutina = self.refs_por_rutina.get(rutina_nombre, {})
    if ej_nombre not in refs_rutina:
      return
    refs = refs_rutina[ej_nombre]
    hechas = refs["series_hechas"]
    card = refs["card_frame"]

    marcadas = sum(1 for h in hechas if h)
    total = len(hechas)
    finalizado = marcadas == total and total > 0

    try:
      refs["lbl_contador"].config(text=f"{marcadas}/{total}")
    except Exception:
      pass
    try:
      if finalizado:
        card.config(bg="#d4edda", text=f"  {refs['base_title']}  —  FINALIZADO ✔  ")
      else:
        card.config(bg="#f0f0f0", text=f"  {refs['base_title']}  ")
    except Exception:
      pass

    if finalizado:
      # Detener crono pendiente.
      try:
        refs["detener_crono_func"]()
      except Exception:
        pass
      # Avanzar al siguiente pendiente de la misma rutina (solo pestaña activa).
      nombres_ej = list(refs_rutina.keys())
      try:
        idx_actual = nombres_ej.index(ej_nombre)
        for siguiente_ej in nombres_ej[idx_actual + 1:]:
          r2 = refs_rutina[siguiente_ej]
          if not all(r2["series_hechas"]):
            self.vars_activas_por_rutina[rutina_nombre].set(siguiente_ej)
            # Mostrar solo el nuevo activo (despliega este, oculta el resto).
            try:
              self._mostrar_solo_activo(rutina_nombre)
            except Exception:
              pass
            break
      except ValueError:
        pass

    self.actualizar_estado_tarjetas()

  def guardar_datos_actuales(self):
    if not self.nombre_perfil_actual:
      return
    if os.path.exists(DATA_FILE):
      try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
          todos = json.load(f)
      except Exception:
        todos = {}
    else:
      todos = {}

    todos[self.nombre_perfil_actual] = self.datos_perfil
    try:
      with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=4, ensure_ascii=False)
    except Exception as e:
      messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")

  def cambiar_perfil(self):
    self.root.withdraw()
    SeleccionPerfilWindow(self.root, self.on_perfil_seleccionado)

  def actualizar_peso_corporal(self):
    peso_actual = self.datos_perfil.get("peso_corporal", 70.0)
    nuevo_peso_str = simpledialog.askstring(
        "Actualizar Peso Corporal",
        "Ingresa tu nuevo peso corporal (kg):",
        initialvalue=str(peso_actual),
        parent=self.root,
    )
    if nuevo_peso_str:
      try:
        nuevo_peso = float(nuevo_peso_str)
        if nuevo_peso < 0:
          raise ValueError
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.datos_perfil["peso_corporal"] = nuevo_peso
        self.datos_perfil["fecha_peso_corporal"] = hoy
        # Registro corporal (máx. 5, sale el más antiguo).
        hist = self.datos_perfil.setdefault("historial_pesos", [])
        hist.append({"fecha": hoy, "peso": nuevo_peso})
        while len(hist) > 5:
          hist.pop(0)
        self.guardar_datos_actuales()
        self.iniciar_interfaz_principal()
      except ValueError:
        messagebox.showerror(
            "Error", "Ingresa un número válido para el peso.", parent=self.root
        )

  def eliminar_historial_peso_corporal(self):
    if not self.datos_perfil.get("historial_pesos") and not self.datos_perfil.get(
        "fecha_peso_corporal"
    ):
      messagebox.showinfo(
          "Historial", "No hay registros para eliminar.", parent=self.root
      )
      return
    if messagebox.askyesno(
        "Confirmar",
        "¿Eliminar el registro de peso corporal? El peso actual se conserva.",
        parent=self.root,
    ):
      self.datos_perfil["historial_pesos"] = []
      self.datos_perfil.pop("fecha_peso_corporal", None)
      self.guardar_datos_actuales()
      self.iniciar_interfaz_principal()

  def ver_historial_peso_corporal(self):
    win = tk.Toplevel(self.root)
    win.title("Historial de peso corporal")
    win.geometry("300x260")
    win.resizable(False, False)
    win.grab_set()
    win.update_idletasks()
    rx, ry = self.root.winfo_x(), self.root.winfo_y()
    rw, rh = self.root.winfo_width(), self.root.winfo_height()
    win.geometry(f"300x260+{rx + rw//2 - 150}+{ry + rh//2 - 130}")
    fr = ttk.Frame(win, padding=12)
    fr.pack(fill=tk.BOTH, expand=True)
    ttk.Label(fr, text="Peso corporal (máx. 5):",
              font=("Arial", 10, "bold")).pack(pady=(0, 8))
    hist = self.datos_perfil.get("historial_pesos", [])
    if not hist:
      ttk.Label(fr, text="Sin registros todavía.",
                font=("Arial", 9, "italic")).pack(pady=10)
    else:
      lb = tk.Listbox(fr, height=6, font=("Arial", 10))
      lb.pack(fill=tk.BOTH, expand=True)
      # Días pasados respecto del registro anterior (el primero sin dato).
      lineas = []
      fecha_prev = None
      for reg in hist:
        txt = f"{reg.get('fecha', '—')}  —  {reg.get('peso', 0)} kg"
        try:
          f = datetime.strptime(str(reg.get("fecha", ""))[:10], "%Y-%m-%d")
          if fecha_prev is not None:
            txt += f"  (+{(f - fecha_prev).days} días)"
          fecha_prev = f
        except Exception:
          pass
        lineas.append(txt)
      for txt in reversed(lineas):
        lb.insert(tk.END, txt)
    ttk.Button(fr, text="Cerrar", command=win.destroy).pack(pady=8)

  def iniciar_interfaz_principal(self):
    tab_previa = self._rutina_activa()
    for widget in self.root.winfo_children():
      widget.destroy()

    main_frame = ttk.Frame(self.root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    top_bar = ttk.Frame(main_frame)
    top_bar.pack(fill=tk.X, pady=3)

    nombre_usr = self.datos_perfil.get("nombre", "Atleta")
    peso_usr = self.datos_perfil.get("peso_corporal", 0.0)
    hist_corp = self.datos_perfil.get("historial_pesos", [])
    if self.datos_perfil.get("fecha_peso_corporal"):
      fecha_corp = self.datos_perfil["fecha_peso_corporal"]
    elif hist_corp:
      fecha_corp = hist_corp[-1].get("fecha", "—")
    else:
      fecha_corp = "—"

    lbl_info_usr = ttk.Label(
        top_bar,
        text=f"Perfil: {nombre_usr}  |  Peso Corporal: {peso_usr} kg ({fecha_corp})",
        font=("Arial", 11, "bold"),
    )
    lbl_info_usr.pack(side=tk.LEFT, padx=(0, 5))

    btn_act_peso = ttk.Button(
        top_bar, text="Actualizar peso", command=self.actualizar_peso_corporal
    )
    btn_act_peso.pack(side=tk.LEFT, padx=5)

    btn_hist_corp = ttk.Button(
        top_bar, text="Historial", command=self.ver_historial_peso_corporal
    )
    btn_hist_corp.pack(side=tk.LEFT, padx=5)

    btn_del_hist_corp = ttk.Button(
        top_bar, text="Eliminar registro",
        command=self.eliminar_historial_peso_corporal,
    )
    btn_del_hist_corp.pack(side=tk.LEFT, padx=5)

    btn_cambiar_perfil = ttk.Button(
        top_bar, text="👤 Cambiar Perfil", command=self.cambiar_perfil
    )
    btn_cambiar_perfil.pack(side=tk.RIGHT, padx=5)

    self.notebook_rutinas = ttk.Notebook(main_frame)
    self.notebook_rutinas.pack(fill=tk.BOTH, expand=True, pady=10)
    self.notebook_rutinas.bind(
        "<<NotebookTabChanged>>", lambda e: self.actualizar_estado_tarjetas()
    )
    self.notebook_rutinas.bind("<ButtonPress-1>", self._tab_press)
    self.notebook_rutinas.bind("<B1-Motion>", self._tab_motion)
    self.notebook_rutinas.bind("<ButtonRelease-1>", self._tab_release)
    self.root.bind_all("<MouseWheel>", self._scroll_rueda)

    self.construir_pestanas_rutinas()

    # Restaurar pestaña activa tras rebuild (evita salto a la primera).
    if tab_previa:
      try:
        for tab_id in self.notebook_rutinas.tabs():
          if self.notebook_rutinas.tab(tab_id, option="text") == tab_previa:
            self.notebook_rutinas.select(tab_id)
            break
      except Exception:
        pass

  def construir_pestanas_rutinas(self):
    for tab in self.notebook_rutinas.tabs():
      self.notebook_rutinas.forget(tab)

    # Rebuild limpio de estado de sesión por rutina.
    self.refs_por_rutina = {}
    self.vars_activas_por_rutina = {}
    self.canvas_por_rutina = {}

    rutinas = self.datos_perfil.get("rutinas", {})

    for rutina_nombre in rutinas.keys():
      rutina_frame = ttk.Frame(self.notebook_rutinas, padding=10)
      self.notebook_rutinas.add(rutina_frame, text=rutina_nombre)
      self.construir_contenido_rutina(rutina_frame, rutina_nombre)

  def construir_contenido_rutina(self, frame, rutina_nombre):
    header_frame = ttk.Frame(frame)
    header_frame.pack(fill=tk.X, pady=5)

    ttk.Label(
        header_frame,
        text=f"Ejercicios para: {rutina_nombre}",
        font=("Arial", 12, "bold"),
    ).pack(side=tk.LEFT)

    btn_agregar = ttk.Button(
        header_frame,
        text="+ Agregar Ejercicio",
        command=lambda: self.agregar_ejercicio(rutina_nombre),
    )
    btn_agregar.pack(side=tk.RIGHT)

    btn_reiniciar_rutina = ttk.Button(
        header_frame,
        text="↻ Reiniciar rutina",
        command=lambda r=rutina_nombre: self.reiniciar_rutina(r),
    )
    btn_reiniciar_rutina.pack(side=tk.RIGHT, padx=(0, 5))

    container_canvas = tk.Canvas(frame, highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        frame, orient="vertical", command=container_canvas.yview
    )
    scrollable_frame = ttk.Frame(container_canvas, padding=5)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: container_canvas.configure(
            scrollregion=container_canvas.bbox("all")
        ),
    )
    container_canvas.create_window(
        (0, 0), window=scrollable_frame, anchor="nw"
    )
    container_canvas.configure(yscrollcommand=scrollbar.set)

    container_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Canvas de esta rutina para el scroll global con la rueda.
    self.canvas_por_rutina[rutina_nombre] = container_canvas

    ejercicios = self.datos_perfil["rutinas"][rutina_nombre]

    if rutina_nombre not in self.refs_por_rutina:
      self.refs_por_rutina[rutina_nombre] = {}
    if rutina_nombre not in self.vars_activas_por_rutina:
      self.vars_activas_por_rutina[rutina_nombre] = tk.StringVar(value="")

    if not ejercicios:
      ttk.Label(
          scrollable_frame,
          text=(
              "No hay ejercicios agregados todavía.\nHaz clic en '+ Agregar"
              " Ejercicio' para empezar."
          ),
          font=("Arial", 10, "italic"),
      ).pack(pady=20, padx=20)
    else:
      primer_ej = list(ejercicios.keys())[0]
      self.vars_activas_por_rutina[rutina_nombre].set(primer_ej)

      for ej_nombre, ej_info in ejercicios.items():
        self.crear_tarjeta_ejercicio(
            scrollable_frame, rutina_nombre, ej_nombre, ej_info
        )

      # Al crear: solo visible la tarjeta activa, el resto ocultas.
      self._mostrar_solo_activo(rutina_nombre)
      self.actualizar_estado_tarjetas()

  @staticmethod
  def _sonar_alarma():
    # Alarma de ~2s sin bloquear la interfaz.
    try:
      import threading
      try:
        import winsound
      except ImportError:
        return

      def _tocar():
        try:
          import time
          for _ in range(4):
            winsound.Beep(880, 250)
            time.sleep(0.25)
        except Exception:
          pass

      threading.Thread(target=_tocar, daemon=True).start()
    except Exception:
      pass

  def crear_tarjeta_ejercicio(self, parent_frame, rutina_nombre, ejercicio, info):
    # Usamos tk.LabelFrame clásico para permitir cambio dinámico de color de fondo (verde finalizado)
    # Modo individual por ejercicio: 'repes' (Series) o 'segs' (Segundos).
    if info.get("modo") not in ("repes", "segs"):
      info["modo"] = "repes"
    md = self._modo_info(info)
    et_sing, et_plur = md["sing"], md["plur"]
    default_val = md["default_val"]
    unidad = md["unidad"]
    cont_ejercicio = ttk.Frame(parent_frame)
    cont_ejercicio.pack(fill=tk.X, pady=6, padx=5)

    def alternar_colapso():
      ref = self.refs_por_rutina.get(rutina_nombre, {}).get(ejercicio)
      if ref is None:
        return
      if ref.get("colapsado"):
        ref["cuerpo"].pack(fill=tk.X)
        ref["colapsado"] = False
      else:
        ref["cuerpo"].pack_forget()
        ref["colapsado"] = True
      self.actualizar_estado_tarjetas()

    header_frame = ttk.Frame(cont_ejercicio)
    header_frame.pack(fill=tk.X)

    header_name = ttk.Label(
        header_frame, text=ejercicio, font=("Arial", 11, "bold")
    )
    header_name.pack(side=tk.LEFT)

    header_btn = ttk.Button(
        header_frame, text="▼", width=3, command=alternar_colapso
    )
    header_btn.pack(side=tk.LEFT, padx=(6, 0))

    cuerpo = ttk.Frame(cont_ejercicio)
    cuerpo.pack(fill=tk.X)

    card = tk.LabelFrame(
        cuerpo,
        text=f"  {ejercicio}  ",
        font=("Arial", 10, "bold"),
        bg="#f0f0f0",
        padx=10,
        pady=10,
    )
    card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    # Panel lateral de registro (sector aparte): último registro guardado.
    side = ttk.Frame(cuerpo, width=210)
    side.pack(side=tk.RIGHT, fill=tk.Y)
    side.pack_propagate(False)
    side_inner = ttk.LabelFrame(side, text="Registro", padding=8)
    side_inner.pack(fill=tk.BOTH, expand=True)

    reg_fecha = ttk.Label(side_inner, text="Sin registros", font=("Arial", 8, "italic"))
    reg_fecha.pack(anchor=tk.W)
    reg_peso = ttk.Label(side_inner, text="Peso: —", font=("Arial", 9, "bold"))
    reg_peso.pack(anchor=tk.W, pady=(4, 0))
    reg_prom = ttk.Label(side_inner, text="Promedio: —", font=("Arial", 9))
    reg_prom.pack(anchor=tk.W)
    reg_series = ttk.Label(
        side_inner, text=f"{et_plur}: —", font=("Arial", 8), wraplength=185,
        justify=tk.LEFT,
    )
    reg_series.pack(anchor=tk.W, pady=(2, 0))
    reg_aviso = ttk.Label(
        side_inner, text="", font=("Arial", 9, "bold"), foreground="green",
        wraplength=185, justify=tk.LEFT,
    )
    reg_aviso.pack(anchor=tk.W, pady=(6, 0))
    reg_ciclo1 = ttk.Label(side_inner, text="", font=("Arial", 8))
    reg_ciclo1.pack(anchor=tk.W, pady=(4, 0))
    reg_ciclo2 = ttk.Label(side_inner, text="", font=("Arial", 8))
    reg_ciclo2.pack(anchor=tk.W)

    def ver_registros_series():
      win = tk.Toplevel(self.root)
      win.title(f"Registros - {ejercicio}")
      win.geometry("360x320")
      win.resizable(False, False)
      win.grab_set()
      win.update_idletasks()
      rx, ry = self.root.winfo_x(), self.root.winfo_y()
      rw, rh = self.root.winfo_width(), self.root.winfo_height()
      win.geometry(f"360x320+{rx + rw//2 - 180}+{ry + rh//2 - 160}")
      fr = ttk.Frame(win, padding=12)
      fr.pack(fill=tk.BOTH, expand=True)
      ttk.Label(fr, text=f"Registros de {ejercicio} (máx. 4):",
                font=("Arial", 10, "bold")).pack(pady=(0, 8))
      hist = info.get("historial_series", [])
      if not hist:
        ttk.Label(fr, text="Sin registros todavía.",
                  font=("Arial", 9, "italic")).pack(pady=10)
      else:
        _mdv = self._modo_info(info)
        _uplur = _mdv["plur"]
        _vcuni = _mdv["carga_unidad"]
        for reg in reversed(hist):
          repes = reg.get("repes", [])
          ttk.Label(
              fr,
              text=(f"{reg.get('fecha', '—')}  —  {reg.get('peso', 0)} {_vcuni}"
                    f"  —  prom. {reg.get('promedio', 0)}"),
              font=("Arial", 9, "bold"),
          ).pack(anchor=tk.W, pady=(6, 0))
          ttk.Label(
              fr,
              text=(_uplur + ": " + " · ".join(str(r) for r in repes)) if repes else f"{_uplur}: —",
              font=("Arial", 9),
              wraplength=330,
              justify=tk.LEFT,
          ).pack(anchor=tk.W)
      ttk.Button(fr, text="Cerrar", command=win.destroy).pack(pady=10)

    btn_ver_registros = ttk.Button(
        side_inner, text="Ver todos", command=ver_registros_series
    )
    btn_ver_registros.pack(anchor=tk.W, pady=(8, 0))

    def reiniciar_registros():
      # Vuelve los registros a 0 (vacía historial y ciclo congelado).
      if not info.get("historial_series") and not info.get("ciclo_congelado"):
        return
      if messagebox.askyesno(
          "Confirmar",
          f"¿Borrar los registros guardados de '{ejercicio}'? Volverán a 0.",
          parent=self.root,
      ):
        info["historial_series"] = []
        info.pop("ciclo_congelado", None)
        self.guardar_datos_actuales()
        try:
          render_registro()
        except Exception:
          pass

    btn_reiniciar_registros = ttk.Button(
        side_inner, text="Reiniciar registros", command=reiniciar_registros
    )
    btn_reiniciar_registros.pack(anchor=tk.W, pady=(4, 0))

    def render_registro():
      _mdr = self._modo_info(info)
      _plur, _uni = _mdr["plur"], _mdr["unidad"]
      _cnom, _cuni = _mdr["carga_nombre"], _mdr["carga_unidad"]
      hist = info.get("historial_series", [])
      if not hist:
        reg_fecha.config(text="Sin registros")
        reg_peso.config(text=f"{_cnom}: —")
        reg_prom.config(text="Promedio: —")
        reg_series.config(text=f"{_plur}: —")
        reg_aviso.config(text="")
        reg_ciclo1.config(text="")
        reg_ciclo2.config(text="")
        return
      ult = hist[-1]
      repes = ult.get("repes", [])
      reg_fecha.config(text=str(ult.get("fecha", "—")))
      reg_peso.config(text=f"{_cnom}: {ult.get('peso', 0.0)} {_cuni}")
      reg_prom.config(text=f"Promedio: {ult.get('promedio', 0)} {_uni}")
      if repes:
        reg_series.config(text=_plur + ": " + " · ".join(str(r) for r in repes))
      else:
        reg_series.config(text=f"{_plur}: —")
      # Racha actual (registros seguidos al peso más nuevo).
      def _f(x):
        try:
          return "%g" % float(x)
        except Exception:
          return str(x)
      peso_nuevo = hist[-1].get("peso", 0)
      racha = 0
      for r in reversed(hist):
        if r.get("peso", 0) == peso_nuevo:
          racha += 1
        else:
          break
      recs = hist[-racha:] if racha else []
      proms = []
      for r in recs:
        p = r.get("promedio", None)
        if p is None:
          rr = r.get("repes", [])
          p = round(sum(rr) / len(rr), 1) if rr else 0
        proms.append(p)
      prom_total = round(sum(proms) / len(proms), 1) if proms else 0
      # Dato congelado: último ciclo completado (persiste aunque salga del FIFO).
      cong = info.get("ciclo_congelado")
      if cong:
        reg_ciclo1.config(
            text=(f"❄ {_f(cong.get('peso', 0))} {_cuni} — "
                  f"{cong.get('registros', 4)} reg. — prom. {_f(cong.get('promedio', 0))}")
        )
      else:
        reg_ciclo1.config(text="")
      # Dato vivo justo debajo, salvo idéntico al congelado.
      if cong and peso_nuevo == cong.get("peso") and racha == cong.get("registros", 4):
        reg_ciclo2.config(text="")
      else:
        reg_ciclo2.config(
            text=f"• {_f(peso_nuevo)} {_cuni} — {racha} reg. — prom. {_f(prom_total)}"
        )
      # Aviso solo con 4 registros nuevos al peso actual: si el peso cambió,
      # la racha se reinicia y el aviso desaparece hasta juntar 4 nuevos.
      # Repes: 10-12 => 'Aumentar carga'. Segundos: prom >= segundos actuales
      # => 'Aumentar tiempo'.
      if _mdr["es_segs"]:
        try:
          _objetivo = float(info.get("peso_actual", 0) or 0)
        except Exception:
          _objetivo = 0
        if racha == 4 and _objetivo > 0 and prom_total >= _objetivo:
          reg_aviso.config(text=f"⬆ Aumentar tiempo (prom. {_f(prom_total)})")
        else:
          reg_aviso.config(text="")
      elif racha == 4 and 10 <= prom_total <= 12:
        reg_aviso.config(text=f"⬆ Aumentar carga (prom. {_f(prom_total)})")
      else:
        reg_aviso.config(text="")

    top_card_frame = ttk.Frame(card)
    top_card_frame.pack(fill=tk.X, pady=(0, 5))

    rb_seleccionar = ttk.Radiobutton(
        top_card_frame,
        text="Ejercicio Activo",
        variable=self.vars_activas_por_rutina[rutina_nombre],
        value=ejercicio,
        command=lambda r=rutina_nombre, ej=ejercicio: self._seleccionar_ejercicio(r, ej),
    )
    rb_seleccionar.pack(side=tk.LEFT)

    info_frame = ttk.Frame(top_card_frame)
    info_frame.pack(side=tk.RIGHT)
    obj_val = info.get('repes', '20' if md['es_segs'] else '10-12')
    obj_unit = 'segundos' if md['es_segs'] else 'repeticiones'
    lbl_info_descanso = ttk.Label(
        info_frame,
        text=(
            f"Objetivo: {obj_val} {obj_unit}  |  Descanso:"
            f" {info.get('descanso', 120)}s"
        ),
        font=("Arial", 9, "italic"),
    )
    lbl_info_descanso.pack()
    lbl_contador = ttk.Label(info_frame, text=f"0/{int(info.get('series', 3))}",
                             font=("Arial", 10, "bold"))
    lbl_contador.pack()

    # Botón individual por ejercicio para cambiar Series <-> Segundos.
    modo_frame = ttk.Frame(card)
    modo_frame.pack(fill=tk.X, pady=(0, 2))
    btn_modo_txt = (
        "⏱ Modo: Segundos → cambiar a Series"
        if md["es_segs"] else "⏱ Modo: Series → cambiar a Segundos"
    )
    btn_modo = ttk.Button(
        modo_frame, text=btn_modo_txt,
        command=lambda r=rutina_nombre, ej=ejercicio: self._toggle_modo(r, ej),
    )
    btn_modo.pack(anchor=tk.W)

    # Sin fill=X: el bloque (series + contadores + botones) queda centrado.
    series_frame = ttk.Frame(card)
    series_frame.pack(pady=4)
    num_series = int(info.get("series", 3))
    series_hechas = []
    marca_labels = []
    reps_widgets = []

    # Base por defecto para el reset (quitar series agregadas de más).
    defecto_global = int(
        self.datos_perfil.get("configuracion_default", {}).get("series", 3)
    )
    if "series_base" in info:
      base_series = int(info["series_base"])
    else:
      base_series = min(num_series, defecto_global)
      info["series_base"] = base_series
    if base_series > num_series:
      base_series = num_series

    for i in range(num_series):
      lb = ttk.Label(series_frame, text=f"○ {et_sing} {i+1}", font=("Arial", 10))
      lb.grid(row=0, column=i, padx=5, pady=2)
      marca_labels.append(lb)
      sp_reps = ttk.Spinbox(series_frame, from_=0, to=200, width=5)
      sp_reps.set(default_val)
      sp_reps.grid(row=1, column=i, padx=5, pady=2)
      reps_widgets.append(sp_reps)
      series_hechas.append(False)

    # Restaurar finalizado del mismo día (persiste al cerrar/abrir).
    # Día distinto => arranca reiniciado.
    _fin_hoy, _vals_hoy = self._sesion_finalizada_hoy(info, num_series)
    if _fin_hoy:
      for i in range(num_series):
        series_hechas[i] = True
        try:
          marca_labels[i].config(text=f"✔ {et_sing} {i+1}", foreground="green")
        except Exception:
          pass
        try:
          reps_widgets[i].set(_vals_hoy[i])
        except Exception:
          pass

    def finalizar_siguiente_serie():
      # Marca 1 a 1 la primera serie pendiente: palomita + bloquea sus repes.
      # Última serie: sin crono, finaliza el ejercicio y avanza.
      try:
        self.vars_activas_por_rutina[rutina_nombre].set(ejercicio)
      except Exception:
        pass
      if all(series_hechas):
        return
      idx = next(i for i, h in enumerate(series_hechas) if not h)
      series_hechas[idx] = True
      try:
        marca_labels[idx].config(text=f"✔ {et_sing} {idx+1}", foreground="green")
      except Exception:
        pass
      try:
        reps_widgets[idx].config(state="disabled")
      except Exception:
        pass
      if all(series_hechas):
        try:
          detener_crono()
        except Exception:
          pass
        # Guardar registro de la sesión (fecha, peso, repes, promedio).
        try:
          hoy = datetime.now().strftime("%Y-%m-%d")
          repes_vals = []
          for sp in reps_widgets:
            try:
              repes_vals.append(int(float(sp.get())))
            except Exception:
              repes_vals.append(0)
          prom = round(sum(repes_vals) / len(repes_vals), 1) if repes_vals else 0
          reg = {
              "fecha": hoy,
              "peso": info.get("peso_actual", 0.0),
              "repes": repes_vals,
              "promedio": prom,
          }
          hist_s = info.setdefault("historial_series", [])
          hist_s.append(reg)
          while len(hist_s) > 4:
            hist_s.pop(0)
          self._actualizar_ciclo_congelado(info)
          # Persistir finalizado del día (sobrevive a cerrar la app).
          try:
            self._marcar_sesion_finalizada(info, repes_vals)
          except Exception:
            pass
          self.guardar_datos_actuales()
        except Exception:
          pass
        try:
          render_registro()
        except Exception:
          pass
      else:
        try:
          iniciar_crono()
        except Exception:
          pass
      self.comprobar_y_avanzar_ejercicio(rutina_nombre, ejercicio)

    def agregar_serie():
      if len(series_hechas) >= 6:
        messagebox.showwarning(
            "Límite", f"Máximo 6 {et_plur.lower()} por ejercicio."
        )
        return
      # Seleccionar este ejercicio: la nueva serie debe quedar editable.
      try:
        self.vars_activas_por_rutina[rutina_nombre].set(ejercicio)
      except Exception:
        pass
      n = len(series_hechas)
      lb = ttk.Label(series_frame, text=f"○ {et_sing} {n+1}", font=("Arial", 10))
      lb.grid(row=0, column=n, padx=5, pady=2)
      sp_nueva = ttk.Spinbox(series_frame, from_=0, to=200, width=5)
      sp_nueva.set(default_val)
      sp_nueva.grid(row=1, column=n, padx=5, pady=2)
      marca_labels.append(lb)
      reps_widgets.append(sp_nueva)
      series_hechas.append(False)
      btns_series_frame.grid_configure(columnspan=n + 1)
      info["series"] = len(series_hechas)
      # Ya no está finalizado (3/3 -> 3/4): limpiar sesión persistida.
      try:
        if self._limpiar_sesion(info):
          pass
      except Exception:
        pass
      self.guardar_datos_actuales()
      # Refresca contador (ej. 3/3 -> 3/4 y sale de FINALIZADO) y bloqueo.
      self.comprobar_y_avanzar_ejercicio(rutina_nombre, ejercicio)

    def _reset_nucleo():
      # Reinicio mecánico sin snapshot ni confirmación (lo usa también
      # el reinicio de rutina). No toca registros ni pesos.
      # Sí limpia la sesión finalizada persistida (reset manual).
      try:
        detener_crono()
      except Exception:
        pass
      _sesion_limpiada = False
      try:
        _sesion_limpiada = self._limpiar_sesion(info)
      except Exception:
        pass
      if len(series_hechas) > base_series:
        for w_extra in marca_labels[base_series:] + reps_widgets[base_series:]:
          try:
            w_extra.destroy()
          except Exception:
            pass
        del marca_labels[base_series:]
        del reps_widgets[base_series:]
        del series_hechas[base_series:]
        info["series"] = base_series
        self.guardar_datos_actuales()
        try:
          btns_series_frame.grid_configure(columnspan=base_series)
        except Exception:
          pass
      for i in range(len(series_hechas)):
        series_hechas[i] = False
        try:
          marca_labels[i].config(text=f"○ {et_sing} {i+1}", foreground="")
        except Exception:
          pass
      for sp in reps_widgets:
        try:
          sp.config(state="normal")
        except Exception:
          pass
        try:
          sp.set(default_val)
        except Exception:
          pass
      if _sesion_limpiada:
        try:
          self.guardar_datos_actuales()
        except Exception:
          pass
      self.comprobar_y_avanzar_ejercicio(rutina_nombre, ejercicio)

    def restablecer_ejercicio():
      # Vuelve al valor por defecto: recorta series agregadas de más,
      # quita palomitas, repes/segs al valor base, crono en 00:00, sin FINALIZADO.
      # No toca el peso.
      if not all(series_hechas):
        if not messagebox.askyesno(
            "Reiniciar ejercicio",
            "El ejercicio no está finalizado. ¿Seguro de reiniciarlo?\n"
            "Se guardará lo hecho y el resto en 0.",
            parent=self.root,
        ):
          return
      try:
        self.vars_activas_por_rutina[rutina_nombre].set(ejercicio)
      except Exception:
        pass
      # Snapshot al registro lateral (FIFO máx. 4) antes de reiniciar.
      # Solo si hay algo hecho (series o repes), para no guardar ceros.
      try:
        def _rep(sp):
          try:
            return int(float(sp.get()))
          except Exception:
            return 0
        repes_crudas = [_rep(sp) for sp in reps_widgets]
        # Si ya estaba finalizado, el registro se guardó al completar:
        # no duplicar, solo reiniciar. Tampoco guardar si está intacto
        # (nada hecho y valores en el valor por defecto).
        if not all(series_hechas) and (
            any(series_hechas) or any(r != default_val for r in repes_crudas)
        ):
          # Hechas conservan sus repes; pendientes se guardan en 0.
          repes_vals = [
              r if h else 0 for r, h in zip(repes_crudas, series_hechas)
          ]
          hoy_r = datetime.now().strftime("%Y-%m-%d")
          prom_r = round(sum(repes_vals) / len(repes_vals), 1) if repes_vals else 0
          hist_r = info.setdefault("historial_series", [])
          hist_r.append({
              "fecha": hoy_r,
              "peso": info.get("peso_actual", 0.0),
              "repes": repes_vals,
              "promedio": prom_r,
          })
          while len(hist_r) > 4:
            hist_r.pop(0)
          self._actualizar_ciclo_congelado(info)
          self.guardar_datos_actuales()
          render_registro()
      except Exception:
        pass
      _reset_nucleo()

    # Fila centrada con los botones de series (debajo de marcas y repes).
    btns_series_frame = ttk.Frame(series_frame)
    btns_series_frame.grid(row=2, column=0, columnspan=num_series, pady=4)

    btn_mas_serie = ttk.Button(
        btns_series_frame, text=f"+ {et_sing}", width=10, command=agregar_serie
    )
    btn_mas_serie.pack(side=tk.LEFT, padx=5)
    btn_reset_estado = ttk.Button(
        btns_series_frame, text="\u21bb", width=3, command=restablecer_ejercicio
    )
    btn_reset_estado.pack(side=tk.LEFT, padx=5)

    crono_frame = ttk.Frame(card)
    crono_frame.pack(fill=tk.X, pady=4)

    descanso_seg = int(info.get("descanso", 120))

    lbl_crono = ttk.Label(
        crono_frame,
        text=f"{descanso_seg // 60:02d}:{descanso_seg % 60:02d}",
        font=("Courier", 16, "bold"),
    )
    lbl_crono.pack(pady=(2, 4))

    crono_btns = ttk.Frame(crono_frame)
    crono_btns.pack()

    crono_data = {"tiempo_restante": descanso_seg, "id": None}

    def actualizar_timer():
      if crono_data["tiempo_restante"] > 0:
        mins, secs = divmod(crono_data["tiempo_restante"], 60)
        lbl_crono.config(text=f"{mins:02d}:{secs:02d}")
        crono_data["tiempo_restante"] -= 1
        crono_data["id"] = self.root.after(1000, actualizar_timer)
      else:
        lbl_crono.config(text="¡Tiempo!")
        self._sonar_alarma()
        messagebox.showinfo(
            "Descanso", f"¡Terminó el descanso para {ejercicio}!"
        )

    def iniciar_crono():
      if crono_data["id"] is not None:
        self.root.after_cancel(crono_data["id"])
      crono_data["tiempo_restante"] = descanso_seg
      actualizar_timer()

    def detener_crono():
      if crono_data["id"] is not None:
        self.root.after_cancel(crono_data["id"])
        crono_data["id"] = None
      lbl_crono.config(text=f"{descanso_seg // 60:02d}:{descanso_seg % 60:02d}")
      crono_data["tiempo_restante"] = descanso_seg

    btn_iniciar = ttk.Button(
        crono_btns, text="Iniciar Descanso", command=iniciar_crono
    )
    btn_iniciar.pack(side=tk.LEFT, padx=3)

    btn_reset = ttk.Button(
        crono_btns, text="Reiniciar", command=detener_crono
    )
    btn_reset.pack(side=tk.LEFT, padx=3)

    def cambiar_tiempo():
      nonlocal descanso_seg
      win = tk.Toplevel(self.root)
      win.title(f"Tiempo de descanso - {ejercicio}")
      win.geometry("260x170")
      win.resizable(False, False)
      win.grab_set()
      win.update_idletasks()
      rx, ry = self.root.winfo_x(), self.root.winfo_y()
      rw, rh = self.root.winfo_width(), self.root.winfo_height()
      win.geometry(f"260x170+{rx + rw//2 - 130}+{ry + rh//2 - 85}")
      fr = ttk.Frame(win, padding=12)
      fr.pack(fill=tk.BOTH, expand=True)
      ttk.Label(fr, text="Minutos:").grid(row=0, column=0, sticky=tk.W, pady=3)
      sp_min = ttk.Spinbox(fr, from_=0, to=59, width=5)
      sp_min.set(descanso_seg // 60)
      sp_min.grid(row=0, column=1, padx=5, pady=3)
      ttk.Label(fr, text="Segundos:").grid(row=1, column=0, sticky=tk.W, pady=3)
      sp_seg = ttk.Spinbox(fr, from_=0, to=59, width=5)
      sp_seg.set(descanso_seg % 60)
      sp_seg.grid(row=1, column=1, padx=5, pady=3)

      def aplicar():
        nonlocal descanso_seg
        try:
          total = int(sp_min.get()) * 60 + int(sp_seg.get())
        except ValueError:
          messagebox.showerror(
              "Error", "Minutos y segundos deben ser números.", parent=win
          )
          return
        if total <= 0:
          messagebox.showerror(
              "Error", "El tiempo debe ser mayor a 0.", parent=win
          )
          return
        descanso_seg = total
        info["descanso"] = total
        self.guardar_datos_actuales()
        try:
          detener_crono()
        except Exception:
          pass
        try:
          _mda = self._modo_info(info)
          _obju = 'segundos' if _mda['es_segs'] else 'repeticiones'
          lbl_info_descanso.config(
              text=(f"Objetivo: {info.get('repes', '10-12')} {_obju}  |"
                    f" Descanso: {total}s")
          )
        except Exception:
          pass
        win.destroy()

      ttk.Button(fr, text="Aceptar", command=aplicar).grid(
          row=2, column=0, columnspan=2, pady=10
      )

    btn_tiempo = ttk.Button(
        crono_btns, text="Cambiar tiempo", command=cambiar_tiempo
    )
    btn_tiempo.pack(side=tk.LEFT, padx=3)

    btn_finalizar = ttk.Button(
        card, text="Finalizar serie", command=finalizar_siguiente_serie,
        padding=(12, 6),
    )
    btn_finalizar.pack(fill=tk.X, pady=5)

    peso_frame = ttk.Frame(card)
    peso_frame.pack(fill=tk.X, pady=4)

    ttk.Label(peso_frame, text=md["carga_titulo"]).pack(
        side=tk.LEFT, padx=(0, 5)
    )
    ent_peso = ttk.Entry(peso_frame, width=8)
    ent_peso.insert(0, str(info.get("peso_actual", 0.0)))
    ent_peso.pack(side=tk.LEFT, padx=5)

    fecha_ult = info.get("fecha_ultima", "Nunca")
    lbl_fecha_peso = ttk.Label(
        peso_frame,
        text=f"({fecha_ult[:10] if fecha_ult != 'Nunca' else '—'})",
        font=("Arial", 8, "italic"),
    )
    lbl_fecha_peso.pack(side=tk.LEFT, padx=2)

    peso_anterior = info.get("peso_anterior", 0.0)
    fecha_ultima = info.get("fecha_ultima", "Nunca")

    def texto_historial(anterior, fecha):
      _hm = self._modo_info(info)
      _hu = _hm["carga_unidad"]
      ant_txt = "—" if (anterior in (0, 0.0, None, "") and fecha == "Nunca") else f"{anterior} {_hu}"
      return f"Anterior: {ant_txt}  |  Última vez: {fecha}"

    peso_hist_frame = ttk.Frame(card)
    peso_hist_frame.pack(fill=tk.X, pady=(0, 5))

    lbl_historial = ttk.Label(
        peso_hist_frame,
        text=texto_historial(peso_anterior, fecha_ultima),
        font=("Arial", 8, "italic"),
    )
    lbl_historial.pack(side=tk.LEFT, padx=2)

    def guardar_peso():
      _gm = self._modo_info(info)
      _gnom, _gu = _gm["carga_nombre"], _gm["carga_unidad"]
      try:
        nuevo_peso = float(ent_peso.get())
      except ValueError:
        messagebox.showerror(
            "Error", f"Ingresa un valor numérico válido para {_gnom.lower()}."
        )
        return
      if nuevo_peso < 0:
        messagebox.showerror("Error", f"{_gnom} no puede ser negativo.")
        return

      actual_peso = info.get("peso_actual", 0.0)
      hoy = datetime.now().strftime("%Y-%m-%d")
      fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")

      info["peso_anterior"] = actual_peso
      info["peso_actual"] = nuevo_peso
      info["fecha_ultima"] = fecha_actual

      self.guardar_datos_actuales()
      # Actualizar etiquetas en el lugar: sin rebuild (conserva marcas, tab y avance).
      try:
        lbl_historial.config(text=texto_historial(actual_peso, fecha_actual))
        lbl_fecha_peso.config(text=f"({hoy})")
      except Exception:
        pass
      messagebox.showinfo(
          "Guardado",
          f"¡Progreso guardado para {ejercicio}!\nNuevo: {nuevo_peso}"
          f" {_gu}\nAnterior: {actual_peso} {_gu}",
      )

    btn_guardar_peso = ttk.Button(
        peso_frame, text=md["carga_boton"], command=guardar_peso
    )
    btn_guardar_peso.pack(side=tk.RIGHT, padx=5)

    btn_eliminar = ttk.Button(
        card,
        text="🗑 Eliminar Ejercicio",
        command=lambda: self.eliminar_ejercicio(rutina_nombre, ejercicio),
    )
    btn_eliminar.pack(anchor=tk.E, pady=2)

    render_registro()

    self.refs_por_rutina[rutina_nombre][ejercicio] = {
        "series_hechas": series_hechas,
        "marca_labels": marca_labels,
        "reps_widgets": reps_widgets,
        "iniciar_crono_func": iniciar_crono,
        "detener_crono_func": detener_crono,
        "card_frame": card,
        "base_title": ejercicio,
        "lbl_contador": lbl_contador,
        "btn_iniciar": btn_iniciar,
        "btn_reset": btn_reset,
        "btn_tiempo": btn_tiempo,
        "ent_peso": ent_peso,
        "btn_guardar_peso": btn_guardar_peso,
        "btn_mas_serie": btn_mas_serie,
        "btn_reset_estado": btn_reset_estado,
        "btn_finalizar": btn_finalizar,
        "btn_modo": btn_modo,
        "et_sing": et_sing,
        "et_plur": et_plur,
        "modo": info.get("modo", "repes"),
        "reset_nucleo": _reset_nucleo,
        "cuerpo": cuerpo,
        "header_name": header_name,
        "header_btn": header_btn,
        "colapsado": False,
        "alternar": alternar_colapso,
    }

  def reiniciar_rutina(self, rutina_nombre):
    # Reinicia todos los ejercicios de la pestaña sin borrar registros ni pesos.
    refs_rutina = self.refs_por_rutina.get(rutina_nombre, {})
    if not refs_rutina:
      return
    if not messagebox.askyesno(
        "Reiniciar rutina",
        f"¿Reiniciar todos los ejercicios de '{rutina_nombre}'?\n"
        "Se conservan registros y pesos.",
        parent=self.root,
    ):
      return
    for ref in refs_rutina.values():
      try:
        ref["reset_nucleo"]()
      except Exception:
        pass
    try:
      primero = next(iter(refs_rutina))
      self.vars_activas_por_rutina[rutina_nombre].set(primero)
      self._mostrar_solo_activo(rutina_nombre)
    except Exception:
      pass
    self.actualizar_estado_tarjetas()

  def _mostrar_solo_activo(self, rutina_nombre):
    # Oculta todas salvo la activa (las otras se pueden desplegar a mano).
    var = self.vars_activas_por_rutina.get(rutina_nombre)
    activo = var.get() if var is not None else ""
    for ej, ref in self.refs_por_rutina.get(rutina_nombre, {}).items():
      try:
        if ej == activo:
          if ref.get("colapsado"):
            ref["cuerpo"].pack(fill=tk.X)
            ref["colapsado"] = False
        else:
          if not ref.get("colapsado"):
            ref["cuerpo"].pack_forget()
            ref["colapsado"] = True
      except Exception:
        pass

  def _seleccionar_ejercicio(self, rutina_nombre, ej_nombre):
    try:
      self._mostrar_solo_activo(rutina_nombre)
    except Exception:
      pass
    self.actualizar_estado_tarjetas()

  def actualizar_estado_tarjetas(self):
    rutina_activa = self._rutina_activa()
    for rutina_nombre, refs_rutina in self.refs_por_rutina.items():
      var_activa = self.vars_activas_por_rutina.get(rutina_nombre)
      ej_activo = var_activa.get() if var_activa is not None else ""
      for ej_nombre, refs in refs_rutina.items():
        hechas = refs["series_hechas"]
        marcadas = sum(1 for h in hechas if h)
        total = len(hechas)
        finalizado = total > 0 and marcadas == total
        es_activo = (
            rutina_nombre == rutina_activa and ej_nombre == ej_activo
        )

        # Contador + color/título según finalizado (verde + FINALIZADO).
        try:
          refs["lbl_contador"].config(text=f"{marcadas}/{total}")
        except Exception:
          pass
        try:
          if finalizado:
            refs["card_frame"].config(
                bg="#d4edda",
                text=f"  {refs['base_title']}  —  FINALIZADO ✔  ",
            )
          else:
            refs["card_frame"].config(
                bg="#f0f0f0", text=f"  {refs['base_title']}  "
            )
        except Exception:
          pass

        # Marcas visuales por serie: ✔ verde o ○ pendiente.
        _et = refs.get("et_sing", "Serie")
        for i, lb in enumerate(refs.get("marca_labels", [])):
          try:
            if hechas[i]:
              lb.config(text=f"✔ {_et} {i+1}", foreground="green")
            else:
              lb.config(text=f"○ {_et} {i+1}", foreground="")
          except Exception:
            pass

        # Encabezado colapsable: nombre + avance + tilde si finalizó.
        try:
          refs["header_btn"].config(
              text="▶" if refs.get("colapsado") else "▼"
          )
          marca_fin = " ✔" if finalizado else ""
          refs["header_name"].config(
              text=f"{ej_nombre} ({marcadas}/{total}){marca_fin}"
          )
        except Exception:
          pass

        if finalizado:
          # Todo bloqueado salvo peso y botones de series.
          for w in refs.get("reps_widgets", []):
            try:
              w.config(state="disabled")
            except Exception:
              pass
          for key in ("btn_iniciar", "btn_reset", "btn_tiempo", "btn_finalizar"):
            try:
              refs[key].config(state="disabled")
            except Exception:
              pass
          for key in ("ent_peso", "btn_guardar_peso"):
            try:
              refs[key].config(state="normal")
            except Exception:
              pass
        else:
          estado = "normal" if es_activo else "disabled"
          for key in (
              "btn_iniciar",
              "btn_reset",
              "btn_tiempo",
              "btn_finalizar",
              "ent_peso",
              "btn_guardar_peso",
          ):
            try:
              refs[key].config(state=estado)
            except Exception:
              pass
          # Repes: solo editables las series pendientes del activo.
          for i, sp in enumerate(refs.get("reps_widgets", [])):
            try:
              if es_activo and not hechas[i]:
                sp.config(state="normal")
              else:
                sp.config(state="disabled")
            except Exception:
              pass
        # + Serie y ↻ siempre habilitados.

  def agregar_ejercicio(self, rutina_nombre):
    nombre = simpledialog.askstring(
        "Nuevo Ejercicio",
        f"Ingresa el nombre del ejercicio para '{rutina_nombre}':",
    )
    if nombre:
      nombre = nombre.strip()
      ejercicios_rutina = self.datos_perfil["rutinas"][rutina_nombre]
      if nombre in ejercicios_rutina:
        messagebox.showerror(
            "Error", "Ese ejercicio ya existe en esta rutina."
        )
        return

      defaults = self.datos_perfil.get(
          "configuracion_default", {"series": 3, "repes": "10-12", "descanso": 120}
      )

      ejercicios_rutina[nombre] = {
          "series": defaults["series"],
          "series_base": defaults["series"],
          "repes": defaults["repes"],
          "descanso": defaults["descanso"],
          "modo": "repes",
          "peso_actual": 0.0,
          "peso_anterior": 0.0,
          "fecha_ultima": "Nunca",
      }
      self.guardar_datos_actuales()
      self.iniciar_interfaz_principal()

  def eliminar_ejercicio(self, rutina_nombre, ejercicio):
    if messagebox.askyesno(
        "Confirmar",
        f"¿Estás seguro de eliminar '{ejercicio}' de {rutina_nombre}?",
    ):
      del self.datos_perfil["rutinas"][rutina_nombre][ejercicio]
      self.guardar_datos_actuales()
      self.iniciar_interfaz_principal()

if __name__ == "__main__":
  root = tk.Tk()
  app = AppEntrenamiento(root)
  root.mainloop()