import requests
from bs4 import BeautifulSoup

class Pokemon:
    def __init__(self, name:str='', number:int=-1, desc:str='', img:str='', types:list=[]):
        self.name = name
        self.types = types
        self.number = number
        self.description = desc
        self.img = img
        
    def scrap_pokemon_info(self, pokemon_name : str) -> object:
        url = f'https://pokemondb.net/pokedex/{pokemon_name}'
        response = requests.get(url)
        
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, 'html.parser')
            
            # Name
            self.name = bs.find('h1').text
            
            # <table> with basic infos
            table_vitals = bs.find('table', {'class':'vitals-table'})
            
            # Number in Pokedex
            self.number = table_vitals.find('strong').text
            
            # Types
            try:
                self.types = [type.text for type in table_vitals.find_all('a', {'class':'type-icon'})]
            except:
                self.types = None
                
            # Description
            try:
                self.description = bs.find('main').p.text
            except:
                self.description = None
               
            # Image
            self.img = bs.find('main').find('img')['src'] 
            return self
        else:
            print('Pokémon não encontrado.')
            return None

    def __str__(self) -> str:
        res  = f'Pokémon: {self.name}\n'
        res += f'Número da Pokédex: {self.number}\n'
        res += f'Tipo(s): {", ".join(self.types)}\n'
        res += f'Descrição: {self.description}\n'
        res += f'Link da imagem: {self.img}\n'
    
        return res
        
if __name__ == '__main__':
    pokemon_name = input('Write a Pokemon name: ')
    a = Pokemon.scrap_pokemon_info(Pokemon, pokemon_name=pokemon_name)
    print(a.img)