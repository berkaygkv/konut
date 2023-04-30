from sqlalchemy import create_engine, MetaData, Table, Float, Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
import yaml
from .constants import PathConstants, UtilityConstants
from sqlalchemy.orm import registry
from sqlalchemy.sql import text


class Link:
    pass

class IlanDetails:
    pass

class DBRegistry:
    def __init__(self) -> None:
        mapper_registry = registry()
        self.metadata = MetaData()
        column_objects = self._read_column_mapping_file()

        links_table = Table("urls", self.metadata,  Column("ad_id", Integer, primary_key=True), Column("url", String), Column("checked", Boolean), Column("initial_datetime", DateTime), Column("last_update_datetime", DateTime))
        ad_details_table = Table("ad_details", self.metadata, *column_objects)
        self.links_table = links_table
        self.ad_details_table = ad_details_table
        mapper_registry.map_imperatively(Link, links_table)
        mapper_registry.map_imperatively(IlanDetails, ad_details_table)

    def _read_column_mapping_file(cls):
        type_map = {"String": String, "Float": Float, "Boolean": Boolean, "Integer": Integer}
        with open(PathConstants.configs_path.joinpath("column_mapping.yaml"), "r") as rd:
            column_mapping = yaml.safe_load(rd)
            primary_columns = [Column(k, type_map[v]) for k, v in column_mapping["primary_columns"].items()]
            # secondary_columns = [Column(k, Boolean) for k in column_mapping["secondary_columns"]]
            secondary_columns = UtilityConstants.secondary_columns
            column_objects = [Column("ad_id", Integer, primary_key=True)] + primary_columns + secondary_columns + [Column("initial_datetime", DateTime), Column("last_update_datetime", DateTime)]
            return column_objects


class DBManager(DBRegistry):
    def __init__(self, db_path) -> None:
        super().__init__()
        engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert_ilan_data(self, data):
        data = IlanDetails(**data)
        self.session.add(data)
        self.session.commit()
    
    def insert_bulk_links(self, bulk_data):
        data = [Link(**k) for k in bulk_data]
        # self.session.add_all(data)
        for dt in data:
            self.session.merge(dt)
        self.session.commit()

    def filter_unchecked(self):
        return self.session.execute(text("SELECT * FROM urls WHERE checked = False")).first()
    
    def fetch_links(self):
        return self.session.execute(text("SELECT * FROM urls WHERE checked = False")).all()
    
    def update_checked_link(self, ad_id, column, value):
        self.session.query(Link).filter(Link.ad_id == ad_id).update({column: value})
        self.session.commit()