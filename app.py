from flask import Flask, render_template
from scrap import Pokemon
from db import dbNeo4j

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('./home.html')

@app.route("/pokedex/<pokemon_name>", methods=['GET'])
def hello_world(pokemon_name : str):
    db = dbNeo4j()
    session = db.connect()
    
    print('NOME BUSCADO ROUTE: ',pokemon_name)
    result = db.find_pokemon(session, {'name':pokemon_name.upper()})
    pokemon = {}
    
    try:
        if len(result) > 0:
            infos = result[0]['pokemon']
            types = [matchs['name'] for matchs in result[0]['types']]
                
            pokemon = Pokemon(
                infos['name'].capitalize(),
                infos['number'],
                infos['desc'],
                infos['img'],
                types
            )
            
            print('Found Pokemon:', pokemon)
        else:    
            pokemon = Pokemon()
            pokemon.scrap_pokemon_info(pokemon_name)
            
            if pokemon.name:
                db.create_pokemon(session, pokemon)     
                print('Created Pokemon:', pokemon)
            else:
                print('Pokemon not found!')
    
    except Exception as e:
        print('error: ', e)
         
    db.close_conn(session)
    
    return render_template('./template.html', pokemon=pokemon)


if __name__ == '__main__':
    try:      
        app.run(port=8080, debug=True)            
    except Exception as e:
        print(e)