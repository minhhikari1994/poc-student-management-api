"""add test score table

Revision ID: 513c3ca4197e
Revises: cae2660f9e77
Create Date: 2025-01-31 13:59:34.093971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '513c3ca4197e'
down_revision = 'cae2660f9e77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_scores',
    sa.Column('test_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.UUID(), nullable=False),
    sa.Column('score', sa.Numeric()),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.ForeignKeyConstraint(['test_id'], ['tests.id'], ),
    sa.PrimaryKeyConstraint('test_id', 'student_id')
    )
    # ### end Alembic commands ###
    op.execute("COMMIT")

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_scores')
    # ### end Alembic commands ###
    op.execute("COMMIT")
