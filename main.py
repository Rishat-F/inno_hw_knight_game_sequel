import random
import os
from copy import deepcopy


monster_counter = 0
MONSTERS_TO_WIN = 10

PROLOGUE = "\n\tДобро пожаловать в сказочную игру \"Герой и Монстры\"!\n\n" \
           "\tКоролевству угрожает нападение со стороны 10 монстров!\n" \
           "\tЛишь отважные и сильные способны спасти Королевство...\n"
EPILOGUE = "\n\tМного смельчаков пало в битве с монстрами...\n" \
           "\tНо никто не смог остановить их.\n" \
           "\tВ итоге Королевство было разрушено чудовищами...\n\n" \
           "\tВы проиграли!\n\n" \
           "Игра окончена."

MELEE_TYPE = "воин"
RANGE_TYPE = "лучник"
MAGE_TYPE = "маг"
TYPES = {"1": MELEE_TYPE, "2": RANGE_TYPE, "3": MAGE_TYPE}

EVATION_CHANCE = 50

HERO_START_HP = 20
DEFAULT_SWORD_ATTACK = 8

MONSTER_MIN_HP = 5
MONSTER_MAX_HP = 12

MONSTER_MIN_ATTACK = 5
MONSTER_MAX_ATTACK = 12

MIN_ATTACK = 6
MAX_ATTACK = 12
ATTACK_MULTIPLIER = 2

APPLE_MIN_HP = 6
APPLE_MAX_HP = 10

QUIVER_MIN_ARROWS = 1
QUIVER_MAX_ARROWS = 3


def greeting():
    print(PROLOGUE)
    choice = input("Готовы бросить вызов опасности? [y/n]\n").lower()
    while choice not in ("y", "n", "yes", "no", "\n", ""):
        clear_terminal()
        print(PROLOGUE)
        choice = input('Введите "y" или "n" чтобы начать игру:\n')
    if choice.startswith("y") or choice in ("\n", ""):
        return True
    return False


def clear_terminal() -> None:
    """Clear terminal window."""
    os.system("cls" if os.name == "nt" else "clear")


def print_hero_stats(hero, monster_counter) -> None:
    """Print stats and game steps in pretty view."""
    clear_terminal()
    print(
        f"----------------------------------------------\n"
        f"Герой:\n"
        f"hp: {hero.hp}   Класс: {hero.type}   Оружие: {hero.weapon}   Рюкзак: {hero.backpack}\n"
        f"\nОсталось одолеть {MONSTERS_TO_WIN - monster_counter} монстров\n"
        f"----------------------------------------------"
    )


def print_battle_stats(hero, monster, monster_counter) -> None:
    """Print stats and game steps in pretty view."""
    print_hero_stats(hero, monster_counter)
    if monster.hp > 0:
        print(
            f"Монстр:\n"
            f"hp: {monster.hp}   Класс: {monster.type}   Атака: {monster.attack}\n"
        )


def random_meeting(hero, monster_counter):
    meeting = random.choices([Sword, Bow, Book, Quiver, Apple, Totem, Monster], [1, 1, 1, 1, 3, 1, 5])[0]
    if issubclass(meeting, Weapon):
        if hero.type == meeting.attack_type:
            return meeting(random.randint(MIN_ATTACK, MAX_ATTACK * ATTACK_MULTIPLIER))
        else:
            return meeting(random.randint(MIN_ATTACK, MAX_ATTACK))
    elif meeting is Apple:
        return meeting(random.randint(APPLE_MIN_HP, APPLE_MAX_HP))
    elif meeting is Quiver:
        return meeting(random.randint(QUIVER_MIN_ARROWS, QUIVER_MAX_ARROWS))
    elif meeting is Totem:
        return meeting(deepcopy(hero), deepcopy(monster_counter))
    elif meeting is Monster:
        return meeting(
            random.randint(MONSTER_MIN_HP, MONSTER_MAX_HP),
            random.randint(MONSTER_MIN_ATTACK, MONSTER_MAX_ATTACK)
        )


