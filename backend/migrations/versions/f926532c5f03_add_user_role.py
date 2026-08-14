"""add user role

Revision ID: f926532c5f03
Revises: 0bcdba253a21
Create Date: 2026-07-30 18:09:23.923582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f926532c5f03'
down_revision: Union[str, Sequence[str], None] = '0bcdba253a21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    user_role = sa.Enum(
        "ADMIN",
        "MANAGER",
        "USER",
        name="userrole",
    )

    user_role.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="USER",
        ),
    )

    op.alter_column(
        "users",
        "role",
        server_default=None,
    )

def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "role")

    user_role = sa.Enum(
        "ADMIN",
        "MANAGER",
        "USER",
        name="userrole",
    )

    user_role.drop(op.get_bind(), checkfirst=True)