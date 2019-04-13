"""empty message

Revision ID: e0152c53a368
Revises: f50cc6b6ed52
Create Date: 2019-04-12 15:40:19.954368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0152c53a368'
down_revision = 'f50cc6b6ed52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('file_name', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photos', 'file_name')
    # ### end Alembic commands ###