class Unit:

    def __init__(self, hp):
        self.hp = hp

    def __str__(self):
        return self.__class__.__name__


class AbleToEvade:

    evation_chance = EVATION_CHANCE

    def _can_evade_enemy_hit(self, enemy):
        if isinstance(self, Monster) and isinstance(enemy, Hero) and self.type == enemy.weapon.attack_type:
            return True
        elif isinstance(self, Hero) and isinstance(enemy, Monster) and self.type == enemy.type:
            return True
        else:
            return False

    def evade_hit(self, enemy):
        if self._can_evade_enemy_hit(enemy):
            return random.choices([True, False], [self.evation_chance, 100 - self.evation_chance])[0]
        else:
            return False


class AbleToAttack:

    def __init__(self, attack):
        self.attack = attack

    def attack_enemy(self, enemy):
        if isinstance(enemy, AbleToEvade):
            if enemy.evade_hit(self):
                print(f"\n\t{str(enemy)} увернулся от удара")
                input("\n\tНажмите Enter\n")
            else:
                enemy.hp -= self.attack
        else:
            enemy.hp -= self.attack


class Monster(Unit, AbleToAttack, AbleToEvade):

    def __init__(self, hp, attack):
        super().__init__(hp)
        super(Unit, self).__init__(attack)
        self.type = random.choice(list(TYPES.values()))

    def __repr__(self):
        return f"{self.__class__.__name__} (hp = {self.hp}, attack = {self.attack}, type = {self.type})"


class Hero(Unit, AbleToAttack, AbleToEvade):

    @staticmethod
    def choose_hero():
        choice = input(
            "\nВыберите класс героя:\n"
            "\tВведите 1, чтобы играть Воином.\n"
            "\tВведите 2, чтобы играть Лучником.\n"
            "\tВведите 3, чтобы играть Магом.\n"
            )
        while choice not in ("1", "2", "3"):
            clear_terminal()
            choice = input(
                "\nНекорректный ввод.\n"
                "\nВыберите класс героя:\n"
                "\tВведите 1, чтобы играть Воином.\n"
                "\tВведите 2, чтобы играть Лучником.\n"
                "\tВведите 3, чтобы играть Магом.\n"
                )
        return TYPES[choice]

    def __init__(self, hp, sword):
        super().__init__(hp)
        self.type = self.choose_hero()
        self.backpack = {}
        self.weapon = sword
        super(Unit, self).__init__(sword.attack)

    def __repr__(self):
        return f"{self.__class__.__name__} (hp = {self.hp}, attack = {self.attack}, type = {self.type})"

    def pick_up(self, thing):
        if isinstance(thing, Quiver):
            self.backpack.setdefault("arrows", 0)
            self.backpack["arrows"] += thing.arrows
        elif self.weapon.type == thing.type:
            self.weapon = thing
            self.attack = self.weapon.attack
        else:
            self.backpack[thing.type] = thing

    @property
    def weapons_in_backpack(self):
        return [thing for thing in self.backpack if isinstance(self.backpack[thing], Weapon)]

    def change_weapon(self):
        if bool(self.weapons_in_backpack):
            weapons_to_chose = enumerate(self.weapons_in_backpack, start=1)
            input_text = "\n\tВведите 0, чтобы оставить свое текущее оружие.\n"
            for i, weapon in weapons_to_chose:
                input_text += f"\tЧтобы сменить оружие на {weapon}, введите {i}.\n"
            choice = input(input_text)
            while choice not in [str(i) for i in range(len(self.weapons_in_backpack) + 1)]:
                choice = input("Некорректный ввод\n" + input_text)
            if choice != "0":
                self.backpack[self.weapon.type] = self.weapon
                self.weapon = self.backpack.pop(self.weapons_in_backpack[int(choice) - 1])
                self.attack = self.weapon.attack
        else:
            print("У вас нет других оружий в рюкзаке.")
            input("\n\tНажмите Enter\n")

    def check_arrows(self):
        if self.backpack.get("arrows"):
            return True
        return False

    def attack_enemy(self, enemy):
        if isinstance(self.weapon, Bow):
            if self.check_arrows():
                super().attack_enemy(enemy)
                self.backpack["arrows"] -= 1
                if not self.check_arrows():
                    try:
                        del self.backpack["arrows"]
                    except KeyError as err:
                        print("В рюкзаке нет данного ключа", err)
            else:
                print("У вас нет стрел, вы не нанесли урона врагу! Смените оружие!")
                input("\n\tНажмите Enter\n")
        else:
            super().attack_enemy(enemy)


