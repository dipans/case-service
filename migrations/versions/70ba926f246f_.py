"""empty message

Revision ID: 70ba926f246f
Revises: 
Create Date: 2020-01-30 01:53:46.279546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70ba926f246f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('case',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('received_date', sa.DateTime(), nullable=False),
    sa.Column('comments', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('case')
    # ### end Alembic commands ###
