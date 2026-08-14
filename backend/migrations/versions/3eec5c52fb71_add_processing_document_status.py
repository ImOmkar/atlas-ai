"""add processing document status

Revision ID: 3eec5c52fb71
Revises: ecce98ef2634
Create Date: 2026-08-01 10:19:04.354202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eec5c52fb71'
down_revision: Union[str, Sequence[str], None] = 'ecce98ef2634'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE documentstatus ADD VALUE 'PROCESSING';"
    )


def downgrade() -> None:
    pass