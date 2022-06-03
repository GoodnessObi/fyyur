"""empty message

Revision ID: 0aa89fa3f6df
Revises: 0485684df3f1
Create Date: 2022-06-03 18:48:30.508696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aa89fa3f6df'
down_revision = '0485684df3f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('date_created', sa.DateTime(), nullable=False))
    op.add_column('artists', sa.Column('date_updated', sa.DateTime(), nullable=True))
    op.add_column('venues', sa.Column('date_created', sa.DateTime(), nullable=False))
    op.add_column('venues', sa.Column('date_updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'date_updated')
    op.drop_column('venues', 'date_created')
    op.drop_column('artists', 'date_updated')
    op.drop_column('artists', 'date_created')
    # ### end Alembic commands ###