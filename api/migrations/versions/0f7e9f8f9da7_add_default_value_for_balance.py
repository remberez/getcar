"""add default value for balance

Revision ID: 0f7e9f8f9da7
Revises: cfa4cc5e3ee4
Create Date: 2025-04-30 20:47:04.171183

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f7e9f8f9da7"
down_revision: Union[str, None] = "cfa4cc5e3ee4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "user",
        "balance",
        server_default="0.00",  # Теперь в нижнем регистре
    )

def downgrade():
    op.alter_column(
        "user",
        "balance",
        server_default="0.00",  # например, "admin" или NULL
    )