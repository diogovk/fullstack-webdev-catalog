"""empty message

Revision ID: 1037bccd1a88
Revises: ae0fe96601f2
Create Date: 2016-01-02 13:25:59.126958

"""

# revision identifiers, used by Alembic.
revision = '1037bccd1a88'
down_revision = 'ae0fe96601f2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('image_file', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'image_file')
    ### end Alembic commands ###
