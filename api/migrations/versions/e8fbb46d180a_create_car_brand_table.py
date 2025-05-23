"""create car brand table

Revision ID: e8fbb46d180a
Revises: 33937501de0e
Create Date: 2025-04-24 16:35:35.190060

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e8fbb46d180a"
down_revision: Union[str, None] = "33937501de0e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "car_brand",
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("car_brand")
    # ### end Alembic commands ###
