"""Add username to user model

Revision ID: 5bd306f33b2b
Revises: 
Create Date: 2025-07-19 21:59:34.923123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bd306f33b2b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('competences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nom')
    )
    op.create_index(op.f('ix_competences_id'), 'competences', ['id'], unique=False)
    op.create_table('equipements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('localisation', sa.String(), nullable=False),
    sa.Column('frequence_entretien', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_equipements_id'), 'equipements', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'responsable', 'technicien', 'client', name='userrole'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('plannings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('frequence', sa.String(), nullable=False),
    sa.Column('prochaine_date', sa.DateTime(), nullable=True),
    sa.Column('derniere_date', sa.DateTime(), nullable=True),
    sa.Column('equipement_id', sa.Integer(), nullable=True),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['equipement_id'], ['equipements.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plannings_id'), 'plannings', ['id'], unique=False)
    op.create_table('techniciens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('equipe', sa.String(), nullable=True),
    sa.Column('disponibilite', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_techniciens_id'), 'techniciens', ['id'], unique=False)
    op.create_table('interventions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titre', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('type', sa.Enum('corrective', 'preventive', name='interventiontype'), nullable=False),
    sa.Column('statut', sa.Enum('ouverte', 'affectee', 'en_cours', 'en_attente', 'cloturee', 'archivee', name='statutintervention'), nullable=False),
    sa.Column('priorite', sa.Integer(), nullable=True),
    sa.Column('urgence', sa.Boolean(), nullable=True),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('date_limite', sa.DateTime(), nullable=True),
    sa.Column('date_cloture', sa.DateTime(), nullable=True),
    sa.Column('technicien_id', sa.Integer(), nullable=True),
    sa.Column('equipement_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['equipement_id'], ['equipements.id'], ),
    sa.ForeignKeyConstraint(['technicien_id'], ['techniciens.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interventions_id'), 'interventions', ['id'], unique=False)
    op.create_table('technicien_competence',
    sa.Column('technicien_id', sa.Integer(), nullable=True),
    sa.Column('competence_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['competence_id'], ['competences.id'], ),
    sa.ForeignKeyConstraint(['technicien_id'], ['techniciens.id'], )
    )
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom_fichier', sa.String(), nullable=False),
    sa.Column('chemin', sa.String(), nullable=False),
    sa.Column('date_upload', sa.DateTime(), nullable=True),
    sa.Column('intervention_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['interventions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)
    op.create_table('historiques_interventions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('statut', sa.Enum('ouverte', 'affectee', 'en_cours', 'en_attente', 'cloturee', 'archivee', name='statutintervention'), nullable=False),
    sa.Column('remarque', sa.String(), nullable=True),
    sa.Column('horodatage', sa.DateTime(), nullable=True),
    sa.Column('intervention_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['interventions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_historiques_interventions_id'), 'historiques_interventions', ['id'], unique=False)
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('canal', sa.String(), nullable=False),
    sa.Column('contenu', sa.String(), nullable=True),
    sa.Column('date_envoi', sa.DateTime(), nullable=True),
    sa.Column('intervention_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['interventions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_historiques_interventions_id'), table_name='historiques_interventions')
    op.drop_table('historiques_interventions')
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents')
    op.drop_table('technicien_competence')
    op.drop_index(op.f('ix_interventions_id'), table_name='interventions')
    op.drop_table('interventions')
    op.drop_index(op.f('ix_techniciens_id'), table_name='techniciens')
    op.drop_table('techniciens')
    op.drop_index(op.f('ix_plannings_id'), table_name='plannings')
    op.drop_table('plannings')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_equipements_id'), table_name='equipements')
    op.drop_table('equipements')
    op.drop_index(op.f('ix_competences_id'), table_name='competences')
    op.drop_table('competences')
    # ### end Alembic commands ###
