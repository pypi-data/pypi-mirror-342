import flet as ft
from database import Database
from flet_table import create_flet_table

db = Database()

def main(page: ft.Page):
    page.title = 'Окно авторизации'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # page.scroll = "AUTO"
    login_input = ft.TextField(label='Введите логин', width=400)
    password_input = ft.TextField(label='Введите пароль', width=400)
    result_text = ft.Text('', color='red', size=16)
    greet_text = ft.Text('Добрый день, пройдите авторизацию', size=20)
    page.update()


    def check_auth(e):
        login = login_input.value.strip()
        password = password_input.value.strip()

        if not password or not login:
            result_text.value = 'Введите данные для авторизации'
            page.update()
            return
        
        try:
            conn = db.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    '''
                        SELECT * FROM user WHERE login = %s AND password = %s;
                    ''', (login, password)
                )
                user = cursor.fetchall()
                print(user)
                if user:
                    if user[0][10] == 1:
                        show_manager_page(user)
                    elif user[0][10] == 2:
                        show_client_page(user)
                else:
                    result_text.value = 'Неверный логин или пароль'
                    page.update()
        except Exception as ex:
            result_text.value = f'Ошибка {ex}'
            page.update()
        finally:
            if conn:
                conn.close()


    def show_manager_page(data):
        page.clean()
        page.title = 'Окно менеджера'
        greet_manager = ft.Text(f'Добро пожаловать, {data[0][2]} {data[0][1]} {data[0][3]}!', size=20, color='green')
        back_button = ft.ElevatedButton('Назад', on_click=show_main_page)
        result_text = ft.Text('', color='red')

        selected_deal_id = None

        type_credit_dropdown = ft.Dropdown(label="Тип кредита", width=300)
        status_dropdown = ft.Dropdown(label="Статус заявки", width=300)

        def get_dropdown_options():
            try:
                conn = db.connect()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, name_type FROM type_credit")
                    type_credit_dropdown.options = [ft.dropdown.Option(str(row[0]), row[1]) for row in cursor.fetchall()]
                    cursor.execute("SELECT id, name_status FROM deal_status")
                    status_dropdown.options = [ft.dropdown.Option(str(row[0]), row[1]) for row in cursor.fetchall()]
            finally:
                if conn:
                    conn.close()

        def get_deal_data():
            try:
                conn = db.connect()
                with conn.cursor() as cursor:
                    cursor.execute(
                        '''
                        SELECT
                            dd.id,
                            u.name,
                            u.surname,
                            u.second_surname,
                            tc.name_type,
                            dd.start_date_deal,
                            ds.name_status
                        FROM
                            deal_document dd
                        JOIN
                            user u ON dd.id_client = u.id
                        JOIN
                            type_credit tc ON dd.id_type_credit = tc.id
                        JOIN
                            deal_status ds ON dd.id_status = ds.id;
                        '''
                    )
                    return cursor.fetchall()
            finally:
                if conn:
                    conn.close()

        def refresh_deals_table():
            data = get_deal_data()
            rows = []

            for row in data:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row[0]))),
                            ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(row[2])),
                            ft.DataCell(ft.Text(row[3])),
                            ft.DataCell(ft.Text(row[4])),
                            ft.DataCell(ft.Text(str(row[5]))),
                            ft.DataCell(ft.Text(row[6])),
                            ft.DataCell(ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, deal_id=row[0]: edit_deal(deal_id))),
                            ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, deal_id=row[0]: delete_deal(deal_id))),
                        ]
                    )
                )
            deals_table.rows = rows
            page.update()

        def edit_deal(deal_id):
            nonlocal selected_deal_id
            selected_deal_id = deal_id
            result_text.value = f"Редактирование заявки ID: {deal_id}"
            page.update()

        def delete_deal(deal_id):
            try:
                conn = db.connect()
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM deal_document WHERE id = %s", (deal_id,))
                    conn.commit()
                result_text.value = f"Удалено ID: {deal_id}"
                result_text.color = "green"
            except Exception as ex:
                result_text.value = f"Ошибка удаления: {ex}"
                result_text.color = "red"
            finally:
                if conn:
                    conn.close()
                refresh_deals_table()
                page.update()

        def update_deal(e):
            nonlocal selected_deal_id
            if not selected_deal_id:
                result_text.value = "Выберите заявку для редактирования"
                page.update()
                return

            try:
                conn = db.connect()
                with conn.cursor() as cursor:
                    cursor.execute(
                        '''
                        UPDATE deal_document
                        SET id_type_credit = %s, id_status = %s
                        WHERE id = %s;
                        ''',
                        (type_credit_dropdown.value, status_dropdown.value, selected_deal_id)
                    )
                    conn.commit()
                result_text.value = "✅ Заявка обновлена"
                result_text.color = "green"
                selected_deal_id = None
            except Exception as ex:
                result_text.value = f"Ошибка обновления: {ex}"
                result_text.color = "red"
            finally:
                if conn:
                    conn.close()
                refresh_deals_table()
                page.update()

        deals_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Имя")),
                ft.DataColumn(ft.Text("Фамилия")),
                ft.DataColumn(ft.Text("Отчество")),
                ft.DataColumn(ft.Text("Тип кредита")),
                ft.DataColumn(ft.Text("Дата начала")),
                ft.DataColumn(ft.Text("Статус")),
                ft.DataColumn(ft.Text("✏️")),
                ft.DataColumn(ft.Text("🗑️")),
            ],
            rows=[],
        )

        save_button = ft.ElevatedButton("Сохранить изменения", on_click=update_deal)

        get_dropdown_options()
        refresh_deals_table()

        page.add(
            ft.Column(
                [
                    greet_manager,
                    result_text,
                    deals_table,
                    ft.Row([type_credit_dropdown, status_dropdown]),
                    ft.Row([save_button, back_button]),
                ],
                scroll=ft.ScrollMode.ALWAYS,
            )
        )
        page.update()

    def show_client_page(data):
        page.clean()
        page.title = 'Окно клиента'
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        greet_client = ft.Text(f'Добро пожаловать, {data[0][2]} {data[0][1]} {data[0][3]}!', size=20, color='green')
        back_button = ft.ElevatedButton('Назад', on_click=show_main_page)

        try:
            conn = db.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    '''
                        SELECT
                            dd.id,
                            u.name,
                            u.surname,
                            u.second_surname,
                            tc.name_type,
                            dd.start_date_deal,
                            ds.name_status
                        FROM
                            deal_document dd
                        JOIN
                            user u ON dd.id_client = u.id
                        JOIN
                            type_credit tc ON dd.id_type_credit = tc.id
                        JOIN
                            deal_status ds ON dd.id_status = ds.id
                        WHERE
                            dd.id_client = %s;
                    ''', (data[0][0])
                )
                data_info = cursor.fetchall()
        except Exception as ex:
            result_text.value = f'Ошибка {ex}'
            page.update()
        finally:
            if conn:
                conn.close()

        table_deal_document = create_flet_table(data_info, ['id', 'name', 'surname', 'second_surname', 'name_type', 'start_date_deal', 'name_status'])

        page.add(
            ft.Column(
                [
                    greet_client,
                    table_deal_document,
                    back_button,
                ],
            ),
        )
        page.update()

    def show_main_page(e: None):
        page.clean()
        page.title = 'Окно авторизации'
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        login_input.value = ''
        password_input.value = ''
        result_text.value = ''
        greet_text = ft.Text('Добрый день, пройдите авторизацию', size=20)
        page.update()

        auth_button = ft.ElevatedButton('Авторизаваться', on_click=check_auth)

        page.add(
            ft.Column(
                [
                    ft.Row(
                        [greet_text],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    login_input,
                    password_input,
                    auth_button,
                    result_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()
    

    auth_button = ft.ElevatedButton('Авторизаваться', on_click=check_auth)

    page.add(
        ft.Column(
            [
                ft.Row(
                    [greet_text],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                login_input,
                password_input,
                auth_button,
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()

ft.app(target=main)