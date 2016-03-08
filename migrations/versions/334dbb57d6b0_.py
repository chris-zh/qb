"""empty message

Revision ID: 334dbb57d6b0
Revises: 2eb7cddf18ae
Create Date: 2016-03-08 22:29:25.631729

"""

# revision identifiers, used by Alembic.
revision = '334dbb57d6b0'
down_revision = '2eb7cddf18ae'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('big_image', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('small_image', sa.Text(), nullable=True))
    op.drop_column('users', 'personal_gravatar')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('personal_gravatar', sa.TEXT(), nullable=True))
    op.drop_column('users', 'small_image')
    op.drop_column('users', 'big_image')
    ### end Alembic commands ###
