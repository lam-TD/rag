"""create jobs table

Revision ID: 5f26ecace3d6
Revises: e3e83b901590
Create Date: 2025-09-28 11:27:57.022078

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5f26ecace3d6"
down_revision: Union[str, Sequence[str], None] = "e3e83b901590"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "type",
            sa.String(length=50),
            nullable=False,
            default="default",
            comment="e.g., 'transcription', 'translation'",
        ),
        sa.Column("file_id", sa.Integer, sa.ForeignKey("files.id"), nullable=False),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            comment="queued|running|done|failed",
        ),
        sa.Column(
            "created_at", sa.DateTime, server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("error", sa.Text, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("jobs")
