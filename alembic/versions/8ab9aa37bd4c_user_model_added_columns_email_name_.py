"""user model: added columns email, name, surname

Revision ID: 8ab9aa37bd4c
Revises: 6a273c26d7d3
Create Date: 2021-12-08 00:05:28.560204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ab9aa37bd4c'
down_revision = '6a273c26d7d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(), nullable=True))
    op.add_column('user', sa.Column('name', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('surname', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'surname')
    op.drop_column('user', 'name')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
