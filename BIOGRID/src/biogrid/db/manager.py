import pandas as pd
import os
from sqlalchemy import Column, Engine, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker
)
from typing import Literal

from sqlalchemy.orm.session import Session

from biogrid.db.models import Base, Interaction, Organism, Protein

# This is the list copied from the test_software.py file
normalized_column_names: list[str] = [
    "biogrid_interaction_id",
    "official_symbol_interactor_a",
    "official_symbol_interactor_b",
    "experimental_system",
    "experimental_system_type",
    "organism_id_interactor_a",
    "organism_id_interactor_b",
    "score",
    "swiss_prot_accessions_interactor_a",
    "swiss_prot_accessions_interactor_b",
    "organism_name_interactor_a",
    "organism_name_interactor_b",
]

class Importer:
    """
    Class to handle the import of data from a TSV file into the database.
    """

    def __init__(self, file_path: str, engine: Engine) -> None:
        """
        Initialize the Importer class.

        Args:
            file_path (str): The path to the TSV file.
            engine (Engine): The SQLAlchemy engine to use for the database connection.
        """
        self.file_path: str = file_path
        self.engine: Engine = engine  # Assign the engine to an instance attribute
        self.session: Session = sessionmaker(bind=self.engine)()
        self.recreate_db()

    def recreate_db(self) -> Literal[True]:
        """
        Recreate the database by dropping all tables and creating them again.

        Returns:
            Literal[True]: Returns True after recreating the database.
        """
        name_of_db_file = str(self.engine).split('///')[1].split(')')[0]
        if not os.path.exists(name_of_db_file):
            open(name_of_db_file, 'w').close()
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        return True    

    def _normalize_column_names(self, data: list) -> list:
        """
        Normalize column names by converting them to lowercase and replacing certain characters.

        Args:
            data (list): List of column names.

        Returns:
            list: List of normalized column names.
        """
        new_data: list = [col.lower().replace('-', '_').replace(" ", "_").replace('#', '') for col in data]
        return new_data
    
    def load_data(self) -> pd.DataFrame:
        """
        Load the TSV file, normalize the column names, and return a new DataFrame with only the required columns.

        Returns:
            pd.DataFrame: The filtered DataFrame with normalized column names.
        """
        file_path: str = os.path.join(os.getcwd(), self.file_path)
        df: pd.DataFrame = pd.read_csv(filepath_or_buffer=file_path, sep='\t')
        df.columns = self._normalize_column_names(data=df.columns.to_list())  # Normalize the column names
        selected_columns: list = normalized_column_names
        df_filtered: pd.DataFrame = df[selected_columns]

        return df_filtered

    def get_interaction_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process the DataFrame to extract interaction data. It is important to note that there can be instances where the values are None
        or repeated or have irregularities like random spaces which need to be removed else the database will give an error about the primary
        key Uniqueness or None values in other columns 

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The processed DataFrame with interaction data.
        """
        df_interaction: pd.DataFrame = df.rename(columns={
            'biogrid_interaction_id': 'id',
            'swiss_prot_accessions_interactor_a': 'interactor_a_id',
            'swiss_prot_accessions_interactor_b': 'interactor_b_id'
        })

        # Keep only required columns
        df_interaction = df_interaction[['id', 'interactor_a_id', 'interactor_b_id', 'score', 'experimental_system', 'experimental_system_type']]

        # Remove rows where 'interactor_a_id' or 'interactor_b_id' is missing
        df_interaction = df_interaction.dropna(subset=['interactor_a_id', 'interactor_b_id'])

        # Ensure IDs are cleaned and uppercase
        df_interaction["interactor_a_id"] = df_interaction["interactor_a_id"].astype(str).str.strip().str.upper()
        df_interaction["interactor_b_id"] = df_interaction["interactor_b_id"].astype(str).str.strip().str.upper()

        # Remove duplicate interaction IDs
        df_interaction = df_interaction.drop_duplicates(subset=['id']).reset_index(drop=True)

        return df_interaction.replace(to_replace='-', value=None)

    def get_proteins_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process the DataFrame to extract protein data. It is important to note that there can be instances where the values are None
        or repeated or have irregularities like random spaces which need to be removed else the database will give an error about the primary
        key Uniqueness or None values in other columns 

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The processed DataFrame with protein data.
        """
        df.columns = self._normalize_column_names(data=df.columns.to_list())
        # Since we want to cover all the instances of the uniprot_id, symbol, and name, we will create separate dataframes and later concatenate them 
        df_melted_1: pd.DataFrame = pd.melt(frame=df, value_vars=["swiss_prot_accessions_interactor_a", "swiss_prot_accessions_interactor_b"],
                            var_name="uniprot_column", value_name="uniprot_id") # Makes a new dataframe in which 1st column is uniprot_column which mentions whether it is interactor_a or _b and then in the second column by the name uniprot_id mention their respective uniprot_id
        df_melted_2: pd.DataFrame = pd.melt(frame=df, value_vars=["official_symbol_interactor_a", "official_symbol_interactor_b"],
                            var_name="symbol_column", value_name="symbol")
        df_melted_3: pd.DataFrame = pd.melt(frame=df, value_vars=["organism_id_interactor_a", "organism_id_interactor_b"],
                            var_name="organism_column", value_name="tax_id")

        # Concatenate melted DataFrames. Removes the duplicates by itself
        df_proteins: pd.DataFrame = pd.concat(objs=[df_melted_1["uniprot_id"], df_melted_2["symbol"], df_melted_3["tax_id"]], axis=1)

        # Remove rows where 'uniprot_id' is missing (NaN or None)
        df_proteins = df_proteins.dropna(subset=["uniprot_id"])

        # Strip spaces and standardize case for uniformity
        df_proteins["uniprot_id"] = df_proteins["uniprot_id"].astype(dtype=str).str.strip().str.upper()
        df_proteins["symbol"] = df_proteins["symbol"].astype(dtype=str).str.strip()
        df_proteins["tax_id"] = pd.to_numeric(arg=df_proteins["tax_id"], errors="coerce")  # Convert tax_id to numeric

        # Drop duplicate proteins based on 'uniprot_id'
        df_proteins = df_proteins.drop_duplicates(subset=['uniprot_id']).reset_index(drop=True)

        return df_proteins

    def get_organisms_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process the DataFrame to extract organism data. It is important to note that there can be instances where the values are None
        or repeated or have irregularities like random spaces which need to be removed else the database will give an error about the primary
        key Uniqueness or None values in other columns 

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The processed DataFrame with organism data.
        """
        df_melted_1: pd.DataFrame = pd.melt(frame=df, id_vars=[], value_vars=["organism_id_interactor_a", "organism_id_interactor_b"],
                    var_name="org_id_column", value_name="tax_id") # Makes a new dataframe in which 1st column is org_id_column which mentions whether it is interactor_a or _b and then in the second column by the name tax_id mention their respective tax_id
        df_melted_2: pd.DataFrame = pd.melt(frame=df, id_vars=[], value_vars=["organism_name_interactor_a", "organism_name_interactor_b"],
                    var_name="organism_column", value_name="name")
        # Concatenate melted DataFrames. Removes the duplicates by itself
        df_organisms: pd.DataFrame = pd.concat(objs=[df_melted_1["tax_id"], df_melted_2["name"]], axis=1).drop_duplicates().reset_index(drop=True)
        
        return df_organisms

    def import_data(self) -> None:
        """
        Import data from the TSV file into the database.
        """
        df: pd.DataFrame = self.load_data()
        df.replace(to_replace='-', value=None, inplace=True)
        organisms_df: pd.DataFrame = self.get_organisms_df(df=df)
        proteins_df: pd.DataFrame = self.get_proteins_df(df=df)
        interactions_df: pd.DataFrame = self.get_interaction_df(df=df)

        session: Session = self.session

        try:
            with session.no_autoflush:  # Prevent autoflush before inserts
                for _, row in organisms_df.iterrows():
                    organism = Organism(tax_id=row['tax_id'], name=row['name'])
                    session.add(organism)

                for _, row in proteins_df.iterrows():
                    # Extra Safety Check Before Inserting
                    if pd.isna(row['uniprot_id']) or row['uniprot_id'] == '': # isna() Detects missing values for an array-like object.
                        print(f"Skipping protein with missing uniprot_id: {row}")
                        continue

                    existing_protein: Protein | None = session.query(Protein).filter_by(uniprot_id=row['uniprot_id']).first()
                    if existing_protein:
                        print(f"Skipping duplicate protein with uniprot_id {row['uniprot_id']}")
                        continue

                    protein = Protein(uniprot_id=row['uniprot_id'], symbol=row['symbol'], tax_id=row['tax_id'])
                    session.add(protein)

                for _, row in interactions_df.iterrows():
                    if row['interactor_a_id'] is None or row['interactor_b_id'] is None:
                        print(f"Skipping interaction with missing IDs: {row}")
                        continue

                    existing_interaction: Interaction | None = session.query(Interaction).filter_by(id=row['id']).first()
                    if existing_interaction:
                        print(f"Skipping duplicate interaction with id {row['id']}")
                        continue

                    interaction = Interaction(
                        id=row['id'],
                        interactor_a_id=row['interactor_a_id'],
                        interactor_b_id=row['interactor_b_id'],
                        score=row['score'],
                        experimental_system=row['experimental_system'],
                        experimental_system_type=row['experimental_system_type']
                    )
                    session.add(interaction)

            session.commit()  # Only commit if all inserts are valid
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
        finally:
            session.close()


class Query:
    """
    Class to handle queries to the database.
    """

    def __init__(self, engine: Engine) -> None:
        """
        Initialize the Query class.

        Args:
            engine (Engine): The SQLAlchemy engine to use for the database connection.
        """
        self.engine: Engine = engine
        self.session: Session = sessionmaker(bind=self.engine)()
    
    def count_proteins(self) -> int:
        """
        Count the number of proteins in the database.

        Returns:
            int: The number of proteins.
        """
        count = self.session.query(Protein).count()
        print(f"Number of proteins: ")
        return count
    
    def count_organisms(self) -> int:
        """
        Count the number of organisms in the database.

        Returns:
            int: The number of organisms.
        """
        count = self.session.query(Organism).count()
        print(f"Number of organisms: ")
        return count
    
    def count_interactions(self) -> int:
        """
        Count the number of interactions in the database.

        Returns:
            int: The number of interactions.
        """
        count = self.session.query(Interaction).count()
        print(f"Number of interactions: ")
        return count




