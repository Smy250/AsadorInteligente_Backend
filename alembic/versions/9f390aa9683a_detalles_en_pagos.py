"""detalles_en_pagos

Revision ID: 9f390aa9683a
Revises: 8efda3b3367e
Create Date: 2026-02-24 22:24:06.368215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f390aa9683a'
down_revision: Union[str, Sequence[str], None] = '8efda3b3367e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Crear la bendita tabla detalle_pago que Postgres está pidiendo a gritos
    op.create_table(
        'detalle_pago',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('id_pago', sa.UUID(), nullable=False),
        sa.Column('id_platillo', sa.UUID(), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now(), nullable=True), # <--- ESTA FALTA
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['id_pago'], ['registro_de_pagos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_platillo'], ['platillos.id'], )
    )

    # 2. Limpiar la tabla registro_de_pagos (quitar lo que ya no sirve)
    # Nota: Si el nombre de la constraint falla, Alembic te avisará, 
    # pero usualmente es este formato en Postgres.
    try:
        op.drop_constraint('registro_de_pagos_id_platillo_fkey', 'registro_de_pagos', type_='foreignkey')
    except:
        pass # Por si la constraint tiene otro nombre o no existe

    op.drop_column('registro_de_pagos', 'cantidad')
    op.drop_column('registro_de_pagos', 'id_platillo')


def downgrade() -> None:
    # Para volver atrás: volver a poner las columnas en pagos y borrar detalles
    op.add_column('registro_de_pagos', sa.Column('id_platillo', sa.UUID(), nullable=True))
    op.add_column('registro_de_pagos', sa.Column('cantidad', sa.Integer(), nullable=True))
    op.create_foreign_key('registro_de_pagos_id_platillo_fkey', 'registro_de_pagos', 'platillos', ['id_platillo'], ['id'])
    
    op.drop_table('detalle_pago')