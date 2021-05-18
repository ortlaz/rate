"""empty message

Revision ID: 8958d07873c3
Revises: 35b68b99e501
Create Date: 2021-05-18 17:16:06.016217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8958d07873c3'
down_revision = '35b68b99e501'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('formulas', sa.Column('formula', sa.String(length=1024), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('formulas', 'formula')
    # ### end Alembic commands ###
