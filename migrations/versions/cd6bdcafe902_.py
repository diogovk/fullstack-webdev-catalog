"""empty message

Revision ID: cd6bdcafe902
Revises: 6f1d6055c55c
Create Date: 2016-02-25 12:09:52.480243

"""

# revision identifiers, used by Alembic.
revision = 'cd6bdcafe902'
down_revision = '6f1d6055c55c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.add_column(u'item', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'item', 'user', ['user_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.drop_column(u'item', 'user_id')
    op.drop_table('user')
    ### end Alembic commands ###