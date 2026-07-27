"""Initial Schema for AIStoryVerse

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-07-26 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Stories Table
    op.create_table(
        'stories',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('cover_image', sa.String(length=512), nullable=True),
        sa.Column('genre', sa.String(length=100), nullable=False, server_default='Fantasy'),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('blueprint', sa.JSON(), nullable=True),
        sa.Column('version_number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('blueprint_version', sa.String(length=50), nullable=False, server_default='v1.0'),
        sa.Column('generation_settings', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='Draft'),
        sa.Column('story_memory', sa.JSON(), nullable=True),
        sa.Column('views', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('times_read', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('chapters_generated', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_words', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_generated_at', sa.DateTime(), nullable=True),
        sa.Column('is_classic', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('is_reimagined', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('original_classic_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stories_status'), 'stories', ['status'], unique=False)
    op.create_index(op.f('ix_stories_user_id'), 'stories', ['user_id'], unique=False)

    # Classic Books Table
    op.create_table(
        'classic_books',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=False),
        sa.Column('cover_image', sa.String(length=512), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('genres', sa.JSON(), nullable=True),
        sa.Column('publication_year', sa.Integer(), nullable=True),
        sa.Column('chapters_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Story Versions Table
    op.create_table(
        'story_versions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('story_id', sa.String(length=36), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('blueprint', sa.JSON(), nullable=True),
        sa.Column('chapter_1_content', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Chapters Table
    op.create_table(
        'chapters',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('story_id', sa.String(length=36), nullable=False),
        sa.Column('chapter_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_reading_time_min', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Classic Chapters Table
    op.create_table(
        'classic_chapters',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('classic_book_id', sa.Integer(), nullable=False),
        sa.Column('chapter_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['classic_book_id'], ['classic_books.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # User Reading Progress Table
    op.create_table(
        'user_reading_progress',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('story_id', sa.String(length=36), nullable=True),
        sa.Column('classic_book_id', sa.Integer(), nullable=True),
        sa.Column('last_read_chapter', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('scroll_position', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_favorite', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('is_saved', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['classic_book_id'], ['classic_books.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_reading_progress_user_id'), 'user_reading_progress', ['user_id'], unique=False)

    # Bookmarks Table
    op.create_table(
        'bookmarks',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('story_id', sa.String(length=36), nullable=True),
        sa.Column('classic_book_id', sa.Integer(), nullable=True),
        sa.Column('chapter_number', sa.Integer(), nullable=False),
        sa.Column('position_percent', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['classic_book_id'], ['classic_books.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookmarks_user_id'), 'bookmarks', ['user_id'], unique=False)

    # Story Sessions Table
    op.create_table(
        'story_sessions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('story_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('ended_at', sa.DateTime(), nullable=True),
        sa.Column('last_read_chapter', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('reading_time_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('device_info', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_story_sessions_user_id'), 'story_sessions', ['user_id'], unique=False)

    # Generation Logs Table
    op.create_table(
        'generation_logs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('story_id', sa.String(length=36), nullable=False),
        sa.Column('chapter_number', sa.Integer(), nullable=True),
        sa.Column('prompt_type', sa.String(length=50), nullable=False),
        sa.Column('prompt_text', sa.Text(), nullable=False),
        sa.Column('response_text', sa.Text(), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('generation_logs')
    op.drop_index(op.f('ix_story_sessions_user_id'), table_name='story_sessions')
    op.drop_table('story_sessions')
    op.drop_index(op.f('ix_bookmarks_user_id'), table_name='bookmarks')
    op.drop_table('bookmarks')
    op.drop_index(op.f('ix_user_reading_progress_user_id'), table_name='user_reading_progress')
    op.drop_table('user_reading_progress')
    op.drop_table('classic_chapters')
    op.drop_table('chapters')
    op.drop_table('story_versions')
    op.drop_table('classic_books')
    op.drop_index(op.f('ix_stories_user_id'), table_name='stories')
    op.drop_index(op.f('ix_stories_status'), table_name='stories')
    op.drop_table('stories')
