"""001_initial_schema

Alembic migration file for initial database schema.

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-12-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(80), nullable=False, unique=True),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(80), nullable=True),
        sa.Column('last_name', sa.String(80), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_admin', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'])
    op.create_index('ix_users_email', 'users', ['email'])

    # Create models table
    op.create_table(
        'models',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('version', sa.String(50), nullable=False),
        sa.Column('model_type', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('accuracy', sa.Float(), nullable=True),
        sa.Column('parameters', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_models_name', 'models', ['name'])
    op.create_index('ix_models_type', 'models', ['model_type'])

    # Create experiments table
    op.create_table(
        'experiments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('model_id', sa.Integer(), nullable=False),
        sa.Column('config', postgresql.JSON(), nullable=True),
        sa.Column('results', postgresql.JSON(), nullable=True),
        sa.Column('status', sa.String(50), default='pending'),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.ForeignKeyConstraint(['model_id'], ['models.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_experiments_status', 'experiments', ['status'])

    # Create datasets table
    op.create_table(
        'datasets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('size_mb', sa.Float(), nullable=True),
        sa.Column('samples_count', sa.Integer(), nullable=True),
        sa.Column('splits', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_datasets_name', 'datasets', ['name'])

    # Create metrics table
    op.create_table(
        'metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('experiment_id', sa.Integer(), nullable=False),
        sa.Column('metric_name', sa.String(100), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), default=sa.func.now()),
        sa.ForeignKeyConstraint(['experiment_id'], ['experiments.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_metrics_experiment', 'metrics', ['experiment_id'])
    op.create_index('ix_metrics_timestamp', 'metrics', ['timestamp'])

def downgrade() -> None:
    op.drop_table('metrics')
    op.drop_table('datasets')
    op.drop_table('experiments')
    op.drop_table('models')
    op.drop_table('users')
