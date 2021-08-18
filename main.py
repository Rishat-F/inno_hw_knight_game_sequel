import random
import os


PROLOGUE = "\n\tДобро пожаловать в сказочную игру \"Герой и Монстры\"!\n\n" \
           "\tКоролевству угрожает нападение со стороны 10 монстров!\n" \
           "\tЛишь отважные и сильные способны спасти Королевство...\n"
EPILOGUE = "\n\tМного смельчаков пало в битве с монстрами...\n" \
           "\tНо никто не смог остановить их.\n" \
           "\tВ итоге Королевство было разрушено чудовищами...\n\n" \
           "\tВы проиграли!\n\n" \
           "Игра окончена."
monster_counter = 0
MONSTERS_TO_WIN = 10
MELEE_TYPE = "melee"
RANGE_TYPE = "range"
MAGE_TYPE = "mage"
TYPES = {"1": MELEE_TYPE, "2": RANGE_TYPE, "3": MAGE_TYPE}
HERO_START_HP = 20
EVATION_CHANCE = 50
DEFAULT_ATTACK = 2


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


def print_hero_stats(hero) -> None:
    """Print stats and game steps in pretty view."""
    clear_terminal()
    print(
        f"----------------------------------------------\n"
        f"Герой:\n"
        f"hp: {hero.hp}   Класс: {hero.type}   Оружие: {hero.weapon}   Рюкзак: {hero.backpack}\n"
        f"\nОсталось одолеть {MONSTERS_TO_WIN - monster_counter} монстров\n"
        f"----------------------------------------------"
    )


def print_battle_stats(hero, monster) -> None:
    """Print stats and game steps in pretty view."""
    print_hero_stats(hero)
    if monster.hp > 0:
        print(
            f"Монстр:\n"
            f"hp: {monster.hp}   Класс: {monster.type}   Атака: {monster.attack}\n"
        )


def random_meeting():
    meeting = random.choice([Sword, Bow, Book, Quiver, Apple, Monster])
    if issubclass(meeting, Weapon):
        return meeting(random.randint(6, 15))
    elif issubclass(meeting, Thing):
        return meeting(random.randint(3, 6))
    elif meeting is Monster:
        return meeting(random.randint(5, 12), random.randint(5, 12))


class Unit:

    def __init__(self, hp):
        self.hp = hp

    def __str__(self):
        return self.__class__.__name__


class AbleToEvade:

    chance = EVATION_CHANCE

    def _can_evade_enemy_hit(self, enemy):
        if isinstance(self, Monster) and isinstance(enemy, Hero) and self.type == enemy.weapon.attack_type:
            return True
        elif isinstance(self, Hero) and isinstance(enemy, Monster) and self.type == enemy.type:
            return True
        else:
            return False

    def evade_hit(self, enemy):
        if self._can_evade_enemy_hit(enemy):
            return random.choices([True, False], [self.chance, 100 - self.chance])[0]
        else:
            return False


class AbleToAttack:

    def __init__(self, attack):
        self.attack = attack

    def attack_enemy(self, enemy):
        if isinstance(enemy, AbleToEvade):
            if enemy.evade_hit(self):
                print(f"{str(enemy)} увернулся от удара")
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

    def __init__(self, hero):
        super().__init__()
        self.hero = hero
        self.monster_counter = monster_counter

    def __repr__(self):
        return f"Сохранение с {self.hero.hp} hp"


def game() -> None:
    default_sword = Sword(DEFAULT_ATTACK)
    hero = Hero(HERO_START_HP, default_sword)
    global monster_counter
    while hero.hp > 0 and monster_counter < 10:
        print_hero_stats(hero)
        meeting = random_meeting()  # тут нужна фабрика, которая будет выдавать рандомно объекты вещей, оружия или монстров
        if isinstance(meeting, Apple):
            hero.hp += meeting.hp
            print_hero_stats(hero)
            print(
                f"\nВы нашли яблоко и съели его.\n"
                f"Кол-во единиц здоровья увеличилось на {meeting.hp}."
            )
            input("\n\tНажмите Enter\n")
        elif isinstance(meeting, Weapon):
            print(f"\nВы нашли {meeting.type}, который дает {meeting.attack} ед. урона.")
            choice = input(
                f"\n\tВведите 1, чтобы подобрать новый {meeting.type}.\n"
                f"\tВведите 2, чтобы пройти мимо.\n"
            )
            while choice not in ("1", "2"):
                choice = input(
                    f"\nНекорректный ввод.\n"
                    f"\tВведите 1, чтобы подобрать новый {meeting.type}.\n"
                    f"\tВведите 2, чтобы пройти мимо.\n"
                )
            if choice == "1":
                hero.pick_up(meeting)
        elif isinstance(meeting, Quiver):
            print(f"\nВы нашли {meeting.type}, с {meeting.arrows} стрелами.")
            choice = input(
                f"\n\tВведите 1, чтобы подобрать {meeting.type}.\n"
                f"\tВведите 2, чтобы пройти мимо.\n"
            )
            while choice not in ("1", "2"):
                choice = input(
                    f"\nНекорректный ввод.\n"
                    f"\tВведите 1, чтобы подобрать {meeting.type}.\n"
                    f"\tВведите 2, чтобы пройти мимо.\n"
                )
            if choice == "1":
                hero.pick_up(meeting)
        elif isinstance(meeting, Monster):
            print_battle_stats(hero, meeting)
            print(
                f"\nБОЙ! На вас напало {meeting.type}-чудовище с {meeting.hp} ед. "
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
                    print_battle_stats(hero, meeting)
                    choice = input(
                        "\nНекорректный ввод.\n\tВведите 0, чтобы убежать.\n"
                        "\tВведите 1, чтобы атаковать чудовище текущим оружием.\n"
                        "\tВведите 2, чтобы сменить оружие перед атакой.\n"
                    )
                if choice == "2":
                    print_battle_stats(hero, meeting)
                    hero.change_weapon()
                    print_battle_stats(hero, meeting)
                    continue
                elif choice == "1":
                    meeting.attack_enemy(hero)
                    hero.attack_enemy(meeting)
                print_battle_stats(hero, meeting)
            if hero.hp > 0 and meeting.hp <= 0:
                monster_counter += 1
                if monster_counter != 10:
                    print_hero_stats(hero)
                    print("\nВы одолели чудовище!")
                    input("\n\tНажмите Enter\n")
    clear_terminal()
    if hero.hp <= 0:
        print("\n\tМонстр вас убил. ПОРАЖЕНИЕ!\n\nИгра окончена.\n")
    else:
        print(
            "\n\tПОБЕДА!\nВы одолели 10 чудовищ и спасли "
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
