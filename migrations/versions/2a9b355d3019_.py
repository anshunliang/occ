"""empty message

Revision ID: 2a9b355d3019
Revises: edc3358b27e2
Create Date: 2020-05-08 22:24:18.931350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a9b355d3019'
down_revision = 'edc3358b27e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('admin_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'admin', ['admin_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'admin_id')
    # ### end Alembic commands ###
