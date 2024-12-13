"""empty message

Revision ID: 6998b14f6c72
Revises: 5cfd3121546f
Create Date: 2024-09-16 22:05:18.212553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6998b14f6c72'
down_revision = '5cfd3121546f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mozoCaller',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_mesa', sa.Integer(), nullable=False),
    sa.Column('solicitado', sa.DateTime(), nullable=False),
    sa.Column('atendido', sa.Boolean(), nullable=True),
    sa.Column('hentrega', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mozoCaller')
    # ### end Alembic commands ###