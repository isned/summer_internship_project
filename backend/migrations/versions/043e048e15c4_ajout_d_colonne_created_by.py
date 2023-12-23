"""ajout d colonne created_by

Revision ID: 043e048e15c4
Revises: 208d186820bd
Create Date: 2023-08-21 14:46:08.835766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '043e048e15c4'
down_revision = '208d186820bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('database_user', schema=None) as batch_op:
        batch_op.drop_index('username')

    op.drop_table('database_user')
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.drop_column('created_by')

    op.create_table('database_user',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='latin1_swedish_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('database_user', schema=None) as batch_op:
        batch_op.create_index('username', ['username'], unique=False)

    # ### end Alembic commands ###
