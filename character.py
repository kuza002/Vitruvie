import json

ENCODING = 'utf-8'

class Character:
    def __init__(self, file_name, js):
        self.file_name = file_name
        self.name = js['name']
        self.characteristics = js['characteristics']
        self.skills = js['skills']
        self.js = js

        if js.get('resources') is not None:
            self.health = js['resources']['здоровье']
            self.endurance = js['resources']['выносливость']
            self.mind = js['resources']['рассудок']
            self.will = js['resources']['воля']
        else:
            self.health = self.characteristics['self-esteem'] * 3
            self.endurance = self.characteristics['movement'] * 3
            self.mind = self.characteristics['thinking'] * 3
            self.will = self.characteristics['communication'] * 3

            self.save()

    def save(self):
        file_path = "./characters/"+self.file_name+".json"
        with open(file_path, 'r', encoding=ENCODING) as file:
            js = json.load(file)

            for character in js:
                if character['name'] == self.name:
                    character['resources'] = {'здоровье': self.health,
                                              'выносливость': self.endurance,
                                              'рассудок': self.mind,
                                              'воля': self.will}

        with open(file_path, 'w', encoding=ENCODING) as file:
            json.dump(js, file, ensure_ascii=False)

        return self

    def to_sting(self):
        text = f"""
        <b>{self.name}</b>
    
        <i>Здоровье: </i> [{("🔴" * self.health) if self.health != 0 else "❌"}]
        <i>Выносливость: </i> [{("🟢" * self.endurance) if self.endurance != 0 else "❌"}]
        <i>Рассудок: </i> [{("🔵" * self.mind) if self.mind != 0 else "❌"}]
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
