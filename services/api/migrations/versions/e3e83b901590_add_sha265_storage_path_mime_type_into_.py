"""add sha265, storage_path, mime_type into files table

Revision ID: e3e83b901590
Revises: 9e8e7520c117
Create Date: 2025-09-27 22:38:15.070206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3e83b901590'
down_revision: Union[str, Sequence[str], None] = '9e8e7520c117'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('files', sa.Column('sha256', sa.String(length=64), nullable=True))
    op.add_column('files', sa.Column('storage_path', sa.String(length=255), nullable=True))
    op.add_column('files', sa.Column('mime_type', sa.String(length=100), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('files', 'mime_type')
    op.drop_column('files', 'storage_path')
    op.drop_column('files', 'sha256')
