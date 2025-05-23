"""empty message

Revision ID: 6f0361d4730f
Revises: 3123de8a938b
Create Date: 2025-05-01 17:41:00.824972

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6f0361d4730f"
down_revision: Union[str, None] = "3123de8a938b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "car_image",
        "image_url",
        existing_type=sa.VARCHAR(length=32),
        type_=sa.String(length=128),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "car_image",
        "image_url",
        existing_type=sa.String(length=128),
        type_=sa.VARCHAR(length=32),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
