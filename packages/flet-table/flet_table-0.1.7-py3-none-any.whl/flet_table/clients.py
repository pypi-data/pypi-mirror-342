import flet as ft
from database import Database

db = Database()

def main(page: ft.Page):
    page.title = 'Управление клиентами'
    page.scroll = "AUTO"
    page.padding = 20

    # Текст для вывода результата
    result_text = ft.Text(value="", size=16)

    # Поля ввода
    fio_input = ft.TextField(label="ФИО", width=300)
    login_input = ft.TextField(label="Логин", width=300)
    password_input = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=300)
    id_order_input = ft.TextField(label="ID заказа", width=300)

    selected_client_id = None

    # Обновление таблицы клиентов
    def refresh_clients():
        try:
            conn = db.connect()
            with conn.cursor() as cur:
                cur.execute("SELECT id, fio, login, password, id_order FROM client")
                rows = cur.fetchall()

                table_rows = []
                for row in rows:
                    row_id, fio, login, password, id_order = row
                    table_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(row_id))),
                                ft.DataCell(ft.Text(fio)),
                                ft.DataCell(ft.Text(login)),
                                ft.DataCell(ft.Text(password)),
                                ft.DataCell(ft.Text(str(id_order))),
                                ft.DataCell(ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, r=row: edit_client(r))),
                                ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, r=row: delete_client(r[0]))),
                            ]
                        )
                    )
                data_table.rows = table_rows
                page.update()
        finally:
            if conn:
                conn.close()

    # Добавление или обновление клиента
    def save_client(e):
        nonlocal selected_client_id
        fio = fio_input.value.strip()
        login = login_input.value.strip()
        password = password_input.value.strip()
        id_order = id_order_input.value.strip()

        if not all([fio, login, password]):
            result_text.value = "⚠️ Заполните все обязательные поля"
            result_text.color = "red"
            page.update()
            return

        try:
            conn = db.connect()
            with conn.cursor() as cur:
                if selected_client_id:  # Редактирование
                    cur.execute("""
                        UPDATE client
                        SET fio = %s, login = %s, password = %s, id_order = %s
                        WHERE id = %s
                    """, (fio, login, password, id_order or None, selected_client_id))
                    result_text.value = "✅ Клиент обновлён"
                else:
                    cur.execute("""
                        INSERT INTO client (fio, login, password, id_order)
                        VALUES (%s, %s, %s, %s)
                    """, (fio, login, password, id_order or None))
                    result_text.value = "✅ Клиент добавлен"

                conn.commit()
                result_text.color = "green"
        except Exception as ex:
            result_text.value = f"❌ Ошибка: {ex}"
            result_text.color = "red"
        finally:
            if conn:
                conn.close()
            clear_inputs()
            refresh_clients()
            page.update()

    # Удаление клиента
    def delete_client(client_id):
        try:
            conn = db.connect()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM client WHERE id = %s", (client_id,))
                conn.commit()
                result_text.value = "🗑️ Клиент удалён"
                result_text.color = "green"
        except Exception as ex:
            result_text.value = f"❌ Ошибка удаления: {ex}"
            result_text.color = "red"
        finally:
            if conn:
                conn.close()
            refresh_clients()
            page.update()

    # Редактирование клиента
    def edit_client(row):
        nonlocal selected_client_id
        selected_client_id = row[0]
        fio_input.value = row[1]
        login_input.value = row[2]
        password_input.value = row[3]
        id_order_input.value = str(row[4]) if row[4] is not None else ""
        result_text.value = f"✏️ Режим редактирования клиента ID {selected_client_id}"
        result_text.color = "blue"
        page.update()

    # Очистка полей
    def clear_inputs():
        nonlocal selected_client_id
        selected_client_id = None
        fio_input.value = ""
        login_input.value = ""
        password_input.value = ""
        id_order_input.value = ""
        page.update()

    # Таблица клиентов
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("ФИО")),
            ft.DataColumn(ft.Text("Логин")),
            ft.DataColumn(ft.Text("Пароль")),
            ft.DataColumn(ft.Text("ID заказа")),
            ft.DataColumn(ft.Text("Редакт.")),
            ft.DataColumn(ft.Text("Удалить")),
        ],
        rows=[]
    )

    # Кнопки
    save_button = ft.ElevatedButton("💾 Сохранить", on_click=save_client)
    clear_button = ft.OutlinedButton("🔄 Очистить", on_click=lambda e: clear_inputs())

    # Интерфейс
    page.add(
        ft.Column(
            controls=[
                ft.Text("🧑 Управление таблицей Клиентов", size=22, weight=ft.FontWeight.BOLD),
                fio_input,
                login_input,
                password_input,
                id_order_input,
                ft.Row([save_button, clear_button]),
                result_text,
                ft.Divider(),
                data_table,
            ],
            spacing=15
        )
    )

    refresh_clients()

ft.app(target=main)
