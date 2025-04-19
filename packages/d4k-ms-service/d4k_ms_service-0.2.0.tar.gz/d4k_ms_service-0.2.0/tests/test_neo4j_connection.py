from d4k_ms_service.neo4j_connection import Neo4jConnection


def test_instance():
    db = Neo4jConnection()
    assert db is not None
    assert db.error() is None
    db.close()


def test_session():
    db = Neo4jConnection()
    session = db.session()
    session.close()
    db.close()


def test_clear():
    db = Neo4jConnection()
    db.clear()
    assert db.count() == 0
    db.close()


def test_query():
    db = Neo4jConnection()
    db.clear()
    db.query("CREATE (n:TEST1) SET n.param = 'test' RETURN n")
    assert db.count() == 1
    results = db.query("MATCH (n:TEST1) RETURN n")
    assert len(results) == 1
    assert results[0][0]._properties == {"param": "test"}
    db.clear()
    assert db.count() == 0
    db.close()
