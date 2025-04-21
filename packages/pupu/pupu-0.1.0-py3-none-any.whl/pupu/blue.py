import sys
import sqlite3
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QTableWidget, QPushButton, QLineEdit, 
                              QDialog, QLabel, QComboBox, QMessageBox, QTableWidgetItem,
                              QFormLayout, QCheckBox, QFileDialog, QGridLayout, QFrame, QScrollArea)
from PySide6.QtCore import Qt, Signal
from typing import List, Dict, Tuple
import uuid

# Настройка Pandas для устранения FutureWarning
pd.set_option('future.no_silent_downcasting', True)

class Database:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Enable foreign key constraints
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()
        self.hidden_tables = ['users', 'Materials_In_Products', 'sqlite_sequence']

    def get_tables(self) -> List[str]:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in self.cursor.fetchall() if table[0] not in self.hidden_tables]

    def get_table_columns(self, table: str) -> List[Tuple[str, str]]:
        self.cursor.execute(f"PRAGMA table_info(\"{table}\")")
        return [(col[1], col[2]) for col in self.cursor.fetchall()]

    def get_table_data(self, table: str) -> List[Tuple]:
        self.cursor.execute(f"SELECT * FROM \"{table}\"")
        return self.cursor.fetchall()

    def get_primary_key(self, table: str) -> str:
        self.cursor.execute(f"PRAGMA table_info(\"{table}\")")
        for col in self.cursor.fetchall():
            if col[5]:  # PK flag
                return col[1]
        columns = self.get_table_columns(table)
        return columns[0][0]

    def get_foreign_keys(self, table: str) -> Dict[str, Tuple[str, str]]:
        self.cursor.execute(f"PRAGMA foreign_key_list(\"{table}\")")
        foreign_keys = {}
        for fk in self.cursor.fetchall():
            column = fk[3]
            ref_table = fk[2]
            ref_column = fk[4]
            foreign_keys[column] = (ref_table, ref_column)
        return foreign_keys

    def detect_many_to_many(self, table: str) -> Dict[str, Tuple[str, str]]:
        many_to_many = {}
        foreign_keys = self.get_foreign_keys(table)
        if len(foreign_keys) >= 2:
            for column, (ref_table, ref_column) in foreign_keys.items():
                many_to_many[column] = (ref_table, ref_column)
        return many_to_many

    def heuristic_foreign_keys(self, table: str) -> Dict[str, Tuple[str, str]]:
        heuristic_keys = {}
        columns = self.get_table_columns(table)
        all_tables = self.get_tables()

        for col_name, col_type in columns:
            if col_name.startswith("Тип_") or col_name.lower().endswith("_id"):
                possible_table = col_name.replace("Тип_", "") if col_name.startswith("Тип_") else col_name[:-3]
                possible_table = f"{possible_table}_Types"
                for tbl in all_tables:
                    if possible_table.lower() in tbl.lower():
                        ref_columns = self.get_table_columns(tbl)
                        ref_column = "Код" if "Код" in [c[0] for c in ref_columns] else "id"
                        heuristic_keys[col_name] = (tbl, ref_column)
                        break
                if col_name not in heuristic_keys:
                    self.create_related_table(possible_table)
                    ref_columns = self.get_table_columns(possible_table)
                    ref_column = "Код"
                    heuristic_keys[col_name] = (possible_table, ref_column)
        return heuristic_keys

    def create_related_table(self, table_name: str):
        try:
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    Код INTEGER PRIMARY KEY AUTOINCREMENT,
                    Название TEXT NOT NULL UNIQUE
                )
            ''')
            self.conn.commit()
            print(f"Создана или проверена таблица {table_name}")
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы {table_name}: {str(e)}")

    def get_relationships(self, table: str) -> Dict[str, Tuple[str, str]]:
        relationships = self.get_foreign_keys(table)
        relationships.update(self.detect_many_to_many(table))
        relationships.update(self.heuristic_foreign_keys(table))
        return relationships

    def get_combo_box_data(self, table: str, display_col: str, value_col: str) -> List[Tuple]:
        try:
            self.cursor.execute(f"SELECT \"{value_col}\", \"{display_col}\" FROM \"{table}\"")
            return self.cursor.fetchall()
        except sqlite3.Error:
            return []

    def find_display_column(self, table: str) -> str:
        ref_columns = self.get_table_columns(table)
        if "Название" in [c[0] for c in ref_columns]:
            return "Название"
        for col in ref_columns:
            if col[1].upper().startswith("TEXT"):
                return col[0]
        pk = self.get_primary_key(table)
        for col in ref_columns:
            if col[0] != pk:
                return col[0]
        return ref_columns[0][0]

    def find_related_id(self, table: str, display_col: str, value_col: str, display_value: str) -> any:
        if not display_value or not display_value.strip():
            print(f"Пустое значение для {table}.{display_col}, возвращается None")
            return None

        display_value = display_value.strip()
        print(f"Поиск {display_value} в {table}.{display_col}")
        try:
            self.cursor.execute(
                f"SELECT \"{value_col}\" FROM \"{table}\" WHERE TRIM(\"{display_col}\") = ?",
                (display_value,)
            )
            result = self.cursor.fetchone()
            found_id = result[0] if result else None
            print(f"Найден ID {found_id} для {display_value} в {table}")
            return found_id
        except sqlite3.Error as e:
            print(f"Ошибка при поиске ID для {display_value} в {table}: {str(e)}")
            return None

    def add_related_value(self, table: str, display_col: str, value_col: str, display_value: str) -> any:
        if not display_value or not isinstance(display_value, str) or not display_value.strip():
            print(f"Пустое или некорректное значение для {table}.{display_col}: {display_value!r}, возвращается None")
            return None

        display_value = display_value.strip()
        print(f"Обработка связанного значения: {display_value!r} для {table}.{display_col} (value_col={value_col})")
        try:
            existing_id = self.find_related_id(table, display_col, value_col, display_value)
            if existing_id is not None:
                print(f"Найден существующий ID {existing_id} для {display_value} в {table}")
                return existing_id

            self.create_related_table(table)
            print(f"Схема после проверки существования таблицы:")
            self.print_table_schema(table)

            columns = self.get_table_columns(table)
            is_autoincrement = any(col[5] and col[1].lower() == value_col.lower() for col in columns)
            print(f"Является ли {value_col} автоинкрементным? {is_autoincrement}")

            if is_autoincrement:
                query = f'INSERT INTO "{table}" ("{display_col}") VALUES (?)'
                self.cursor.execute(query, (display_value,))
            else:
                self.cursor.execute(f"SELECT MAX(\"{value_col}\") FROM \"{table}\"")
                max_id = self.cursor.fetchone()[0]
                new_id = (max_id or 0) + 1
                query = f'INSERT INTO "{table}" ("{value_col}", "{display_col}") VALUES (?, ?)'
                self.cursor.execute(query, (new_id, display_value))

            self.conn.commit()
            print(f"Вставлено {display_value} в {table}")

            new_id = self.find_related_id(table, display_col, value_col, display_value)
            if new_id is None:
                raise ValueError(f"Не удалось получить новый ID для {display_value} в {table}")
            print(f"Добавлен новый ID {new_id} для {display_value} в {table}")
            return new_id
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении значения {display_value} в {table}: {str(e)}")
            return None

    def insert(self, table: str, data: Dict):
        columns = ', '.join(f'"{key}"' for key in data.keys())
        placeholders = ', '.join('?' * len(data))
        query = f'INSERT INTO "{table}" ({columns}) VALUES ({placeholders})'
        try:
            self.cursor.execute(query, list(data.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при вставке в {table}: {str(e)}")
            raise

    def update(self, table: str, pk_column: str, pk_value: str, data: Dict):
        set_clause = ', '.join(f'"{k}" = ?' for k in data.keys())
        query = f'UPDATE "{table}" SET {set_clause} WHERE "{pk_column}" = ?'
        self.cursor.execute(query, list(data.values()) + [pk_value])
        self.conn.commit()

    def delete(self, table: str, pk_column: str, pk_value: str):
        all_tables = self.get_tables()
        dependent_tables = []
        for child_table in all_tables:
            if child_table == table:
                continue
            foreign_keys = self.get_foreign_keys(child_table)
            for fk_column, (ref_table, ref_column) in foreign_keys.items():
                if ref_table == table and ref_column == pk_column:
                    self.cursor.execute(
                        f"SELECT COUNT(*) FROM \"{child_table}\" WHERE \"{fk_column}\" = ?",
                        (pk_value,)
                    )
                    count = self.cursor.fetchone()[0]
                    if count > 0:
                        dependent_tables.append((child_table, count))

        if dependent_tables:
            error_message = f"Невозможно удалить запись из таблицы {table}, так как она используется в:\n"
            for dep_table, count in dependent_tables:
                error_message += f"- {dep_table} ({count} записей)\n"
            raise sqlite3.IntegrityError(error_message)

        query = f'DELETE FROM "{table}" WHERE "{pk_column}" = ?'
        self.cursor.execute(query, [pk_value])
        self.conn.commit()

    def authenticate(self, username: str, password: str) -> Tuple[bool, bool]:
        self.cursor.execute(
            'SELECT is_admin FROM users WHERE username = ? AND password = ?',
            (username, password)
        )
        result = self.cursor.fetchone()
        return (bool(result), result[0] if result else False)

    def register_user(self, username: str, password: str, is_admin: bool = False):
        user_id = str(uuid.uuid4())
        try:
            self.cursor.execute(
                'INSERT INTO users (id, username, password, is_admin) VALUES (?, ?, ?, ?)',
                (user_id, username, password, is_admin)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_users(self) -> List[Tuple]:
        self.cursor.execute('SELECT id, username, password, is_admin FROM users')
        return self.cursor.fetchall()

    def update_user(self, user_id: str, username: str, password: str, is_admin: bool):
        try:
            self.cursor.execute(
                'UPDATE users SET username = ?, password = ?, is_admin = ? WHERE id = ?',
                (username, password, is_admin, user_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении пользователя: {str(e)}")
            raise

    def delete_user(self, user_id: str):
        try:
            self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пользователя: {str(e)}")
            raise

    def print_table_schema(self, table: str):
        try:
            self.cursor.execute(f"PRAGMA table_info(\"{table}\")")
            columns = self.cursor.fetchall()
            print(f"Схема таблицы {table}:")
            for col in columns:
                print(f"Столбец: {col[1]}, Тип: {col[2]}, Не Null: {col[3]}, По умолчанию: {col[4]}, PK: {col[5]}")
        except sqlite3.Error as e:
            print(f"Ошибка при получении схемы таблицы {table}: {str(e)}")

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setStyleSheet("""
            QDialog {
                background-color: #E6F7FA;
                font-family: Arial;
            }
            QLineEdit {
                border: 1px solid #4A90E2;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFFFF;
                color: #333333;
            }
            QPushButton {
                background-color: #4A90E2;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7AB8F5;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
        """)
        
        # Основной layout для центрирования
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Форма для полей ввода
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("Имя пользователя:", self.username_input)
        form_layout.addRow("Пароль:", self.password_input)
        
        # Кнопки в горизонтальном layout
        buttons_layout = QHBoxLayout()
        login_button = QPushButton("Войти")
        register_button = QPushButton("Зарегистрироваться")
        
        buttons_layout.addWidget(login_button)
        buttons_layout.addWidget(register_button)
        
        login_button.clicked.connect(self.accept)
        register_button.clicked.connect(self.register)
        
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
            return
        
        db = Database("database.db")
        if db.register_user(username, password):
            QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован")
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует")

class AddUserDialog(QDialog):
    def __init__(self, existing_username: str = None):
        super().__init__()
        self.setWindowTitle("Добавить нового пользователя" if not existing_username else "Редактировать пользователя")
        self.setStyleSheet("""
            QDialog {
                background-color: #E6F7FA;
                font-family: Arial;
            }
            QLineEdit {
                border: 1px solid #4A90E2;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFFFF;
                color: #333333;
            }
            QPushButton {
                background-color: #4A90E2;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7AB8F5;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QCheckBox {
                color: #333333;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.is_admin_check = QCheckBox("Администратор")
        
        if existing_username:
            self.username_input.setText(existing_username)
        
        form_layout.addRow("Имя пользователя:", self.username_input)
        form_layout.addRow("Пароль:", self.password_input)
        form_layout.addRow("", self.is_admin_check)
        
        # Кнопка "Сохранить" в правом нижнем углу
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

class UserManager(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление пользователями")
        self.setMinimumSize(600, 400)

        # Стили
        self.setStyleSheet("""
            QWidget {
                background-color: #E6F7FA;
                font-family: Arial;
            }
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #4A90E2;
                border-radius: 5px;
                gridline-color: #4A90E2;
                color: #333333;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #4A90E2;
            }
            QHeaderView::section {
                background-color: #4A90E2;
                color: #FFFFFF;
                padding: 5px;
                border: none;
            }
            QLineEdit, QComboBox {
                border: 1px solid #4A90E2;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFFFF;
                color: #333333;
            }
            QPushButton {
                background-color: #4A90E2;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #7AB8F5;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
        """)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Боковая панель с кнопками
        sidebar_layout = QVBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")

        sidebar_layout.addWidget(self.add_button)
        sidebar_layout.addWidget(self.edit_button)
        sidebar_layout.addWidget(self.delete_button)
        sidebar_layout.addStretch()

        self.add_button.clicked.connect(self.add_user)
        self.edit_button.clicked.connect(self.edit_user)
        self.delete_button.clicked.connect(self.delete_user)

        # Таблица пользователей
        table_container = QWidget()
        table_layout = QVBoxLayout()
        self.user_table = QTableWidget()
        self.user_table.setMinimumHeight(200)
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Имя пользователя", "Пароль", "Администратор"])
        self.refresh_users()
        table_layout.addWidget(self.user_table)
        table_container.setLayout(table_layout)

        self.user_table.cellClicked.connect(self.on_cell_clicked)

        main_layout.addLayout(sidebar_layout)
        main_layout.addWidget(table_container, stretch=1)
        self.setLayout(main_layout)

    def refresh_users(self):
        users = self.db.get_users()
        self.user_table.setRowCount(len(users))
        for row_idx, user in enumerate(users):
            # user: (id, username, password, is_admin)
            self.user_table.setItem(row_idx, 0, QTableWidgetItem(user[1]))  # username
            self.user_table.setItem(row_idx, 1, QTableWidgetItem(user[2]))  # password
            self.user_table.setItem(row_idx, 2, QTableWidgetItem("Да" if user[3] else "Нет"))  # is_admin
        self.user_table.resizeColumnsToContents()

    def on_cell_clicked(self, row, column):
        self.selected_user_id = self.db.get_users()[row][0]  # id пользователя

    def add_user(self):
        dialog = AddUserDialog()
        if dialog.exec():
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            is_admin = dialog.is_admin_check.isChecked()

            if not username or not password:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
                return

            if self.db.register_user(username, password, is_admin):
                QMessageBox.information(self, "Успех", "Пользователь успешно добавлен")
                self.refresh_users()
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует")

    def edit_user(self):
        if not hasattr(self, 'selected_user_id'):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите пользователя, щелкнув по строке")
            return

        users = self.db.get_users()
        selected_user = next((user for user in users if user[0] == self.selected_user_id), None)
        if not selected_user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        dialog = AddUserDialog(existing_username=selected_user[1])
        dialog.password_input.setText(selected_user[2])
        dialog.is_admin_check.setChecked(bool(selected_user[3]))

        if dialog.exec():
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            is_admin = dialog.is_admin_check.isChecked()

            if not username or not password:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
                return

            try:
                self.db.update_user(self.selected_user_id, username, password, is_admin)
                QMessageBox.information(self, "Успех", "Пользователь успешно обновлен")
                self.refresh_users()
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось обновить пользователя: {str(e)}")

    def delete_user(self):
        if not hasattr(self, 'selected_user_id'):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите пользователя, щелкнув по строке")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить этого пользователя?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_user(self.selected_user_id)
                QMessageBox.information(self, "Успех", "Пользователь успешно удален")
                self.refresh_users()
                delattr(self, 'selected_user_id')
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить пользователя: {str(e)}")

class TableEditor(QWidget):
    def __init__(self, db: Database, table: str, is_admin: bool):
        super().__init__()
        self.db = db
        self.table = table
        self.is_admin = is_admin
        self.columns = self.db.get_table_columns(table)
        self.pk_column = self.db.get_primary_key(table)
        self.relationships = self.db.get_relationships(table)
        self.selected_pk_value = None

        # Основной стиль для редактора таблицы
        self.setStyleSheet("""
            QWidget {
                background-color: #E6F7FA;
                font-family: Arial;
            }
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #4A90E2;
                border-radius: 5px;
                gridline-color: #4A90E2;
                color: #333333;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #4A90E2;
            }
            QHeaderView::section {
                background-color: #4A90E2;
                color: #FFFFFF;
                padding: 5px;
                border: none;
            }
            QLineEdit, QComboBox {
                border: 1px solid #4A90E2;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFFFF;
                color: #333333;
            }
            QPushButton {
                background-color: #4A90E2;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #7AB8F5;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
        """)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)

        # Таблица (слева)
        table_container = QWidget()
        table_layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        self.table_widget.setMinimumWidth(400)
        self.refresh_table()
        table_layout.addWidget(self.table_widget)
        table_container.setLayout(table_layout)

        self.table_widget.cellClicked.connect(self.on_cell_clicked)

        # Правая панель: поля ввода и кнопки
        right_panel = QVBoxLayout()
        
        # Прокручиваемая область для полей ввода
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        inputs_container = QWidget()
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)

        self.inputs = {}
        for col_name, col_type in self.columns:
            if col_name.lower() == "код":
                continue

            row_layout = QHBoxLayout()
            label = QLabel(col_name)
            if col_name in self.relationships:
                ref_table, ref_column = self.relationships[col_name]
                ref_columns = self.db.get_table_columns(ref_table)
                display_col = self.db.find_display_column(ref_table)

                combo_box = QComboBox()
                combo_data = self.db.get_combo_box_data(ref_table, display_col, ref_column)
                for value, display in combo_data:
                    combo_box.addItem(display, value)
                self.inputs[col_name] = combo_box
                row_layout.addWidget(label)
                row_layout.addWidget(combo_box)
            else:
                input_field = QLineEdit()
                self.inputs[col_name] = input_field
                row_layout.addWidget(label)
                row_layout.addWidget(input_field)

            controls_layout.addLayout(row_layout)

        inputs_container.setLayout(controls_layout)
        scroll_area.setWidget(inputs_container)
        right_panel.addWidget(scroll_area)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.add_button = QPushButton("Добавить")
        self.update_button = QPushButton("Обновить")
        self.delete_button = QPushButton("Удалить")
        clear_button = QPushButton("Очистить поля")

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(clear_button)

        self.add_button.clicked.connect(self.add_record)
        self.update_button.clicked.connect(self.update_record)
        self.delete_button.clicked.connect(self.delete_record)
        clear_button.clicked.connect(self.clear_inputs)

        right_panel.addLayout(buttons_layout)

        main_layout.addWidget(table_container, stretch=2)
        main_layout.addLayout(right_panel, stretch=1)
        self.setLayout(main_layout)

    def refresh_table(self):
        data = self.db.get_table_data(self.table)
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(self.columns))
        self.table_widget.setHorizontalHeaderLabels([col[0] for col in self.columns])

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                col_name = self.columns[col_idx][0]
                if col_name in self.relationships:
                    ref_table, ref_column = self.relationships[col_name]
                    ref_columns = self.db.get_table_columns(ref_table)
                    display_col = self.db.find_display_column(ref_table)
                    self.cursor = self.db.conn.cursor()
                    self.cursor.execute(
                        f"SELECT \"{display_col}\" FROM \"{ref_table}\" WHERE \"{ref_column}\" = ?",
                        (value,)
                    )
                    display_value = self.cursor.fetchone()
                    display_value = display_value[0] if display_value else f"Неизвестно ({value})"
                else:
                    display_value = str(value)
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(display_value))
        self.table_widget.resizeColumnsToContents()

    def on_cell_clicked(self, row, column):
        pk_index = [col[0] for col in self.columns].index(self.pk_column)
        self.selected_pk_value = self.table_widget.item(row, pk_index).text()

        for col_idx, col in enumerate(self.columns):
            col_name = col[0]
            if col_name.lower() == "код" or col_name not in self.inputs:
                continue

            cell_value = self.table_widget.item(row, col_idx).text()
            input_widget = self.inputs[col_name]

            if col_name in self.relationships:
                ref_table, ref_column = self.relationships[col_name]
                display_col = self.db.find_display_column(ref_table)
                self.cursor = self.db.conn.cursor()
                self.cursor.execute(
                    f"SELECT \"{ref_column}\" FROM \"{ref_table}\" WHERE \"{display_col}\" = ?",
                    (cell_value,)
                )
                fk_value = self.cursor.fetchone()
                fk_value = fk_value[0] if fk_value else None

                if fk_value is not None:
                    combo_box = input_widget
                    index = combo_box.findData(fk_value)
                    if index >= 0:
                        combo_box.setCurrentIndex(index)
                    else:
                        combo_box.setCurrentIndex(0)
            else:
                input_widget.setText(cell_value)

    def add_record(self):
        data = {}
        for col in self.columns:
            col_name = col[0]
            if col_name.lower() == "код" or col_name not in self.inputs:
                continue
            input_widget = self.inputs[col_name]
            if isinstance(input_widget, QComboBox):
                value = input_widget.currentData()
            else:
                value = input_widget.text()
            data[col_name] = value

        try:
            self.db.insert(self.table, data)
            self.refresh_table()
            self.clear_inputs()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить запись: {str(e)}")

    def update_record(self):
        if not self.selected_pk_value:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите запись, щелкнув по строке")
            return

        data = {}
        for col in self.columns:
            col_name = col[0]
            if col_name.lower() == "код" or col_name == self.pk_column or col_name not in self.inputs:
                continue
            input_widget = self.inputs[col_name]
            if isinstance(input_widget, QComboBox):
                value = input_widget.currentData()
            else:
                value = input_widget.text()
            data[col_name] = value

        try:
            self.db.update(self.table, self.pk_column, self.selected_pk_value, data)
            self.refresh_table()
            self.clear_inputs()
            self.selected_pk_value = None
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить запись: {str(e)}")

    def delete_record(self):
        if not self.selected_pk_value:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите запись, щелкнув по строке")
            return

        try:
            self.db.delete(self.table, self.pk_column, self.selected_pk_value)
            self.refresh_table()
            self.clear_inputs()
            self.selected_pk_value = None
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить запись: {str(e)}")

    def clear_inputs(self):
        for col_name, input_widget in self.inputs.items():
            if isinstance(input_widget, QLineEdit):
                input_widget.clear()
            elif isinstance(input_widget, QComboBox):
                input_widget.setCurrentIndex(0)

class MainWindow(QMainWindow):
    logout_signal = Signal()  # Сигнал для уведомления о выходе

    def __init__(self, db: Database, is_admin: bool):
        super().__init__()
        self.db = db
        self.is_admin = is_admin
        self.setWindowTitle("Управление базой данных")
        self.setMinimumSize(800, 600)

        # Основной стиль для главного окна
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E6F7FA;
                font-family: Arial;
            }
            QComboBox {
                border: 1px solid #4A90E2;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFFFF;
                color: #333333;
            }
            QPushButton {
                background-color: #4A90E2;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7AB8F5;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Боковая панель (слева)
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)

        # Выбор таблицы
        table_selection_layout = QVBoxLayout()
        header_label = QLabel("Выберите таблицу:")
        self.table_selector = QComboBox()
        self.table_selector.addItems(self.db.get_tables())
        table_selection_layout.addWidget(header_label)
        table_selection_layout.addWidget(self.table_selector)
        sidebar.addLayout(table_selection_layout)

        # Кнопки
        import_excel_button = QPushButton("Импортировать из Excel")
        logout_button = QPushButton("Выйти")
        import_excel_button.clicked.connect(self.import_from_excel)
        logout_button.clicked.connect(self.logout)
        sidebar.addWidget(import_excel_button)
        sidebar.addWidget(logout_button)

        # Панель администратора (доступна только админам)
        if self.is_admin:
            admin_frame = QFrame()
            admin_frame.setStyleSheet("""
                QFrame {
                    background-color: #D6EAF8;
                    border: 1px solid #4A90E2;
                    border-radius: 5px;
                    padding: 10px;
                }
            """)
            admin_layout = QVBoxLayout()
            manage_users_button = QPushButton("Управление пользователями")
            manage_users_button.clicked.connect(self.manage_users)
            admin_layout.addWidget(manage_users_button)
            admin_frame.setLayout(admin_layout)
            sidebar.addWidget(admin_frame)

        sidebar.addStretch()

        # Основная область для таблицы
        self.table_container = QWidget()
        self.table_layout = QVBoxLayout(self.table_container)

        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.table_container, stretch=1)

        self.table_selector.currentTextChanged.connect(self.load_table)
        if self.db.get_tables():
            self.load_table(self.db.get_tables()[0])

    def load_table(self, table: str):
        while self.table_layout.count():
            item = self.table_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            
        table_editor = TableEditor(self.db, table, self.is_admin)
        self.table_layout.addWidget(table_editor)

    def manage_users(self):
        self.user_manager = UserManager(self.db)
        self.user_manager.show()

    def import_from_excel(self):
        table = self.table_selector.currentText()
        if not table:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите таблицу")
            return

        self.db.print_table_schema(table)
        columns = self.db.get_table_columns(table)
        column_names = [col[0] for col in columns]
        column_types = {col[0]: col[1] for col in columns}
        pk_column = self.db.get_primary_key(table)
        relationships = self.db.get_relationships(table)
        print(f"Связи для таблицы {table}: {relationships}")

        for col, (ref_table, ref_column) in relationships.items():
            print(f"Проверка схемы для связанной таблицы {ref_table}")
            self.db.print_table_schema(ref_table)
            self.db.cursor.execute(f"SELECT * FROM \"{ref_table}\"")
            print(f"Текущие данные в {ref_table}: {self.db.cursor.fetchall()}")

        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл Excel", "", "Файлы Excel (*.xlsx *.xls)")
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            excel_columns = df.columns.tolist()
            print(f"Столбцы Excel: {excel_columns}")
            print(f"Исходные значения для 'Тип партнера': {df.get('Тип партнера', pd.Series()).tolist()}")

            excel_columns_normalized = []
            for col in excel_columns:
                if ';' in col:
                    col_parts = col.split(';')
                    excel_columns_normalized.append(col_parts[0])
                else:
                    excel_columns_normalized.append(col)

            excel_columns_lower = [col.lower() for col in excel_columns_normalized]
            table_columns_lower = [col.lower() for col in column_names]

            matching_columns = []
            column_mapping = {}
            for i, excel_col_lower in enumerate(excel_columns_lower):
                for j, table_col_lower in enumerate(table_columns_lower):
                    if excel_col_lower == table_col_lower and table_col_lower != "код":
                        matching_columns.append(column_names[j])
                        column_mapping[excel_columns[i]] = column_names[j]
                        break

            if not matching_columns:
                QMessageBox.warning(self, "Ошибка", "Совпадающие столбцы между Excel и таблицей не найдены")
                return

            df.rename(columns=column_mapping, inplace=True)
            df = df[matching_columns]

            for col in matching_columns:
                if col in relationships:
                    df[col] = df[col].apply(lambda x: str(x).strip() if pd.notnull(x) else '')
                    print(f"Очищенные значения для {col} (внешний ключ): {df[col].tolist()}")
                    print(f"Типы для {col} (внешний ключ): {df[col].apply(type).tolist()}")

                    ref_table, ref_column = relationships[col]
                    display_col = self.db.find_display_column(ref_table)
                    print(f"Преобразование {col}: ref_table={ref_table}, ref_column={ref_column}, display_col={display_col}")

                    transformed_values = []
                    for idx, x in enumerate(df[col]):
                        print(f"Обработка значения {idx}: {x!r} (тип: {type(x)})")
                        if x and isinstance(x, str) and x.strip():
                            result = self.db.add_related_value(ref_table, display_col, ref_column, x)
                            print(f"Результат для {x}: {result}")
                            transformed_values.append(result)
                        else:
                            print(f"Пропуск пустого или некорректного значения: {x!r}")
                            transformed_values.append(None)
                    df[col] = transformed_values
                    print(f"Преобразованные значения для {col}: {transformed_values}")

            for col in matching_columns:
                if col in relationships:
                    continue
                col_type = column_types[col].upper()
                if col_type.startswith('INT') or col_type.startswith('REAL'):
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).infer_objects(copy=False)
                    print(f"Числовые значения для {col}: {df[col].tolist()}")
                else:
                    df[col] = df[col].apply(lambda x: str(x).strip() if pd.notnull(x) else '')
                    print(f"Очищенные значения для {col}: {df[col].tolist()}")
                print(f"Типы для {col}: {df[col].apply(type).tolist()}")

            data = df.to_dict('records')
            print(f"Данные для вставки: {data}")

            inserted_rows = 0
            skipped_rows = []
            for row in data:
                if any(row[col] is None for col in matching_columns if col in relationships):
                    skipped_rows.append(row)
                    print(f"Пропуск строки из-за отсутствия значения в связанном поле: {row}")
                    continue
                for col in matching_columns:
                    if row[col] is None:
                        col_type = column_types[col].upper()
                        row[col] = 0 if col_type.startswith('INT') or col_type.startswith('REAL') else ''
                self.db.insert(table, row)
                inserted_rows += 1

            for col, (ref_table, ref_column) in relationships.items():
                self.db.cursor.execute(f"SELECT * FROM \"{ref_table}\"")
                print(f"Итоговые данные в {ref_table}: {self.db.cursor.fetchall()}")

            message = f"Данные успешно импортированы в таблицу {table} (совпавшие столбцы: {matching_columns}, добавлено строк: {inserted_rows})"
            if skipped_rows:
                message += f"\nПропущено {len(skipped_rows)} строк из-за некорректных значений внешних ключей."
                print(f"Пропущенные строки: {skipped_rows}")
            QMessageBox.information(self, "Успех", message)
            self.load_table(table)

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось импортировать данные: {str(e)}")

    def logout(self):
        self.close()
        self.logout_signal.emit()

def main():
    app = QApplication(sys.argv)
    db = Database("database.db")

    while True:
        login_dialog = LoginDialog()
        if not login_dialog.exec():
            break  # Пользователь закрыл окно входа

        username = login_dialog.username_input.text()
        password = login_dialog.password_input.text()
        
        auth_result, is_admin = db.authenticate(username, password)
        if not auth_result:
            QMessageBox.warning(None, "Ошибка", "Неверные учетные данные")
            continue

        window = MainWindow(db, is_admin)
        window.show()

        # Создаем флаг для отслеживания выхода
        logout_flag = False

        def on_logout():
            nonlocal logout_flag
            logout_flag = True

        window.logout_signal.connect(on_logout)
        
        # Запускаем цикл обработки событий
        app.exec()

        if not logout_flag:
            break  # Пользователь закрыл окно, выходим из цикла

    sys.exit(0)

if __name__ == "__main__":
    main()