class Thing:

    def __init__(self):
        self.type = self.__class__.__name__.lower()


class Weapon(Thing):

    def __init__(self, attack):
        super().__init__()
        self.attack = attack

    def __repr__(self):
        return f"{self.type}(attack = {self.attack})"


class Sword(Weapon):

    attack_type = MELEE_TYPE

    def __init__(self, attack):
        super().__init__(attack)


class Bow(Weapon):

    attack_type = RANGE_TYPE

    def __init__(self, attack):
        super().__init__(attack)


class Book(Weapon):

    attack_type = MAGE_TYPE

    def __init__(self, attack):
        super().__init__(attack)


class Quiver(Thing):

    def __init__(self, arrows_quantity):
        super().__init__()
        self.arrows = arrows_quantity


class Apple(Thing):

    def __init__(self, hp):
        super().__init__()
        self.hp = hp


class Totem(Thing):

    def __init__(self, hero, monster_counter):
        super().__init__()
        self.hero = hero
        self.monster_counter = monster_counter

    def __repr__(self):
        return f"cохранение с {self.hero.hp} hp"


def game() -> None:
    default_sword = Sword(DEFAULT_SWORD_ATTACK)
    hero = Hero(HERO_START_HP, default_sword)
    global monster_counter
    while hero.hp > 0 and monster_counter < 10:
        print_hero_stats(hero, monster_counter)
        meeting = random_meeting(hero, monster_counter)  # тут нужна фабрика, которая будет выдавать рандомно объекты вещей, оружия или монстров
        if isinstance(meeting, Apple):
            hero.hp += meeting.hp
            print_hero_stats(hero, monster_counter)
            print(
                f"\nВы нашли яблоко и съели его.\n"
                f"Кол-во единиц здоровья увеличилось на {meeting.hp}."
                )
            input("\n\tНажмите Enter\n")
        elif isinstance(meeting, Weapon):
            print(
                f"\nВы нашли {meeting.type}, который дает {meeting.attack} ед. урона."
                )
            choice = input(
                f"\n\tВведите 0, чтобы пройти мимо.\n"
                f"\tВведите 1, чтобы подобрать новый {meeting.type}.\n"
                )
            while choice not in ("0", "1"):
                print_hero_stats(hero, monster_counter)
                choice = input(
                    f"\nВы нашли {meeting.type}, который дает {meeting.attack} ед. урона."
                    f"\n\tНекорректный ввод.\n"
                    f"\n\tВведите 0, чтобы пройти мимо.\n"
                    f"\tВведите 1, чтобы подобрать новый {meeting.type}.\n"
                    )
            if choice == "1":
                hero.pick_up(meeting)
        elif isinstance(meeting, Quiver):
            print(f"\nВы нашли {meeting.type}, с {meeting.arrows} стрелами.")
            choice = input(
                f"\n\tВведите 0, чтобы пройти мимо.\n"
                f"\tВведите 1, чтобы подобрать новый {meeting.type}.\n"
                )
            while choice not in ("0", "1"):
                print_hero_stats(hero, monster_counter)
                choice = input(
                    f"\nВы нашли {meeting.type}, с {meeting.arrows} стрелами."
                    f"\n\tНекорректный ввод.\n"
                    f"\n\tВведите 0, чтобы пройти мимо.\n"
                    f"\tВведите 1, чтобы подобрать новый {meeting.type}.\n"
                    )
            if choice == "1":
                hero.pick_up(meeting)
        elif isinstance(meeting, Totem):
            print(f"\nВы нашли {meeting.type}")
            choice = input(
                f"\n\tВведите 0, чтобы пройти мимо.\n"
                f"\tВведите 1, чтобы подобрать новый {meeting.type}.\n"
                )
            while choice not in ("0", "1"):
                print_hero_stats(hero, monster_counter)
                choice = input(
                    f"\nВы нашли {meeting.type}"
                    f"\n\tНекорректный ввод.\n"
                    f"\n\tВведите 0, чтобы пройти мимо.\n"
                    f"\tВведите 1, чтобы подобрать новый {meeting.type}.\n"
                    )
            if choice == "1":
                hero.pick_up(meeting)
        elif isinstance(meeting, Monster):
            print_battle_stats(hero, meeting, monster_counter)
            print(
                f"\nБОЙ! На вас напал монстр-{meeting.type} с {meeting.hp} ед. "
                f"здоровья и с атакой в {meeting.attack} ед. урона."
                )
            choice = None
            while hero.hp > 0 and meeting.hp > 0 and choice != "0":
                choice = input(
                    "\n\tВведите 0, чтобы убежать.\n"
                    "\tВведите 1, чтобы атаковать чудовище текущим оружием.\n"
                    "\tВведите 2, чтобы сменить оружие перед атакой.\n"
                    )
                while choice not in ("0", "1", "2"):
                    print_battle_stats(hero, meeting, monster_counter)
                    choice = input(
                        f"\nБОЙ! На вас напал монстр-{meeting.type} с {meeting.hp} ед. "
                        f"здоровья и с атакой в {meeting.attack} ед. урона."
                        f"\n\tНекорректный ввод.\n\tВведите 0, чтобы убежать.\n"
                        f"\tВведите 1, чтобы атаковать чудовище текущим оружием.\n"
                        f"\tВведите 2, чтобы сменить оружие перед атакой.\n"
                        )
                if choice == "2":
                    print_battle_stats(hero, meeting, monster_counter)
                    hero.change_weapon()
                    print_battle_stats(hero, meeting, monster_counter)
                    continue
                elif choice == "1":
                    print_battle_stats(hero, meeting, monster_counter)
                    meeting.attack_enemy(hero)
                    print_battle_stats(hero, meeting, monster_counter)
                    hero.attack_enemy(meeting)
                    print_battle_stats(hero, meeting, monster_counter)
            if hero.hp > 0 and meeting.hp <= 0:
                monster_counter += 1
                if monster_counter != 10:
                    print_hero_stats(hero, monster_counter)
                    print("\nВы одолели чудовище!")
                    input("\n\tНажмите Enter\n")
            if hero.hp <= 0 and "totem" in hero.backpack:
                choice = input("\n\tМонстр вас убил. Использовать тотем? [y/n]\n").lower()
                while choice not in ("y", "n", "yes", "no", "\n", ""):
                    clear_terminal()
                    choice = input("\n\tМонстр вас убил. Использовать тотем? [y/n]\n").lower()
                if choice.startswith("y") or choice in ("\n", ""):
                    monster_counter = hero.backpack["totem"].monster_counter
                    hero = hero.backpack["totem"].hero
                    try:
                        del hero.backpack["totem"]
                    except KeyError:
                        pass
    clear_terminal()
    if hero.hp <= 0:
        print("\n\tМонстр вас убил. ПОРАЖЕНИЕ!\n\nИгра окончена.\n")
    else:
        print(
            "\n\tПОБЕДА!\n\tВы одолели 10 чудовищ и спасли "
            "Королевство от уничтожения!\n\nИгра окончена.\n"
        )
    quit()


if __name__ == "__main__":
    clear_terminal()
    if greeting():
        clear_terminal()
        game()
    else:
        clear_terminal()
        print(EPILOGUE)
