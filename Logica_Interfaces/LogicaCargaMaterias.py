import pyodbc
from PyQt5.QtWidgets import (
    QMessageBox, QTreeWidgetItem, QTableWidgetItem
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from Diseño_Interfaces.CargaMaterias import CargaMaterias
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import os


class CargaMateriasLogic(CargaMaterias):
    def __init__(self, num_control):
        super().__init__()
        self.num_control = num_control
        self.selecciones = {}        
        self.horario_ocupado = set() 

        # Conectar señales (tree usado tanto para paquetes como para materias/grupos)
        self.tree_materias.itemClicked.connect(self._on_tree_item_clicked)
        self.btn_carga_paquete.clicked.connect(self.carga_automatica_paquete)
        self.btn_finalizar.clicked.connect(self.finalizar_carga)
        self.cargar_materias_disponibles()

    def conectar(self):
        return pyodbc.connect(
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=DESKTOP-33OLAEM\SQLEXPRESS;'
            r'DATABASE=PruebaDB;'
            r'Trusted_Connection=yes;'
        )

    def cargar_materias_disponibles(self):
        conn = self.conectar()
        cursor = conn.cursor()

        # Obtener semestre
        cursor.execute("SELECT Semestre FROM Alumnos WHERE Num_control = ?", (self.num_control,))
        row = cursor.fetchone()
        if not row:
            QMessageBox.critical(self, "Error", "Alumno no encontrado.")
            conn.close()
            return
        semestre = row[0]

        cursor.execute("SELECT Id_periodo FROM Periodos WHERE Activo = 1")
        periodo_row = cursor.fetchone()
        if not periodo_row:
            QMessageBox.critical(self, "ERROR", "No existe período activo.")
            conn.close()
            return
        periodo_id = periodo_row[0]

        # materias reprobadas para paquete personalizado 
        cursor.execute("""
            SELECT Serie
            FROM Kardex
            WHERE Num_control = ? AND Estatus = 'REPROBADA'
        """, (self.num_control,))
        reprobadas_rows = cursor.fetchall()
        reprobadas = [r[0] for r in reprobadas_rows] if reprobadas_rows else []

        self.tree_materias.clear()
        nodo_paquetes = QTreeWidgetItem(["PAQUETES"])
        nodo_paquetes.setBackground(0, QColor("#cfe9ff"))
        fontp = QFont(); fontp.setBold(True)
        nodo_paquetes.setFont(0, fontp)
        self.tree_materias.addTopLevelItem(nodo_paquetes)

        cursor.execute("""
            SELECT Serie, Nombre FROM Materias
            WHERE Semestre = ?
            ORDER BY Serie
        """, (semestre,))
        materias_sem = cursor.fetchall() 

        paquetes = {'A': [], 'B': [], 'C': [], 'D': []}
        for idx, (serie, nombre) in enumerate(materias_sem, start=1):
            p_index = ((idx-1) // 6)  # 0 -> A, 1 -> B, 2 -> C, 3 -> D, etc.
            if p_index == 0:
                paquetes['A'].append((serie, nombre, idx))
            elif p_index == 1:
                paquetes['B'].append((serie, nombre, idx))
            elif p_index == 2:
                paquetes['C'].append((serie, nombre, idx))
            else:
                paquetes['D'].append((serie, nombre, idx))

        for letra, lista in paquetes.items():
            paq_item = QTreeWidgetItem([f"Paquete {letra}"])
            paq_item.setData(0, Qt.UserRole, f"PAQUETE:{letra}")
            paq_item.setBackground(0, QColor("#b3e5fc"))
            nodo_paquetes.addChild(paq_item)

            for serie, nombre, orden in lista:
                cursor.execute("""
                    SELECT TOP 1 h.Hora_inicio, h.Hora_fin
                    FROM Grupos g
                    JOIN Horario_Grupo h ON g.Id_grupo = h.Id_grupo
                    WHERE g.Serie_materia = ? AND g.Grupo_letra = ? AND g.Id_periodo = ?
                    ORDER BY h.Hora_inicio
                """, (serie, letra, periodo_id))
                hora_row = cursor.fetchone()
                if hora_row:
                    ini, fin = hora_row
                    try:
                        hora_txt = f"{ini.strftime('%H:%M')}–{fin.strftime('%H:%M')}"
                    except Exception:
                        hora_txt = "--:--"
                else:
                    hora_txt = "--:--"

                sub = QTreeWidgetItem([f"   • {serie} - {nombre}  —  {hora_txt}"])
                sub.setFlags(sub.flags() & ~Qt.ItemIsSelectable)
                paq_item.addChild(sub)

        # Si el alumno tiene reprobadas, creamos el nodo PERSONALIZADO
        if reprobadas:
            pers_item = QTreeWidgetItem([f"PAQUETE PERSONALIZADO"])
            pers_item.setData(0, Qt.UserRole, "PAQUETE:PERS")
            pers_item.setBackground(0, QColor("#ffd7a6"))
            fontp2 = QFont(); fontp2.setBold(True)
            pers_item.setFont(0, fontp2)
            nodo_paquetes.addChild(pers_item)

            for serie in reprobadas:
                cursor.execute("SELECT Nombre FROM Materias WHERE Serie = ?", (serie,))
                r = cursor.fetchone()
                nombre_r = r[0] if r else serie

                # buscar hora 
                cursor.execute("""
                    SELECT TOP 1 h.Hora_inicio, h.Hora_fin
                    FROM Grupos g
                    JOIN Horario_Grupo h ON g.Id_grupo = h.Id_grupo
                    WHERE g.Serie_materia = ? AND g.Id_periodo = ?
                    ORDER BY h.Hora_inicio
                """, (serie, periodo_id))
                hora_row = cursor.fetchone()
                if hora_row:
                    try:
                        hora_txt = f"{hora_row[0].strftime('%H:%M')}–{hora_row[1].strftime('%H:%M')}"
                    except Exception:
                        hora_txt = "--:--"
                else:
                    hora_txt = "--:--"

                sub = QTreeWidgetItem([f"   • {serie} - {nombre_r}  —  {hora_txt}"])
                sub.setFlags(sub.flags() & ~Qt.ItemIsSelectable)
                pers_item.addChild(sub)

            # Luego, las materias del semestre disponibilidad
            cursor.execute("""
                SELECT m.Serie, m.Nombre, m.Creditos
                FROM Materias m
                WHERE m.Semestre = ?
                  AND (m.Seriada IS NULL OR m.Seriada IN (
                      SELECT Serie FROM Kardex WHERE Num_control = ? AND Estatus = 'APROBADA'
                  ))
                  AND m.Serie NOT IN (
                      SELECT Serie FROM Kardex WHERE Num_control = ?
                      AND (Estatus = 'APROBADA' OR Estatus = 'CURSANDO')
                  )
                ORDER BY m.Serie
            """, (semestre, self.num_control, self.num_control))
            sem_mats = cursor.fetchall()
            for serie_s, nombre_s, cred in sem_mats:
                if serie_s in reprobadas:
                    continue
                cursor.execute("""
                    SELECT TOP 1 h.Hora_inicio, h.Hora_fin
                    FROM Grupos g
                    JOIN Horario_Grupo h ON g.Id_grupo = h.Id_grupo
                    WHERE g.Serie_materia = ? AND g.Id_periodo = ?
                    ORDER BY h.Hora_inicio
                """, (serie_s, periodo_id))
                hora_row = cursor.fetchone()
                if hora_row:
                    try:
                        hora_txt = f"{hora_row[0].strftime('%H:%M')}–{hora_row[1].strftime('%H:%M')}"
                    except Exception:
                        hora_txt = "--:--"
                else:
                    hora_txt = "--:--"

                sub = QTreeWidgetItem([f"   • {serie_s} - {nombre_s}  —  {hora_txt}"])
                sub.setFlags(sub.flags() & ~Qt.ItemIsSelectable)
                pers_item.addChild(sub)

            pers_item.setExpanded(False)

        nodo_paquetes.setExpanded(True)

        # materias disponibles 
        query = """
        SELECT m.Serie, m.Nombre, m.Creditos
        FROM Materias m
        WHERE m.Semestre = ?
          AND (m.Seriada IS NULL OR m.Seriada IN (
              SELECT Serie FROM Kardex WHERE Num_control = ? AND Estatus = 'APROBADA'
          ))
          AND m.Serie NOT IN (
              SELECT Serie FROM Kardex WHERE Num_control = ?
              AND (Estatus = 'APROBADA' OR Estatus = 'CURSANDO')
          )
        ORDER BY m.Serie
        """
        cursor.execute(query, (semestre, self.num_control, self.num_control))
        materias = cursor.fetchall()

        for serie, nombre, creditos in materias:

            item_materia = QTreeWidgetItem([f"{serie} - {nombre} ({creditos} créditos)"])
            item_materia.setBackground(0, QColor("#e8f5e9"))
            font = QFont(); font.setBold(True)
            item_materia.setFont(0, font)
            self.tree_materias.addTopLevelItem(item_materia)

            cursor.execute("""
                SELECT g.Id_grupo, g.Grupo_letra, g.Cupo_actual, g.Cupo_maximo
                FROM Grupos g
                WHERE g.Serie_materia = ?
                  AND g.Id_periodo = ?
                ORDER BY g.Grupo_letra
            """, (serie, periodo_id))

            for id_grupo, letra, actual, maximo in cursor.fetchall():
                lleno = actual >= maximo
                color = "#a5d6a7" if not lleno else "#ff8a80"

                cursor.execute("""
                    SELECT TOP 1 Hora_inicio, Hora_fin
                    FROM Horario_Grupo
                    WHERE Id_grupo = ?
                    ORDER BY Hora_inicio
                """, (id_grupo,))
                hora_row = cursor.fetchone()
                horario_text = ""
                if hora_row:
                    ini, fin = hora_row
                    try:
                        horario_text = f" — {ini.strftime('%H:%M')}–{fin.strftime('%H:%M')}"
                    except Exception:
                        horario_text = ""

                text_grupo = f"   Grupo {letra} → Cupo: {actual}/{maximo}{horario_text}"
                item_grupo = QTreeWidgetItem([text_grupo])
                item_grupo.setData(0, Qt.UserRole, id_grupo)
                item_grupo.setBackground(0, QColor(color))

                if lleno:
                    item_grupo.setFlags(item_grupo.flags() & ~Qt.ItemIsEnabled)

                item_materia.addChild(item_grupo)

            item_materia.setExpanded(False)

        # MATERIAS ADELANTABLES
        cursor.execute("""
            SELECT m.Serie, m.Nombre, m.Creditos
            FROM Materias m
            WHERE m.Semestre > ?
              AND m.Seriada IS NULL
              AND m.Serie NOT IN (
                  SELECT Serie FROM Kardex
                  WHERE Num_control = ?
                    AND (Estatus = 'APROBADA' OR Estatus = 'CURSANDO')
              )
            ORDER BY m.Semestre, m.Serie
        """, (semestre, self.num_control))

        adelantables = cursor.fetchall()

        if adelantables:
            nodo_adelante = QTreeWidgetItem(["MATERIAS ADELANTABLES"])
            font_a = QFont(); font_a.setBold(True)
            nodo_adelante.setFont(0, font_a)
            nodo_adelante.setBackground(0, QColor("#fff4ce"))
            self.tree_materias.addTopLevelItem(nodo_adelante)

            for serie, nombre, creditos in adelantables:
                item_mat = QTreeWidgetItem([f"{serie} - {nombre} ({creditos} créditos)"])
                item_mat.setBackground(0, QColor("#fffbe6"))
                nodo_adelante.addChild(item_mat)

                # grupos disponibles
                cursor.execute("""
                    SELECT g.Id_grupo, g.Grupo_letra, g.Cupo_actual, g.Cupo_maximo
                    FROM Grupos g
                    WHERE g.Serie_materia = ?
                      AND g.Id_periodo = ?
                    ORDER BY g.Grupo_letra
                """, (serie, periodo_id))

                for idg, letra, cupo_a, cupo_m in cursor.fetchall():
                    lleno = cupo_a >= cupo_m
                    color = "#dcedc8" if not lleno else "#ffcdd2"

                    cursor.execute("""
                        SELECT TOP 1 Hora_inicio, Hora_fin
                        FROM Horario_Grupo
                        WHERE Id_grupo = ?
                        ORDER BY Hora_inicio
                    """, (idg,))
                    hrow = cursor.fetchone()
                    hora_txt = ""
                    if hrow:
                        try:
                            hora_txt = f" — {hrow[0].strftime('%H:%M')}–{hrow[1].strftime('%H:%M')}"
                        except Exception:
                            hora_txt = ""

                    child = QTreeWidgetItem([f"   Grupo {letra} — {cupo_a}/{cupo_m}{hora_txt}"])
                    child.setData(0, Qt.UserRole, idg)
                    child.setBackground(0, QColor(color))

                    if lleno:
                        child.setFlags(child.flags() & ~Qt.ItemIsEnabled)

                    item_mat.addChild(child)

            nodo_adelante.setExpanded(False)

        conn.close()

    def _on_tree_item_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if isinstance(data, str) and data.startswith("PAQUETE:"):
            tag = data.split(":")[1]
            if tag == "PERS":
                self.aplicar_paquete_personalizado()
            else:
                self.aplicar_paquete(tag)
            return

        if data is None:
            return
        try:
            id_grupo = int(data)
        except Exception:
            return
        parent = item.parent()
        if not parent:
            return
        serie = parent.text(0).split(" - ")[0]
        if serie in self.selecciones and self.selecciones[serie] == id_grupo:
            del self.selecciones[serie]
        else:
            self.selecciones[serie] = id_grupo
        self.actualizar_horario()

    def aplicar_paquete(self, letra_paquete: str):
        """
        Intenta seleccionar para el alumno las materias del semestre tomando
        el grupo cuya letra coincide con letra_paquete.
        Respeta cupo y evita choques de horario.
        """
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT Semestre FROM Alumnos WHERE Num_control = ?", (self.num_control,))
        row = cursor.fetchone()
        if not row:
            QMessageBox.critical(self, "Error", "Alumno no encontrado.")
            conn.close()
            return
        semestre = row[0]

        cursor.execute("SELECT Id_periodo FROM Periodos WHERE Activo = 1")
        periodo_row = cursor.fetchone()
        if not periodo_row:
            QMessageBox.critical(self, "ERROR", "No existe período activo.")
            conn.close()
            return
        periodo_id = periodo_row[0]

        cursor.execute("""
            SELECT m.Serie, m.Nombre
            FROM Materias m
            WHERE m.Semestre = ?
              AND (m.Seriada IS NULL OR m.Seriada IN (
                  SELECT Serie FROM Kardex WHERE Num_control = ? AND Estatus = 'APROBADA'
              ))
              AND m.Serie NOT IN (
                  SELECT Serie FROM Kardex WHERE Num_control = ?
                  AND (Estatus = 'APROBADA' OR Estatus = 'CURSANDO')
              )
            ORDER BY m.Serie
        """, (semestre, self.num_control, self.num_control))

        materias = cursor.fetchall()

        seleccionadas = 0
        saltadas_cupo = 0
        saltadas_choque = 0
        saltadas_no_grupo = 0

        self.selecciones.clear()
        self.horario_ocupado.clear()

        for serie, nombre in materias:
            cursor.execute("""
                SELECT Id_grupo, Cupo_actual, Cupo_maximo
                FROM Grupos
                WHERE Serie_materia = ? AND Id_periodo = ? AND Grupo_letra = ?
            """, (serie, periodo_id, letra_paquete))
            grp = cursor.fetchone()
            if not grp:
                saltadas_no_grupo += 1
                continue
            id_grupo, cupo_actual, cupo_maximo = grp
            if cupo_actual >= cupo_maximo:
                saltadas_cupo += 1
                continue

            cursor.execute("""
                SELECT Dia_semana, Hora_inicio
                FROM Horario_Grupo
                WHERE Id_grupo = ?
            """, (id_grupo,))
            horarios = cursor.fetchall()
            choque = False
            proposed_cells = []
            for dia, hora in horarios:
                try:
                    fila = hora.hour - 7
                except Exception:
                    choque = True
                    break
                if fila < 0 or fila >= 15:
                    choque = True
                    break
                days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
                if dia not in days:
                    choque = True
                    break
                col = days.index(dia) + 1
                if (fila, col) in self.horario_ocupado:
                    choque = True
                    break
                proposed_cells.append((fila, col))

            if choque:
                saltadas_choque += 1
                continue

            self.selecciones[serie] = id_grupo
            for cell in proposed_cells:
                self.horario_ocupado.add(cell)
            seleccionadas += 1

        conn.close()
        # Actualizar el horario 
        self.actualizar_horario()

    #configuracion de paquetes personalizados
    def aplicar_paquete_personalizado(self):
        """
        Genera automáticamente un paquete para alumnos con materias reprobadas.
        Regla:
            - Primero se cargan TODAS las reprobadas
            - Luego se agregan materias del semestre actual
            - Máximo 6 materias
            - Sin choques de horario
        """

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT Semestre FROM Alumnos WHERE Num_control = ?", (self.num_control,))
        semestre = cursor.fetchone()[0]
        cursor.execute("SELECT Id_periodo FROM Periodos WHERE Activo = 1")
        row = cursor.fetchone()
        if not row:
            QMessageBox.critical(self, "Error", "No existe período activo.")
            conn.close()
            return
        periodo_id = row[0]

        # materias reprobadas
        cursor.execute("""
            SELECT m.Serie, m.Nombre
            FROM Kardex k
            JOIN Materias m ON k.Serie = m.Serie
            WHERE Num_control = ? AND Estatus = 'REPROBADA'
        """, (self.num_control,))
        reprobadas = cursor.fetchall()
        # materias que se supone debe cursar el alumno
        cursor.execute("""
            SELECT m.Serie, m.Nombre
            FROM Materias m
            WHERE m.Semestre = ?
              AND (m.Seriada IS NULL OR m.Seriada IN (
                    SELECT Serie
                    FROM Kardex
                    WHERE Num_control = ? AND Estatus='APROBADA'
              ))
              AND m.Serie NOT IN (
                    SELECT Serie
                    FROM Kardex
                    WHERE Num_control = ? AND (Estatus='APROBADA' OR Estatus='CURSANDO')
              )
        """, (semestre, self.num_control, self.num_control))
        materias_semestre = cursor.fetchall()


        self.selecciones.clear()
        self.horario_ocupado.clear()

        MAX_MATERIAS = 6
        total_asignadas = 0


        def intentar_asignar_materia(serie):
            nonlocal total_asignadas

            if total_asignadas >= MAX_MATERIAS:
                return False

            # hay espacio?
            cursor.execute("""
                SELECT Id_grupo
                FROM Grupos
                WHERE Serie_materia = ? AND Id_periodo = ? AND Cupo_actual < Cupo_maximo
                ORDER BY Grupo_letra
            """, (serie, periodo_id))
            grupos = cursor.fetchall()

            for (id_grupo,) in grupos:

                # horarios del grupo
                cursor.execute("""
                    SELECT Dia_semana, Hora_inicio, Hora_fin
                    FROM Horario_Grupo
                    WHERE Id_grupo = ?
                """, (id_grupo,))
                horarios = cursor.fetchall()

                # hay choques entre materias???
                choque = False
                for dia, ini, _ in horarios:

                    fila = ini.hour - 7
                    col = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"].index(dia) + 1

                    if (fila, col) in self.horario_ocupado:
                        choque = True
                        break

                if choque:
                    continue

                # Si no hay choque
                self.selecciones[serie] = id_grupo

                # Marcar horario ocupado
                for dia, ini, _ in horarios:
                    fila = ini.hour - 7
                    col = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"].index(dia) + 1
                    self.horario_ocupado.add((fila, col))

                total_asignadas += 1
                return True

            return False

        # AGREGAR REPROBADAS
        for serie, _ in reprobadas:
            intentar_asignar_materia(serie)

        # MATERIAS DEL SEMESTRE
        for serie, _ in materias_semestre:
            if total_asignadas < MAX_MATERIAS:
                intentar_asignar_materia(serie)
            else:
                break

        conn.close()

        # Actualizar la vista del horario
        self.actualizar_horario()

        QMessageBox.information(
            self,
            "Paquete generado",
            f"Se asignaron {total_asignadas} materias de forma automática."
        )


    # ACTUALIZAR HORARIO 
    def actualizar_horario(self):
        self.limpiar_horario()
        self.horario_ocupado.clear()
        celdas = []

        conn = self.conectar()
        cursor = conn.cursor()

        for serie, id_grupo in self.selecciones.items():
            cursor.execute("""
                SELECT h.Dia_semana, h.Hora_inicio, m.Nombre, g.Grupo_letra
                FROM Horario_Grupo h
                JOIN Grupos g ON h.Id_grupo = g.Id_grupo
                JOIN Materias m ON g.Serie_materia = m.Serie
                WHERE h.Id_grupo = ?
            """, (id_grupo,))

            for dia, hora_inicio, nombre_mat, letra in cursor.fetchall():
                try:
                    fila = hora_inicio.hour - 7
                except Exception:
                    continue
                if fila < 0 or fila >= 15:
                    continue
                days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
                if dia not in days:
                    continue
                col = days.index(dia) + 1
                texto_celda = f"{nombre_mat} ({letra})"
                celdas.append((fila, col, serie, texto_celda))
                self.horario_ocupado.add((fila, col))

        conn.close()

        hay_choque = len(celdas) != len(self.horario_ocupado)

        for fila, col, serie, texto_celda in celdas:
            color = QColor("#ff5252") if hay_choque else QColor("#90caf9")
            item = QTableWidgetItem(texto_celda)
            item.setBackground(color)
            item.setForeground(QColor("white") if hay_choque else QColor("black"))
            item.setTextAlignment(Qt.AlignCenter)
            self.tabla_horario.setItem(fila, col, item)

        # Cambiar estilo del botón
        self.btn_finalizar.setEnabled(not hay_choque)
        if hay_choque:
            self.btn_finalizar.setStyleSheet("background:#b0b0b0;")
        else:
            self.btn_finalizar.setStyleSheet("background:#4caf50;color:white;font-weight:bold;")

    def limpiar_horario(self):
        for i in range(15):
            for j in range(1, 6):
                self.tabla_horario.setItem(i, j, QTableWidgetItem(""))

    # ==================== CARGA AUTOMÁTICA (botón) - mantiene comportamiento previo ====================
    def carga_automatica_paquete(self):
        # Este botón ahora hace lo mismo que antes: intenta seleccionar el mejor grupo
        # por materia (independiente de paquetes). Lo dejamos como "mejor cupo disponible".
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT Semestre FROM Alumnos WHERE Num_control = ?", (self.num_control,))
        row = cursor.fetchone()
        if not row:
            QMessageBox.critical(self, "Error", "Alumno no encontrado.")
            conn.close()
            return
        semestre = row[0]

        cursor.execute("""
            SELECT Serie
            FROM Materias
            WHERE Semestre = ?
              AND (Seriada IS NULL OR Seriada IN (
                  SELECT Serie FROM Kardex WHERE Num_control = ? AND Estatus='APROBADA'
              ))
              AND Serie NOT IN (
                  SELECT Serie FROM Kardex WHERE Num_control = ?
                   AND (Estatus='APROBADA' OR Estatus='CURSANDO')
              )
        """, (semestre, self.num_control, self.num_control))

        materias = [r[0] for r in cursor.fetchall()]
        self.selecciones.clear()

        # Período activo
        cursor.execute("SELECT Id_periodo FROM Periodos WHERE Activo=1")
        periodo_row = cursor.fetchone()
        if not periodo_row:
            QMessageBox.critical(self, "ERROR", "No existe período activo.")
            conn.close()
            return
        periodo_id = periodo_row[0]

        for serie in materias:
            cursor.execute("""
                SELECT TOP 1 Id_grupo
                FROM Grupos
                WHERE Serie_materia = ?
                  AND Id_periodo = ?
                  AND Cupo_actual < Cupo_maximo
                ORDER BY (Cupo_maximo - Cupo_actual) DESC
            """, (serie, periodo_id))

            row = cursor.fetchone()
            if row:
                self.selecciones[serie] = row[0]

        conn.close()
        self.actualizar_horario()

        QMessageBox.information(self, "Paquete listo",
                                f"Se seleccionaron {len(self.selecciones)} materias.")

    def finalizar_carga(self):
        if not self.selecciones:
            QMessageBox.warning(self, "Nada seleccionado",
                                "Selecciona al menos un grupo.")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        try:
            for id_grupo in self.selecciones.values():
                cursor.execute("""
                    INSERT INTO Inscripciones (Num_control, Id_grupo)
                    VALUES (?, ?)
                """, (self.num_control, id_grupo))
            conn.commit()

            QMessageBox.information(self, "Carga completa",
                                    "Tu carga académica fue registrada correctamente.")
            self.generar_pdf_comprobante()
            self.close()

            from Logica_Interfaces.Menu import MenuLogic
            MenuLogic(self.num_control).show()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "ERROR", str(e))

        finally:
            conn.close()

    def generar_pdf_comprobante(self):
        escritorio = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        archivo = os.path.join(
            escritorio,
            f"Comprobante_{self.num_control}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )

        c = canvas.Canvas(archivo, pagesize=letter)
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(300, 780, "COMPROBANTE DE CARGA ACADÉMICA")

        c.setFont("Helvetica", 12)
        c.drawString(50, 750, f"Alumno: {self.num_control}")
        c.drawString(50, 730, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        y = 680

        conn = self.conectar()
        cursor = conn.cursor()

        for serie, id_grupo in self.selecciones.items():
            cursor.execute("""
                SELECT m.Nombre, g.Grupo_letra
                FROM Materias m
                JOIN Grupos g ON m.Serie = g.Serie_materia
                WHERE g.Id_grupo = ?
            """, (id_grupo,))
            row = cursor.fetchone()
            if row:
                nombre, grupo = row
                c.drawString(50, y, f"• {serie} - {nombre} - Grupo {grupo}")
                y -= 30

        conn.close()

        c.showPage()
        c.save()

        try:
            os.startfile(archivo)
        except Exception:
            pass
