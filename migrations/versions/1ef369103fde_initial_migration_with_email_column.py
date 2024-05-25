"""Initial migration with email column

Revision ID: 1ef369103fde
Revises: 
Create Date: 2024-05-15 06:04:25.187939

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1ef369103fde'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint('uq_users_email', ['email'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_email', type_='unique')
        batch_op.drop_column('email')
    # ### end Alembic commands ###


    # ### end Alembic commands ###
