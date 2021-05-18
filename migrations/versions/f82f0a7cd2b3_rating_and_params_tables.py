"""rating and params tables

Revision ID: f82f0a7cd2b3
Revises: c006771b60fc
Create Date: 2021-04-24 13:26:18.663100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f82f0a7cd2b3'
down_revision = 'c006771b60fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('formulas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fl_name', sa.String(length=200), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_formulas_fl_name'), 'formulas', ['fl_name'], unique=False)
    op.create_table('parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('formula', sa.String(length=1024), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('par_name', sa.String(length=200), nullable=True),
    sa.Column('flag_max', sa.Integer(), nullable=True),
    sa.Column('flag_min', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parameters_par_name'), 'parameters', ['par_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_parameters_par_name'), table_name='parameters')
    op.drop_table('parameters')
    op.drop_index(op.f('ix_formulas_fl_name'), table_name='formulas')
    op.drop_table('formulas')
    # ### end Alembic commands ###
