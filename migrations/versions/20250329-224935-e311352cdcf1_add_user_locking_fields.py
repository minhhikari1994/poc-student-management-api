"""add user locking fields

Revision ID: e311352cdcf1
Revises: 513c3ca4197e
Create Date: 2025-03-29 22:49:35.649346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e311352cdcf1'
down_revision = '513c3ca4197e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_locked', sa.Boolean(), server_default='false', nullable=False))
        batch_op.add_column(sa.Column('failed_login_count', sa.Integer(), server_default='0', nullable=False))

    # ### end Alembic commands ###
    op.execute("COMMIT")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.drop_column('failed_login_count')
        batch_op.drop_column('is_locked')

    # ### end Alembic commands ###
    op.execute("COMMIT")
