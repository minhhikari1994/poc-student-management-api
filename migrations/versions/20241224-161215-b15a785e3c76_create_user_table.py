"""Create user table

Revision ID: b15a785e3c76
Revises: 
Create Date: 2024-12-24 16:12:15.712580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b15a785e3c76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_account',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('login_id', sa.String(length=100), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_account')
    # ### end Alembic commands ###
