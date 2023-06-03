"""add url for media

Revision ID: 1455980480e9
Revises: cf9dbee89d33
Create Date: 2023-05-23 15:48:04.131278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1455980480e9'
down_revision = 'cf9dbee89d33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mediafile', sa.Column('url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mediafile', 'url')
    # ### end Alembic commands ###