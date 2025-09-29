import random


class Creature:

    def __init__(self, name, attaсk, protection, health, full_health, damage):

        self.name = name
        self.attack = attaсk
        self.protection = protection
        self.health = health
        self.full_health = health
        self.damage = damage

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        if not (1 <= value <= 30):
            raise ValueError("Атака должна быть от 1 до 30")
        self._attack = value

    @property
    def protection(self):
        return self._protection

    @protection.setter
    def protection(self, value):
        if not (1 <= value <= 30):
            raise ValueError("Защита должна быть от 1 до 30")
        self._protection = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < 0:
            raise ValueError("Здоровье должно быть положительным")
        self._health = value

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        if not (isinstance(value, list) and len(value) == 2):
            raise ValueError("Диапазон урона должен быть списком из двух чисел")
        if value[0] <= 0 or value[1] < value[0]:
            raise ValueError("Некорректные границы урона")
        self._damage = value

    def is_alive(self):
        return self.health > 0

    def take_hit(self, value):
        self.health = max(0, self.health - value)

    def character_hit(self, attacted: 'Creature'):
        if not self.is_alive():
            return f'{self.name} не может атаковать'
        if not attacted.is_alive():
            return f'{attacted.name} уже умер'
        modificator = self.attack - attacted.protection + 1
        if modificator <= 0:
            modificator = 1

        cubes = [random.randint(1,6) for _ in range(modificator)]
        success = any(cube > 5 for cube in cubes)

        if not success:
            return f'{self.name} промахнулся... {attacted.name} увернулся!'

        hit = random.randint(self.damage[0], self.damage[1])
        attacted.take_hit(hit)

        return (f'{self.name} попал по {attacted.name}у! '
                f'Урон = {hit}. У {attacted.name} осталось {attacted.health} здоровья.')

    def __str__(self):
        return (f'{self.name}\nЗдоровье: {self.health}/{self.full_health}, Атака: {self.attack}, Защита: {self.protection}, Урон: от {self.damage[0]} до {self.damage[1]}')


class Player(Creature):

    def __init__(self, name, attaсk, protection, health, full_health, damage):
        super().__init__(name, attaсk, protection, health, full_health, damage)

        self.heal_count = 0
        self.max_heals = 4

    def heal(self):
        if not self.is_alive():
            return f'{self.name} уже погиб...'
        if self.heal_count >= self.max_heals:
            return f'лекарств больше нет...'

        self.health = min(self.full_health, self.health + self.full_health * 0.3)
        self.heal_count += 1

        return f'{self.name} вылечился'

    def __str__(self):
        return f'ИГРОК: {super().__str__()}'


class Monster(Creature):

    def __init__(self, name, attaсk, protection, health, full_health, damage):
        super().__init__(name, attaсk, protection, health, full_health, damage)

    def __str__(self):
        return f'МОНСТР: {super().__str__()}'


#ИГРА
player = Player("Герой", 15, 12, 50, 50, [5, 12])
monster1 = Monster("Гоблин", 10, 8, 30, 30, [3, 7])
monster2 = Monster("Орк", 18, 15, 40, 40, [6, 10])

monsters = [monster1, monster2]

print("===== НАЧАЛО ИГРЫ =====")
print(player)
for monster in monsters:
    print(monster)

print("\n===== БИТВА НАЧИНАЕТСЯ! =====\n")

round_num = 1
while player.is_alive() and any(monster.is_alive() for monster in monsters):
    print(f"\n----- Раунд {round_num} -----")

    '''Ход игрока: атакует первого монстра'''
    attacted = next(monster for monster in monsters if monster.is_alive())
    print(player.character_hit(attacted))

    '''Иногда игрок лечится'''
    if random.random() < 0.2:
        print(player.heal())

    '''Ход монстров'''
    for monster in monsters:
        if monster.is_alive():
            print(monster.character_hit(player))

    print(player)
    for monster in monsters:
        print(monster)

    round_num += 1

print("\n===== ИГРА ОКОНЧЕНА =====")
if player.is_alive():
    print("Игрок победил монстров!")
else:
    print("Монстры победили игрока...")
