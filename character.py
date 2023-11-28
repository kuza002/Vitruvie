import json

class Character:
    def __init__(self, file_name, json):
        self.file_name = file_name
        self.name = json['name']
        self.characteristics = json['characteristics']
        self.skills = json['skills']

        self.resources = {}
        if json.get('resources') is not None:
            self.resources = json.resources
        else:
            self.health = self.characteristics['self-esteem'] * 3
            self.endurance = self.characteristics['movement'] * 3
            self.mind = self.characteristics['thinking'] * 3
            self.will = self.characteristics['communication'] * 3

    def save(self):
        file_path = "./characters/"+self.file_name+".json"
        with open(file_path, 'r', encoding='windows-1251') as file:
            js = json.load(file)

            for character in js:
                if character['name'] == self.name:
                    character['resources'] = {'health': self.health,
                                              'endurance': self.endurance,
                                              'mind': self.mind,
                                              'will': self.will}

        with open(file_path, 'w', encoding='windows-1251') as file:
            json.dump(js, file)

    def to_sting(self):
        text = f"""
        <b>{self.name}</b>
    
        <i>Здоровье: </i> [{("🔴" * self.health) if self.health != 0 else "❌"}]
        <i>Выносливость: </i> [{("🟢" * self.endurance) if self.endurance != 0 else "❌"}]
        <i>Разум: </i> [{("🔵" * self.mind) if self.mind != 0 else "❌"}]
        <i>Воля: </i> [{("🟠" * self.will) if self.will != 0 else "❌"}]
        
        <pre>
        |   Навык      | Знач. |
        |--------------|:-----:|
        | <a href=>Самочувствие</a> |   {self.characteristics['self-esteem']}   |
        | Движение     |   {self.characteristics['movement']}   |
        | Мышление     |   {self.characteristics['thinking']}   |
        | Общение      |   {self.characteristics['communication']}   |
        </pre>
        """
        return text

    def get_damage(self, damage):
        self.health -= damage
        self.save()
