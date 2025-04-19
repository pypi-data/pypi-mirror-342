import flet as ft
import psycopg2  # Или другой драйвер БД

def create_editable_table(
    data: list[tuple],
    columns: list[str],
    on_edit: callable = None,
    on_delete: callable = None
) -> ft.DataTable:
    """
    Создает редактируемую таблицу с кнопками удаления
    :param data: Список кортежей с данными (первый элемент - ID записи)
    :param columns: Названия колонок (первая - 'ID')
    :param on_edit: Функция для сохранения изменений (id, column_name, new_value)
    :param on_delete: Функция для удаления записи (id)
    """
    rows = []
    for row in data:
        record_id = row[0]  # Получаем ID из первой колонки
        
        # Создаем ячейки таблицы
        cells = [
            # Нередактируемый ID
            ft.DataCell(ft.Text(str(record_id))),
            
            # Редактируемые поля (кроме ID)
            *(ft.DataCell(
                ft.TextField(
                    value=str(val),
                    border=ft.InputBorder.NONE,
                    on_change=lambda e, id=record_id, col=col: on_edit(id, col, e.value)
                )
            ) for col, val in zip(columns[1:], row[1:]))
        ]
        
        # Кнопка удаления
        cells.append(ft.DataCell(
            ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Удалить запись",
                on_click=lambda e, id=record_id: on_delete(id)
            )
        ))
        
        rows.append(ft.DataRow(cells=cells))
    
    return ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in columns] + [ft.DataColumn(ft.Text("Действия"))],
        rows=rows,
        border=ft.border.all(1),
    )

# Пример реализации функций для работы с БД
def main(page: ft.Page):
    # Подключение к БД (пример для PostgreSQL)
    conn = psycopg2.connect(
        dbname="your_db",
        user="user",
        password="pass",
        host="localhost"
    )
    cursor = conn.cursor()

    def handle_edit(record_id: int, column_name: str, new_value: str):
        """Обновляет запись в базе данных"""
        try:
            # Важно! Используем параметризованные запросы для безопасности
            cursor.execute(
                f"UPDATE your_table SET {column_name} = %s WHERE id = %s",
                (new_value, record_id)
            )
            conn.commit()
            print(f"Запись {record_id} обновлена: {column_name} = {new_value}")
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при обновлении: {e}")

    def handle_delete(record_id: int):
        """Удаляет запись из базы данных"""
        try:
            cursor.execute(
                "DELETE FROM your_table WHERE id = %s",
                (record_id,)
            )
            conn.commit()
            print(f"Запись {record_id} удалена")
            
            # Обновляем интерфейс после удаления
            page.update()
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при удалении: {e}")

    # Пример данных (в реальном приложении получаем из БД)
    data = [
        (1, "Иван", "ivan@mail.com", 25),
        (2, "Мария", "maria@mail.com", 30),
        (3, "Алексей", "alex@mail.com", 28)
    ]
    columns = ["ID", "Имя", "Email", "Возраст"]

    # Создаем и добавляем таблицу
    page.add(
        create_editable_table(
            data=data,
            columns=columns,
            on_edit=handle_edit,
            on_delete=handle_delete
        )
    )

    # Закрытие соединения при выходе
    def on_close(e):
        cursor.close()
        conn.close()
    page.on_close = on_close

ft.app(target=main)