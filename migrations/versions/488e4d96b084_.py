"""empty message

Revision ID: 488e4d96b084
Revises: cd6bdcafe902
Create Date: 2016-02-26 16:10:12.656669

"""

# revision identifiers, used by Alembic.
revision = '488e4d96b084'
down_revision = 'cd6bdcafe902'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'item_user_id_fkey', 'item', type_='foreignkey')
    op.create_foreign_key(None, 'item', 'user', ['owner_id'], ['id'])
    op.drop_column('item', 'user_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.create_foreign_key(u'item_user_id_fkey', 'item', 'user', ['user_id'], ['id'])
    op.drop_column('item', 'owner_id')
    ### end Alembic commands ###
