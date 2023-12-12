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
            self.health = int(self.characteristics['самочувствие']) * 3
            self.endurance = int(self.characteristics['движение']) * 3
            self.mind = int(self.characteristics['мышление']) * 3
            self.will = int(self.characteristics['общение']) * 3

            self.save()

    @staticmethod
    def by_name(username, person_name):
        pass

    def add_to_stat(self, stat, value):
        def valid(value, maximum, minimum=0):
            value = min(value, maximum)
            return max(value, 0)

        stat = stat.lower().strip()
        if stat not in list(self.js['resources'].keys()):
            return False

        match stat:
            case 'здоровье':
                valid_value = valid(self.health + value, int(self.characteristics['самочувствие']) * 3)
                self.health = valid_value

            case 'выносливость':
                valid_value = valid(self.endurance + value, int(self.characteristics['движение']) * 3)
                self.endurance = valid_value

            case "рассудок":
                valid_value = valid(self.mind + value, int(self.characteristics['мышление']) * 3)
                self.mind = valid_value

            case 'воля':
                valid_value = valid(self.will + value, int(self.characteristics['общение']) * 3)
                self.will = valid_value

        self.save()
        return valid_value

    def save(self):
        file_path = "./characters/" + self.file_name + ".json"
        with open(file_path, 'r', encoding=ENCODING) as file:
            js = json.load(file)

            for character in js:
                if character['name'] == self.name:
                    character['resources'] = {'здоровье': self.health,
                                              'выносливость': self.endurance,
                                              'рассудок': self.mind,
                                              'воля': self.will}
                    self.js = character
                    break
            else:
                js.append(self.js)

        with open(file_path, 'w', encoding=ENCODING) as file:
            json.dump(js, file, ensure_ascii=False)

        return self

    def to_sting(self):
        text = f"""
        <b>{self.name}</b>
    
        <i>Здоровье({self.health}/{int(self.characteristics['самочувствие']) * 3}): </i> [{("🔴" * self.health) if self.health != 0 else "❌"}]
        <i>Выносливость({self.endurance}/{int(self.characteristics['движение']) * 3}): </i> [{("🟢" * self.endurance) if self.endurance != 0 else "❌"}]
        <i>Рассудок({self.mind}/{int(self.characteristics['мышление']) * 3}): </i> [{("🔵" * self.mind) if self.mind != 0 else "❌"}]
        <i>Воля({self.will}/{int(self.characteristics['общение']) * 3}): </i> [{("🟠" * self.will) if self.will != 0 else "❌"}]
        
        <pre>
        |   Навык      | Знач. |
        |--------------|:-----:|
        | <a href=>Самочувствие</a> |   {self.characteristics['самочувствие']}   |
        | Движение     |   {self.characteristics['движение']}   |
        | Мышление     |   {self.characteristics['мышление']}   |
        | Общение      |   {self.characteristics['общение']}   |
        </pre>
        """
        return text
