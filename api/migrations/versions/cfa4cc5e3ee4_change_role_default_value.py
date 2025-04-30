"""change role default value

Revision ID: cfa4cc5e3ee4
Revises: 7246606b08e3
Create Date: 2025-04-30 20:37:35.258094

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models import UserRoles

# revision identifiers, used by Alembic.
revision: str = "cfa4cc5e3ee4"
down_revision: Union[str, None] = "7246606b08e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "user",
        "role",
        type_=sa.Enum(UserRoles, name="userroles"),
        server_default="USER",  # Теперь в нижнем регистре
    )

def downgrade():
    op.alter_column(
        "user",
        "role",
        server_default="USER",  # например, "admin" или NULL
        existing_type=sa.Enum(UserRoles, name="userroles"),
    )