import pyodbc
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QTableWidgetItem
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt

from Diseño_Interfaces.CargaMaterias import CargaMaterias


class CargaMateriasLogic(CargaMaterias):
    """
    Esta clase controla TODO el sistema de carga de materias.
    Aquí se maneja:
    - Lectura de materias disponibles
    - Carga por paquete
    - Paquetes personalizados
    - Reprobadas
    - Adelantables
    - Choques de horario
    - Registro en BD
    """

    MAX_PKG_SIZE = 6
    MAX_PERSONALIZED = 4

    def __init__(self, num_control):
        super().__init__()
        self.num_control = num_control
        self.selecciones = {}        
        self.horario_ocupado = set() 
        self.personalizados = []     

        # conexion de los botones a sus funciones
        self.tree_materias.itemClicked.connect(self._on_tree_item_clicked)
        self.btn_limpiar.clicked.connect(self.limpiar_todo)
        self.btn_eliminar_carga.clicked.connect(self.eliminar_carga_bd)
        self.btn_finalizar.clicked.connect(self.finalizar_carga)

        self.cargar_materias_disponibles()

    # conexion a la base de datos
    def conectar(self):
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=tcp:localhost,1433;'
            'DATABASE=PruebaDB;'
            'Trusted_Connection=yes;'
        )

    # carga
    def cargar_materias_disponibles(self):
        #es el panel izquierdo con las opciones de paquetes
        # materias adelantables, reprobadas etc
        conn = self.conectar()
        cur = conn.cursor()

        # semestre del alumno (tomando este dato sabemos que matereias debe cursar)
        cur.execute("SELECT Semestre FROM Alumnos WHERE Num_control=?", (self.num_control,))
        row = cur.fetchone()
        if not row:
            return
        semestre = row[0]

        # periodo activo
        cur.execute("SELECT Id_periodo FROM Periodos WHERE Activo=1")
        periodo_id = cur.fetchone()[0]

        # extraemos las materias reprobadas del alumno mediante
        # el kardex que estan registradas como REPROBADA
        cur.execute("""
            SELECT m.Serie, m.Nombre, m.Creditos
            FROM Kardex k JOIN Materias m ON k.Serie=m.Serie
            WHERE k.Num_control=? AND k.Estatus='REPROBADA'
        """, (self.num_control,))
        materias_rep = cur.fetchall()

        self.tree_materias.clear()
        self.personalizados = []

        # Paquete regular
        nodo_paq = self._crear_nodo("PAQUETES", "#cfe9ff")
        materias_semestre = self._get_materias_semestre(cur, semestre)

        paquetes = self._separar_paquetes(materias_semestre)

        for letra, lista in paquetes.items():
            item_paq = self._crear_item_paquete(letra, nodo_paq)
            for serie, nombre in lista:
                hora_txt = self._hora_representativa(cur, serie, letra, periodo_id)
                sub = QTreeWidgetItem([f"   • {serie} - {nombre} — {hora_txt}"])
                sub.setFlags(sub.flags() & ~Qt.ItemIsSelectable)
                item_paq.addChild(sub)

        # paquetes personalizados
        if materias_rep:
            objetivo = self._armar_objetivo(cur, semestre, materias_rep)
            paquetes_personalizados = self._generar_paquetes_personalizados(objetivo, periodo_id, cur)

            if paquetes_personalizados:
                nodo_pers = self._crear_nodo("PAQUETES PERSONALIZADOS", "#ffd7a6")
                self.personalizados = paquetes_personalizados

                for i, paquete in enumerate(paquetes_personalizados):
                    letra_pers = chr(ord("A") + i)
                    nodo = QTreeWidgetItem([f"Paquete Personalizado {letra_pers}"])
                    nodo.setData(0, Qt.UserRole, f"PAQUETE:PERS_IDX:{i}")
                    nodo.setBackground(0, QColor("#ffcc99"))
                    nodo_pers.addChild(nodo)

                    for serie, nombre, grp, horas in paquete['detalle']:
                        txt = f"   • {serie} - {nombre} → Grupo {grp} — {horas}"
                        sub = QTreeWidgetItem([txt])
                        sub.setFlags(sub.flags() & ~Qt.ItemIsSelectable)
                        nodo.addChild(sub)

        # mostrara en el panel las materias que reprobo con sus opciones de
        # grupos y horario
        if materias_rep:
            nodo_rep = self._crear_nodo("MATERIAS REPROBADAS", "#ffe0e0")
            for serie, nombre, cred in materias_rep:
                item = QTreeWidgetItem([f"{serie} - {nombre} ({cred} créditos)"])
                item.setBackground(0, QColor("#ffd9d9"))
                nodo_rep.addChild(item)
                self._insertar_grupos(cur, item, serie, periodo_id)

        # panel izquierdo donde extraemos de la base de datos las materias que deberia
        # cursar el alumno
        cur.execute("""
            SELECT Serie, Nombre, Creditos
            FROM Materias
            WHERE Semestre=? 
              AND (Seriada IS NULL OR Seriada IN (
                     SELECT Serie FROM Kardex WHERE Num_control=? AND Estatus='APROBADA'
                  ))
              AND Serie NOT IN (
                     SELECT Serie FROM Kardex 
                     WHERE Num_control=? AND (Estatus='APROBADA' OR Estatus='CURSANDO')
                  )
            ORDER BY Serie
        """, (semestre, self.num_control, self.num_control))
        materias_sem = cur.fetchall()

        if materias_sem:
            nodo_sem = self._crear_nodo("MATERIAS DEL SEMESTRE", "#e7ffe7")
            for serie, nombre, cred in materias_sem:
                item = QTreeWidgetItem([f"{serie} - {nombre} ({cred} créditos)"])
                nodo_sem.addChild(item)
                self._insertar_grupos(cur, item, serie, periodo_id)

        # un poco de lo mismo en el panel izquierdo aqui se mostraran la materias
        # que el alumno puede adelantar osea que no necesitan estar seriadas
        cur.execute("""
            SELECT Serie, Nombre, Creditos
            FROM Materias
            WHERE Semestre>? 
              AND Seriada IS NULL
              AND Serie NOT IN (
                SELECT Serie FROM Kardex WHERE Num_control=?
              )
            ORDER BY Semestre, Serie
        """, (semestre, self.num_control))
        adelantables = cur.fetchall()

        if adelantables:
            nodo_ad = self._crear_nodo("MATERIAS ADELANTABLES", "#fff4ce")
            for serie, nombre, cred in adelantables:
                item = QTreeWidgetItem([f"{serie} - {nombre} ({cred} créditos)"])
                nodo_ad.addChild(item)
                self._insertar_grupos(cur, item, serie, periodo_id)

        conn.close()
    
    def _crear_nodo(self, texto, color):
        nodo = QTreeWidgetItem([texto])
        nodo.setBackground(0, QColor(color))
        f = QFont(); f.setBold(True)
        nodo.setFont(0, f)
        self.tree_materias.addTopLevelItem(nodo)
        return nodo

    def _crear_item_paquete(self, letra, nodo):
        item = QTreeWidgetItem([f"Paquete {letra}"])
        item.setData(0, Qt.UserRole, f"PAQUETE:{letra}")
        item.setBackground(0, QColor("#b3e5fc"))
        nodo.addChild(item)
        return item

    def _hora_representativa(self, cur, serie, letra, periodo_id):
        cur.execute("""
            SELECT TOP 1 Hora_inicio, Hora_fin
            FROM Grupos g JOIN Horario_Grupo h ON g.Id_grupo=h.Id_grupo
            WHERE Serie_materia=? AND Grupo_letra=? AND Id_periodo=?
            ORDER BY Hora_inicio
        """, (serie, letra, periodo_id))
        r = cur.fetchone()
        if not r:
            return "--:--"
        try:
            return f"{r[0].strftime('%H:%M')}–{r[1].strftime('%H:%M')}"
        except:
            return "--:--"

    def _get_materias_semestre(self, cur, semestre):
        cur.execute("SELECT Serie, Nombre FROM Materias WHERE Semestre=? ORDER BY Serie", (semestre,))
        return cur.fetchall()

    def _separar_paquetes(self, materias):
        """
        Divide las materias de semestre en 4 paquetes de máximo 6 materias.
        """
        paq = {"A": [], "B": [], "C": [], "D": []}
        for i, row in enumerate(materias):
            idx = (i // 6)
            letra = ["A", "B", "C", "D"][min(idx, 3)]
            paq[letra].append(row)
        return paq

    def _insertar_grupos(self, cur, item_mat, serie, periodo_id):
        """Inserta los grupos y el horario dentro de un item de materia."""
        cur.execute("""
            SELECT Id_grupo, Grupo_letra, Cupo_actual, Cupo_maximo
            FROM Grupos
            WHERE Serie_materia=? AND Id_periodo=?
            ORDER BY Grupo_letra
        """, (serie, periodo_id))

        for idg, letra, cup_a, cup_m in cur.fetchall():

            hora_txt = self._hora_representativa(cur, serie, letra, periodo_id)
            item_grupo = QTreeWidgetItem([f"   Grupo {letra} → {cup_a}/{cup_m} {hora_txt}"])
            item_grupo.setData(0, Qt.UserRole, idg)
            item_mat.addChild(item_grupo)

            # detalles del horario
            cur.execute("""
                SELECT Dia_semana, Hora_inicio, Hora_fin
                FROM Horario_Grupo
                WHERE Id_grupo=?
                ORDER BY CASE Dia_semana
                    WHEN 'Lunes' THEN 1 WHEN 'Martes' THEN 2 WHEN 'Miércoles' THEN 3
                    WHEN 'Jueves' THEN 4 WHEN 'Viernes' THEN 5 END, Hora_inicio
            """, (idg,))
            for dia, ini, fin in cur.fetchall():
                QTreeWidgetItem(item_grupo, [
                    f"      • {dia} {ini.strftime('%H:%M')} - {fin.strftime('%H:%M')}"
                ])

    #
    # GENERAR PAQUETES PERSONALIZADOS
    def _armar_objetivo(self, cur, semestre, materias_rep):
        """Arma la lista de materias objetivo (reprobadas + semestre)."""
        # como prioridad las reprobadas primero
        objetivo = [s[0] for s in materias_rep]  

        # materias que sí puede cursar del semestre
        cur.execute("""
            SELECT Serie
            FROM Materias
            WHERE Semestre=?
              AND (Seriada IS NULL OR Seriada IN (
                   SELECT Serie FROM Kardex WHERE Num_control=? AND Estatus='APROBADA'
              ))
              AND Serie NOT IN (
                SELECT Serie FROM Kardex 
                WHERE Num_control=? AND (Estatus='APROBADA' OR Estatus='CURSANDO')
              )
            ORDER BY Serie
        """, (semestre, self.num_control, self.num_control))

        for serie, in cur.fetchall():
            if len(objetivo) < self.MAX_PKG_SIZE and serie not in objetivo:
                objetivo.append(serie)

        return objetivo

    def _generar_paquetes_personalizados(self, objetivo_series, periodo_id, cur):
        """
        Aquí se hace la magia:
        - Revisamos todos los grupos disponibles por materia
        - Intentamos combinarlos sin choques
        - Solo generamos hasta 4 soluciones
        """

        # obtener opciones de cada materia
        opciones = {}
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

        for serie in objetivo_series:
            cur.execute("""
                SELECT Id_grupo, Grupo_letra, Cupo_actual, Cupo_maximo
                FROM Grupos
                WHERE Serie_materia=? AND Id_periodo=?
                ORDER BY Grupo_letra
            """, (serie, periodo_id))

            opciones[serie] = []
            for idg, letra, cup_a, cup_m in cur.fetchall():
                # sacamos horarios del grupo
                cur.execute("""
                    SELECT Dia_semana, Hora_inicio, Hora_fin
                    FROM Horario_Grupo
                    WHERE Id_grupo=?
                """, (idg,))
                horarios = cur.fetchall()

                celdas = []
                horas_txt = []
                valido = True

                for dia, ini, fin in horarios:
                    if dia not in dias:
                        valido = False
                        break

                    fila = ini.hour - 7
                    if fila < 0 or fila >= 15:
                        valido = False
                        break

                    col = dias.index(dia) + 1
                    celdas.append((fila, col))
                    horas_txt.append(f"{dia} {ini.strftime('%H:%M')}-{fin.strftime('%H:%M')}")

                if not valido:
                    continue

                opciones[serie].append({
                    "id": idg,
                    "letra": letra,
                    "cupo_a": cup_a,
                    "cupo_m": cup_m,
                    "celdas": celdas,
                    "txt": ", ".join(horas_txt)
                })

        # backtracking para generar hasta 4 paquetes en algunos casos 
        # forzamos la generacion de paquetes como resultado solo se modifica una materia
        soluciones = []
        usado = set()
        asign = {}

        def dfs(i):
            if len(soluciones) >= self.MAX_PERSONALIZED:
                return
            if i == len(objetivo_series):
                # armamos paquete completo
                detalle = []
                for serie in objetivo_series:
                    opt = asign[serie]
                    cur.execute("SELECT Nombre FROM Materias WHERE Serie=?", (serie,))
                    nombre = cur.fetchone()[0]
                    detalle.append((serie, nombre, opt["letra"], opt["txt"]))

                soluciones.append({
                    "mapping": {s: asign[s]["id"] for s in asign},
                    "detalle": detalle
                })
                return

            serie = objetivo_series[i]
            for opt in opciones.get(serie, []):

                if opt["cupo_a"] >= opt["cupo_m"]:
                    continue

                choque = any(c in usado for c in opt["celdas"])
                if choque:
                    continue

                asign[serie] = opt
                for c in opt["celdas"]:
                    usado.add(c)

                dfs(i + 1)

                for c in opt["celdas"]:
                    usado.remove(c)

        dfs(0)
        return soluciones

    # EVENTOS "lo relacionado cuando el usuario decide dar click al programa o acciones"
    def _on_tree_item_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)

        # paquete seleccionado
        if isinstance(data, str) and data.startswith("PAQUETE:"):
            parts = data.split(":")
            if parts[1] == "PERS_IDX":
                self._aplicar_paquete_personalizado_por_indice(int(parts[2]))
            else:
                self.aplicar_paquete(parts[1])
            return

        # selección normal
        if data is None:
            return

        try:
            id_grupo = int(data)
        except:
            return

        parent = item.parent()
        if not parent:
            return

        serie = parent.text(0).split(" - ")[0]

        # si lo vuelve a dar click lo quita
        if self.selecciones.get(serie) == id_grupo:
            del self.selecciones[serie]
        else:
            self.selecciones[serie] = id_grupo

        self.actualizar_horario()

    # Paquete regular
    def aplicar_paquete(self, letra):
        conn = self.conectar()
        cur = conn.cursor()

        # semestre
        cur.execute("SELECT Semestre FROM Alumnos WHERE Num_control=?", (self.num_control,))
        semestre = cur.fetchone()[0]

        # periodo
        cur.execute("SELECT Id_periodo FROM Periodos WHERE Activo=1")
        periodo_id = cur.fetchone()[0]

        # materias que si puede cursar del semestre
        cur.execute("""
            SELECT Serie
            FROM Materias
            WHERE Semestre=?
              AND (Seriada IS NULL OR Seriada IN (
                   SELECT Serie FROM Kardex 
                   WHERE Num_control=? AND Estatus='APROBADA'
              ))
              AND Serie NOT IN (
                SELECT Serie FROM Kardex WHERE Num_control=? 
                AND (Estatus='APROBADA' OR Estatus='CURSANDO')
              )
        """, (semestre, self.num_control, self.num_control))
        materias = [r[0] for r in cur.fetchall()]

        self.selecciones.clear()
        self.horario_ocupado.clear()

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

        # intentar meter todas las materias del paquete
        for serie in materias:
            cur.execute("""
                SELECT Id_grupo, Cupo_actual, Cupo_maximo
                FROM Grupos
                WHERE Serie_materia=? AND Id_periodo=? AND Grupo_letra=?
            """, (serie, periodo_id, letra))
            row = cur.fetchone()
            if not row:
                continue

            idg, cup_a, cup_m = row
            if cup_a >= cup_m:
                continue

            cur.execute("SELECT Dia_semana, Hora_inicio FROM Horario_Grupo WHERE Id_grupo=?", (idg,))
            horarios = cur.fetchall()

            choq = False
            temp = []
            for dia, hora in horarios:
                if dia not in dias:
                    choq = True
                    break
                fila = hora.hour - 7
                col = dias.index(dia) + 1
                if (fila, col) in self.horario_ocupado:
                    choq = True
                    break
                temp.append((fila, col))

            if choq:
                continue

            self.selecciones[serie] = idg
            for c in temp:
                self.horario_ocupado.add(c)

        conn.close()
        self.actualizar_horario()

    # PAQUETE PERSONALIZADO 
    def _aplicar_paquete_personalizado_por_indice(self, idx):
        if idx < 0 or idx >= len(self.personalizados):
            return

        paquete = self.personalizados[idx]["mapping"]
        self.selecciones.clear()
        self.horario_ocupado.clear()

        conn = self.conectar()
        cur = conn.cursor()

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

        for serie, idg in paquete.items():

            cur.execute("SELECT Cupo_actual, Cupo_maximo FROM Grupos WHERE Id_grupo=?", (idg,))
            cup_a, cup_m = cur.fetchone()
            if cup_a >= cup_m:
                continue

            cur.execute("SELECT Dia_semana, Hora_inicio FROM Horario_Grupo WHERE Id_grupo=?", (idg,))
            hrs = cur.fetchall()

            choq = False
            temp = []
            for dia, hora in hrs:
                fila = hora.hour - 7
                col = dias.index(dia) + 1
                if (fila, col) in self.horario_ocupado:
                    choq = True
                    break
                temp.append((fila, col))

            if choq:
                continue

            self.selecciones[serie] = idg
            for c in temp:
                self.horario_ocupado.add(c)

        conn.close()
        self.actualizar_horario()

    # Horario (la tabla donde se muestran los horarios )
    def actualizar_horario(self):
        """Actualiza el horario bonito del lado derecho."""
        self.limpiar_horario()
        self.horario_ocupado.clear()

        conn = self.conectar()
        cur = conn.cursor()

        celdas = []
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

        for serie, idg in self.selecciones.items():
            cur.execute("""
                SELECT Dia_semana, Hora_inicio, m.Nombre, g.Grupo_letra
                FROM Horario_Grupo h
                JOIN Grupos g ON h.Id_grupo=g.Id_grupo
                JOIN Materias m ON g.Serie_materia=m.Serie
                WHERE h.Id_grupo=?
            """, (idg,))
            for dia, hora, nombre, letra in cur.fetchall():
                fila = hora.hour - 7
                col = dias.index(dia) + 1
                texto = f"{nombre} ({letra})"
                celdas.append((fila, col, texto))
                self.horario_ocupado.add((fila, col))

        conn.close()

        choque = len(celdas) != len(self.horario_ocupado)

        for fila, col, texto in celdas:
            item = QTableWidgetItem(texto)
            item.setBackground(QColor("#ff5252") if choque else QColor("#90caf9"))
            item.setForeground(QColor("white") if choque else QColor("black"))
            item.setTextAlignment(Qt.AlignCenter)
            self.tabla_horario.setItem(fila, col, item)

        self.btn_finalizar.setEnabled(not choque)
        self.btn_finalizar.setStyleSheet(
            "background:#b0b0b0;" if choque else "background:#4caf50;color:white;font-weight:bold;"
        )

    def limpiar_horario(self):
        """Limpia la tabla del horario."""
        for f in range(15):
            for c in range(1, 6):
                self.tabla_horario.setItem(f, c, QTableWidgetItem(""))

    #  LIMPIAR Y ELIMINAR CARGA
    def limpiar_todo(self):
        """Limpia el horario sin borrar nada de BD."""
        self.selecciones.clear()
        self.horario_ocupado.clear()
        self.limpiar_horario()

    def eliminar_carga_bd(self):
        """Elimina todo lo inscrito en la BD."""
        conn = self.conectar()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM Inscripciones WHERE Num_control=?", (self.num_control,))
        if cur.fetchone()[0] == 0:
            conn.close()
            return

        ok = QMessageBox.question(
            self, "Confirmar",
            "¿Deseas borrar TODA tu carga inscrita?",
            QMessageBox.Yes | QMessageBox.No
        )

        if ok != QMessageBox.Yes:
            conn.close()
            return

        cur.execute("DELETE FROM Inscripciones WHERE Num_control=?", (self.num_control,))
        conn.commit()

        conn.close()

        self.limpiar_todo()

    # Finalizar la carga, cuando el alumno decide terminar su carga al ddarle click sus materias 
    # se guardaran en la bd y en el kardex las materias que tomo apareceran en cursando 
    def finalizar_carga(self):
        """Guarda la selección final en la BD."""
        if not self.selecciones:
            return

        conn = self.conectar()
        cur = conn.cursor()

        try:
            for idg in self.selecciones.values():
                cur.execute(
                    "INSERT INTO Inscripciones (Num_control, Id_grupo) VALUES (?, ?)",
                    (self.num_control, idg)
                )
            conn.commit()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "ERROR", str(e))

        finally:
            conn.close()

        self.close()
