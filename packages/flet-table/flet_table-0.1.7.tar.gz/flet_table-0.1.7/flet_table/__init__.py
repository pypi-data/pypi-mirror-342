from auth import auth_page

from flet_table.edit_table import create_editable_table
from flet_table.elements import (
    datetime_input,
    dropdown,
    get_alert_dialog,
    get_date_picker,
    get_error_banner,
    get_switch,
    get_tabs,
    get_time_picker,
    low_page_alert_dialog,
    radio_group,
)
from flet_table.hash_pass_functools import get_password_hash, validate_password
from flet_table.table import create_flet_table, create_image_table

__version__ = '1.0.7'
