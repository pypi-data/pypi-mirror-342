from d4k_ms_service.node import Node, Neo4jConnection


def test_create():
    class KlassA(Node):
        a: str

    db = Neo4jConnection()
    db.clear()
    instance = KlassA.create({"a": "test"})
    assert instance.a == "test"
    assert db.count() == 1
    db.close()


def test_find():
    class KlassA(Node):
        a: str

    db = Neo4jConnection()
    db.clear()
    db.query("CREATE (a:KlassA) SET a.uuid='1234567890', a.a='test find' RETURN a")
    assert db.count() == 1
    instance = KlassA.find("1234567890")
    assert instance.a == "test find"
    assert db.count() == 1
    db.close()


def test_exists():
    class KlassA(Node):
        a: str

    db = Neo4jConnection()
    db.clear()
    assert KlassA.exists("a", "test find") == None
    db.query("CREATE (a:KlassA) SET a.uuid='1234567890', a.a='test find' RETURN a")
    assert db.count() == 1
    assert KlassA.exists("a", "test find").uuid == "1234567890"
    db.close()


def test_save():
    class KlassA(Node):
        a: str
        b: str
        c: int

    db = Neo4jConnection()
    db.clear()
    db.query(
        "CREATE (a:KlassA) SET a.uuid='1234567890', a.a='test find 2', a.b='String B', a.c=10 RETURN a"
    )
    instance = KlassA.find("1234567890")
    assert instance.a == "test find 2"
    assert instance.b == "String B"
    assert instance.c == 10
    assert db.count() == 1
    instance.a = "Something new"
    instance.save()
    instance = KlassA.find("1234567890")
    assert instance.a == "Something new"
    assert instance.b == "String B"
    assert instance.c == 10
    assert db.count() == 1
    db.close()


def test_raw():
    class KlassA(Node):
        a: str
        b: str
        c: int

    class KlassB(Node):
        x: str

    db = Neo4jConnection()
    db.clear()
    db.query(
        "CREATE (a:KlassA) SET a.uuid='1234567890', a.a='test find 2', a.b='String B', a.c=10 RETURN a"
    )
    instance = KlassB.find("1234567890", True)
    assert instance["a"] == "test find 2"
    assert instance["b"] == "String B"
    assert instance["c"] == 10
    assert db.count() == 1
    instance = KlassA.exists("a", "test find 2", True)
    assert instance["a"] == "test find 2"
    assert instance["b"] == "String B"
    assert instance["c"] == 10
    assert db.count() == 1
    db.close()
