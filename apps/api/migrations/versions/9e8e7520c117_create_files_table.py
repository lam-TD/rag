"""create files table

Revision ID: 9e8e7520c117
Revises:
Create Date: 2025-09-27 21:30:35.759992

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e8e7520c117"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "files",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("size", sa.Integer, nullable=False),
        sa.Column("note", sa.Unicode(255), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("files")
