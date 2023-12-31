"""add op _user_name_and_password

Revision ID: 9c133083e714
Revises: f015625a017b
Create Date: 2023-06-30 17:01:00.146997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c133083e714'
down_revision = 'f015625a017b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('password', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_column('password')
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###
