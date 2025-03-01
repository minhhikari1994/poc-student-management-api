import click
from flask import Blueprint

from ..models.base import db
from ..models import UserAccount

from ..services.user_account import reset_user_password, create_user_account_from_cli

user_commands_bp = Blueprint('user_commands', __name__)

@user_commands_bp.cli.command('create')
@click.argument('login_id')
@click.argument('is_admin', default=False)
def create(login_id, is_admin):
    result, message = create_user_account_from_cli(login_id, is_admin)
    if result:
        db.session.commit()
        print(f'Success, password for the account is: {message}')
    else:
        print(message)

@user_commands_bp.cli.command('resetpw')
@click.argument('login_id')
def resetpw(login_id):
    existing_account = UserAccount.query.filter_by(login_id=login_id).first()
    if existing_account is None:
        print('Login id does not exist')
        return
    result, new_password = reset_user_password(existing_account)
    if result:
        db.session.commit()
        print(f'Success, new password is: {new_password}')
    else:
        print('Failed to reset password')