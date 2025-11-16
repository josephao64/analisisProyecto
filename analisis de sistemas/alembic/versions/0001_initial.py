"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2025-10-24 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    movement_type = sa.Enum('IN', 'OUT', 'ADJUST', name='movement_type')
    movement_type.create(op.get_bind(), checkfirst=True)

    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sku', sa.String(length=32), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('min_stock', sa.Numeric(12,3), nullable=False, server_default='0'),
        sa.Column('price', sa.Numeric(12,2), nullable=False, server_default='0'),
        sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sku')
    )
    op.create_index('ix_products_sku_unique', 'products', ['sku'], unique=True)
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)

    op.create_table('locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('ix_locations_code_unique', 'locations', ['code'], unique=True)
    op.create_index(op.f('ix_locations_id'), 'locations', ['id'], unique=False)

    op.create_table('stocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Numeric(12,3), nullable=False, server_default='0'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_id', 'location_id', name='uq_stock_product_location')
    )
    op.create_index(op.f('ix_stocks_id'), 'stocks', ['id'], unique=False)

    op.create_table('movements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('type', movement_type, nullable=False),
        sa.Column('quantity', sa.Numeric(12,3), nullable=False),
        sa.Column('reason', sa.String(length=120), nullable=False),
        sa.Column('reference', sa.String(length=120), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movements_id'), 'movements', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_movements_id'), table_name='movements')
    op.drop_table('movements')
    op.drop_index(op.f('ix_stocks_id'), table_name='stocks')
    op.drop_table('stocks')
    op.drop_index(op.f('ix_locations_id'), table_name='locations')
    op.drop_index('ix_locations_code_unique', table_name='locations')
    op.drop_table('locations')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_index('ix_products_sku_unique', table_name='products')
    op.drop_table('products')
    movement_type = sa.Enum('IN', 'OUT', 'ADJUST', name='movement_type')
    movement_type.drop(op.get_bind(), checkfirst=True)
