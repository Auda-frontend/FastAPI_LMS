"""Create students, admins, books, and book_issues tables

Revision ID: 135cc480a490
Revises: a99d45463b65
Create Date: 2024-11-26 07:34:55.387375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '135cc480a490'
down_revision: Union[str, None] = 'a99d45463b65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
