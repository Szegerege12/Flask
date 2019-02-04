"""new fields in user model

Revision ID: 705172aacaf1
Revises: f2b1a02fa2c8
Create Date: 2019-01-30 15:08:04.359749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '705172aacaf1'
down_revision = 'f2b1a02fa2c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###