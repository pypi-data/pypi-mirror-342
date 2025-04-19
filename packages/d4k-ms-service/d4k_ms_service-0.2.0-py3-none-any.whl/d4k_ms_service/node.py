from uuid import uuid4
from pydantic import BaseModel
from d4k_ms_service.neo4j_connection import Neo4jConnection


class Node(BaseModel):
    uuid: str

    @classmethod
    def create(cls, params):
        db = Neo4jConnection()
        with db.session() as session:
            result = session.execute_write(cls._create, cls, params)
        db.close()
        return result

    @classmethod
    def find(cls, uuid, raw=False):
        db = Neo4jConnection()
        with db.session() as session:
            result = session.execute_read(cls._find, cls, uuid, raw)
        db.close()
        return result

    @classmethod
    def exists(cls, key, value, raw=False):
        db = Neo4jConnection()
        with db.session() as session:
            result = session.execute_read(cls._exists, cls, key, value, raw)
        db.close()
        return result

    def save(self):
        db = Neo4jConnection()
        with db.session() as session:
            result = session.execute_write(self._save, self)
        db.close()
        return result

    @classmethod
    def wrap(cls, node):
        return cls(**cls.as_dict(node))

    @classmethod
    def as_dict(cls, node):
        dict = {}
        for items in node.items():
            dict[items[0]] = items[1]
        return dict

    @staticmethod
    def _create(tx, cls, source_params):
        params = []
        for param in source_params.keys():
            params.append(f"a.{param}='{source_params[param]}'")
        params_str = ", ".join(params)
        query = """
      CREATE (a:%s {uuid: $uuid1})
      SET %s 
      RETURN a
    """ % (cls.__name__, params_str)
        result = tx.run(query, uuid1=str(uuid4()))
        for row in result:
            return cls.wrap(row["a"])
        return None

    @staticmethod
    def _find(tx, cls, uuid, raw):
        node_clause = "a" if raw else f"a:{cls.__name__}"
        query = "MATCH (%s { uuid: $uuid1 }) RETURN a" % (node_clause)
        result = tx.run(query, uuid1=uuid)
        for row in result:
            return cls.as_dict(row["a"]) if raw else cls.wrap(row["a"])
        return None

    @staticmethod
    def _exists(tx, cls, key, value, raw):
        node_clause = "a" if raw else f"a:{cls.__name__}"
        where_clause = f'{key}: "{value}"'
        query = "MATCH (%s {%s}) RETURN a" % (node_clause, where_clause)
        result = tx.run(query)
        for row in result:
            return cls.as_dict(row["a"]) if raw else cls.wrap(row["a"])
        return None

    @staticmethod
    def _save(tx, self):
        params = []
        for param in self.model_fields.keys():
            params.append(f"a.{param}='{getattr(self, param)}'")
        params_str = ", ".join(params)
        query = """
      MATCH (a:%s {uuid: '%s'})
      SET %s 
      RETURN a
    """ % (self.__class__.__name__, self.uuid, params_str)
        result = tx.run(query)
        for row in result:
            return self.__class__.wrap(row["a"])
        return None
