from neo4j import GraphDatabase
from d4k_ms_base.service_environment import ServiceEnvironment


class Neo4jConnection:
    def __init__(self):
        sv = ServiceEnvironment()
        self._db_name = sv.get("NEO4J_DB_NAME")
        self._url = sv.get("NEO4J_URI")
        self._usr = sv.get("NEO4J_USERNAME")
        self._pwd = sv.get("NEO4J_PASSWORD")
        try:
            self._driver = GraphDatabase.driver(self._url, auth=(self._usr, self._pwd))
            self._error = None
        except Exception as e:
            self._driver = None
            self._error = e

    def session(self):
        return self._driver.session(database=self._db_name)

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def query(self, query, db=None):
        self._error = None
        assert self._driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self._driver.session(database=self._db_name)
            response = list(session.run(query))
        except Exception as e:
            self._error = e
        finally:
            if session is not None:
                session.close()
        return response

    def error(self):
        return self._error

    def clear(self):
        query = """
      CALL apoc.periodic.iterate('MATCH (n) RETURN n', 'DETACH DELETE n', {batchSize:1000})
    """
        self.query(query)

    def count(self):
        with self._driver.session(database=self._db_name) as session:
            result = session.run("MATCH (n) RETURN COUNT(n) as count")
            record = result.single()
            session.close()
            return record["count"]
