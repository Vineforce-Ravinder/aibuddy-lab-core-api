"""Add base model audit fields to courses, modules, and topics tables

Revision ID: add_base_model_fields_001
Revises: courses_modules_topics_001
Create Date: 2026-01-14 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_base_model_fields_001'
down_revision: Union[str, Sequence[str], None] = 'courses_modules_topics_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add base model fields to courses, modules, and topics"""
    
    # Add missing fields to courses table
    op.add_column('courses', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('courses', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('courses', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('courses', sa.Column('created_by', sa.String(length=36), nullable=True))
    op.add_column('courses', sa.Column('updated_by', sa.String(length=36), nullable=True))
    op.add_column('courses', sa.Column('deleted_by', sa.String(length=36), nullable=True))
    
    # Add missing fields to modules table
    op.add_column('modules', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('modules', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('modules', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('modules', sa.Column('created_by', sa.String(length=36), nullable=True))
    op.add_column('modules', sa.Column('updated_by', sa.String(length=36), nullable=True))
    op.add_column('modules', sa.Column('deleted_by', sa.String(length=36), nullable=True))
    
    # Add missing fields to topics table
    op.add_column('topics', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('topics', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('topics', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('topics', sa.Column('created_by', sa.String(length=36), nullable=True))
    op.add_column('topics', sa.Column('updated_by', sa.String(length=36), nullable=True))
    op.add_column('topics', sa.Column('deleted_by', sa.String(length=36), nullable=True))


def downgrade() -> None:
    """Downgrade schema - Remove base model fields from courses, modules, and topics"""
    
    # Remove fields from topics table
    op.drop_column('topics', 'deleted_by')
    op.drop_column('topics', 'updated_by')
    op.drop_column('topics', 'created_by')
    op.drop_column('topics', 'deleted_at')
    op.drop_column('topics', 'is_deleted')
    op.drop_column('topics', 'is_verified')
    
    # Remove fields from modules table
    op.drop_column('modules', 'deleted_by')
    op.drop_column('modules', 'updated_by')
    op.drop_column('modules', 'created_by')
    op.drop_column('modules', 'deleted_at')
    op.drop_column('modules', 'is_deleted')
    op.drop_column('modules', 'is_verified')
    
    # Remove fields from courses table
    op.drop_column('courses', 'deleted_by')
    op.drop_column('courses', 'updated_by')
    op.drop_column('courses', 'created_by')
    op.drop_column('courses', 'deleted_at')
    op.drop_column('courses', 'is_deleted')
    op.drop_column('courses', 'is_verified')
