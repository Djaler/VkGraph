from app.model import UsersGraph


def test_connections_generation():
    mutual_ids = {
        1: [2, 3],
        2: [1, 4],
        3: [1],
        4: [2]
    }
    
    graph = UsersGraph(users=[], mutual_ids=mutual_ids)
    
    assert len(graph.connections) == 3
    assert all(connection in graph.connections for connection in
               ({1, 2}, {1, 3}, {2, 4}))


def test_connections_generation_without_all_links():
    mutual_ids = {
        1: [2],
        3: [1],
        4: [2]
    }
    
    graph = UsersGraph(users=[], mutual_ids=mutual_ids)
    
    assert len(graph.connections) == 3
    assert all(connection in graph.connections for connection in
               ({1, 2}, {1, 3}, {2, 4}))
