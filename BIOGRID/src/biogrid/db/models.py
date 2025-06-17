'''
In this file, we are going to use sqlalchemy libraries and its modules to map the datasets in the tests to python objects.
This describes sqlalchemy as an ORM (Object Relational Mapper)
'''

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

from typing import List, Optional
from sqlalchemy.orm import Mapped
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

class Protein(Base):
    """
    ORM model for the 'protein' table. As 1 protein (i.e 1 uniprot_id) is unique to one organism, The relationship is added in the org variable

    Attributes:
        uniprot_id (str): The unique identifier for the protein.
        symbol (str): The symbol of the protein.
        tax_id (int): The taxonomic identifier for the organism.
        org (Organism): The relationship to the Organism model.
    """
    __tablename__ = "protein"
    uniprot_id: Mapped[str] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(__name_pos=String(length=100))
    tax_id: Mapped[int] = mapped_column(__name_pos=ForeignKey("organism.tax_id"))
    org: Mapped["Organism"] = relationship(argument="Organism", back_populates="proteins")

    def __repr__(self) -> str:
        return f"Protein(uniprot_id={self.uniprot_id}, symbol={self.symbol}, tax_id={self.tax_id})"

class Organism(Base):
    """
    ORM model for the 'organism' table. As 1 organism can have many proteins (i.e many uniprot_id) The relationship is added in the proteins variable

    Attributes:
        tax_id (int): The taxonomic identifier for the organism.
        name (str): The name of the organism.
        proteins (List[Protein]): The relationship to the Protein model.
    """
    __tablename__ = "organism"
    tax_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(__name_pos=String(length=100))
    proteins: Mapped[List[Protein]] = relationship(argument="Protein", back_populates="org")
    
    def __repr__(self) -> str:
        return f"Organism(tax_id={self.tax_id}, name={self.name})"

class Interaction(Base):
    """
    ORM model for the 'interaction' table.

    Attributes:
        id (int): The unique identifier for the interaction.
        interactor_a_id (str): The unique identifier for the first interactor protein.
        interactor_b_id (str): The unique identifier for the second interactor protein.
        score (Optional[float]): The score of the interaction.
        experimental_system (str): The experimental system used to detect the interaction.
        experimental_system_type (str): The type of experimental system used.
    """
    __tablename__ = "interaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    interactor_a_id: Mapped[str] = mapped_column(__name_pos=ForeignKey(column="protein.uniprot_id"))
    interactor_b_id: Mapped[str] = mapped_column(__name_pos=ForeignKey(column="protein.uniprot_id"))
    score: Mapped[Optional[float]] = mapped_column()  # Can be a float or None. This is what we call a nullable in the database
    experimental_system: Mapped[str] = mapped_column(__name_pos=String(length=100))
    experimental_system_type: Mapped[str] = mapped_column(__name_pos=String(length=100))

    def __repr__(self) -> str:
        return f"Interaction(id={self.id}, interactor_a_id={self.interactor_a_id}, interactor_b_id={self.interactor_b_id}, score={self.score}, experimental_system={self.experimental_system}, experimental_system_type={self.experimental_system_type})"