from neo4j import GraphDatabase

class dbNeo4j:
    def __init__(self) -> None:
        self.URI = "bolt://localhost:7687"
        self.AUTH = ("neo4j", "123456789")
        
    def connect(self):
        try:
            driver_session = GraphDatabase.driver(self.URI, auth=self.AUTH).session()
            print('Open  session.')
            return driver_session
        except:
            print('Error [open session]!')
            return None
    
    def close_conn(self, session : GraphDatabase.driver):
        try:
            session.close()
            print('Close session.')
        except:
            print('Error [close session]!')
                    
    def create_pokemon(self, session, pokemon) -> None:
        if not pokemon:
            
            return -1
        
        node1_props = {
            "name" : pokemon.name.upper(),
            "idPokedex" : pokemon.number,
            "desc" : pokemon.description,
            "img"  : pokemon.img
        }
        
        session.run("CREATE (a:POKEMON {name:$name, number:$idPokedex, desc:$desc, img:$img})", node1_props)
        result = None
        
        for type_name in pokemon.types:
            #session.run("MERGE (node1:TYPE {name: $name})", name=type_name)
            query = (
                "MATCH (n1:POKEMON {number: $pokemon_id}) "
                "MERGE (n2:TYPE {name: $type_name}) "
                "WITH n1, n2 "
                "MERGE (n1)-[:HAS_TYPE]->(n2) "
            )
            result = session.run(
                query,
                pokemon_id = pokemon.number,
                type_name = type_name.upper()
            )

        return result
    
    def delete_all_nodes(session : GraphDatabase.driver):
        session.run("MATCH (n) DETACH DELETE n")
 
    def find_pokemon(self, session, props):
        query = (
            "MATCH (pokemon:POKEMON)-[:HAS_TYPE]->(type:TYPE) WHERE pokemon.name = $name RETURN pokemon, COLLECT(type) AS types "
        )
        
        result = session.run(query, name=props['name'])
        return result.data()


if __name__ == "__main__":
    bd = dbNeo4j()
    session = bd.connect()
    if session:
        b = bd.find_pokemon(session, {'name':'002'}) 
        print('RESULTADOS:', b.data())
        if b:
            for i in b:
                print(i)
        
        bd.close_conn(session)