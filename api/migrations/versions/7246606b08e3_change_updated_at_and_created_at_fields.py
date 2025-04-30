"""change updated_at and created_at fields

Revision ID: 7246606b08e3
Revises: ad6e1cf432e6
Create Date: 2025-04-30 20:31:15.437843

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = "7246606b08e3"
down_revision: Union[str, None] = "ad6e1cf432e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "user",
        "created_at",
        server_default=func.now(),
        existing_type=sa.DateTime(timezone=True),
    )
    op.alter_column(
        "user",
        "updated_at",
        server_default=func.now(),
        onupdate=func.now(),
        existing_type=sa.DateTime(timezone=True),
    )

def downgrade():
    op.alter_column(
        "user",
        "created_at",
        server_default="null",
        existing_type=sa.DateTime(timezone=True),
    )
    op.alter_column(
        "user",
        "updated_at",
        server_default="null",
        onupdate=None,
        existing_type=sa.DateTime(timezone=True),
    )
