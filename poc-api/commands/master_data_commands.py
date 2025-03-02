import click
from flask import Blueprint

from ..services.data_import import import_master_data_from_excel

master_data_cli_bp = Blueprint('master_data_cli_bp', __name__)

@master_data_cli_bp.cli.command('import')
@click.argument('file_path')
def import_master_data(file_path):
    master_excel_file = open(file_path, 'rb')
    result = import_master_data_from_excel(master_excel_file)
    if result:
        print('Success')
    else:
        print('Failed')

