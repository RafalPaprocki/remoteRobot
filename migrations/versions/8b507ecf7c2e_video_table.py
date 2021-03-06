"""video table

Revision ID: 8b507ecf7c2e
Revises: bd1738e2a72b
Create Date: 2019-11-20 21:10:47.866780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b507ecf7c2e'
down_revision = 'bd1738e2a72b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('preview_frame', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    # ### end Alembic commands ###
