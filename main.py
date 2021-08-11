import random


monster_counter = 0
TYPES = {"1": "melee", "2": "range", "3": "mage"}
HERO_START_HP = 20


def greeting():
    print(
        '\nДобро пожаловать в сказочную игру "Герой и Монстры"!\n\n'
        "Королевству угрожает нападение со стороны 10 монстров!\n"
        "Лишь отважные и сильные способны спасти Королевство...\n"
    )
    choice = input("Готовы бросить вызов опасности? [y/n]\n").lower()
    while choice not in ("y", "n", "yes", "no", "\n", ""):
        choice = input('\nВведите "y" или "no" чтобы продолжить игру:\n')
    if choice.startswith("y") or choice in ("\n", ""):
        return True
    return False


def choose_hero():
    choice = input(
        "\n\tВведите 1, чтобы играть Воином.\n"
        "\tВведите 2, чтобы играть Лучником.\n"
        "\tВведите 3, чтобы играть Магом.\n"
    )
    while choice not in ("1", "2", "3"):
        choice = input(
            "\nНекорректный ввод.\n"
            "\tВведите 1, чтобы играть Воином.\n"
            "\tВведите 2, чтобы играть Лучником.\n"
            "\tВведите 3, чтобы играть Магом.\n"
        )
    return TYPES[choice]


def random_meeting():
    meeting = random.choice([Sword, Bow, Book, Quiver, Apple, Monster])
    if meeting is Weapon:
        return meeting(random.randint(6, 15))
    elif meeting is Quiver:
        return meeting(random.randint(3, 6))
    elif meeting is Apple:
        return meeting(random.randint(3, 6))
    elif meeting is Monster:
        return meeting(random.randint(5, 12), random.randint(5, 12))


class Unit:

    def __init__(self, hp):
        self.hp = hp


class Monster(Unit):

    def __init__(self, hp, attack):
        super().__init__(hp)
        self.attack = attack
        self.type = random.choice(list(TYPES.values()))

    def __repr__(self):
        return f"{self.__class__.__name__} (hp = {self.hp}, attack = {self.attack}, type = {self.type})"


class Hero(Unit):

    def __init__(self, hp, type, sword):
        super().__init__(hp)
        self.type = type
        self.backpack = {
            "sword": sword,
        }
        self.weapon = sword
        self.attack = self.weapon.attack

    def __repr__(self):
        return f"{self.__class__.__name__} (hp = {self.hp}, attack = {self.attack}, type = {self.type})"

    def pick_up_weapon(self, weapon):
        self.backpack[weapon.type] = weapon

    def pick_up_quiver(self, quiver):
        self.backpack.setdefault("arrows", 0)
        self.backpack["arrows"] += quiver.arrows


    def change_weapon(self):
        choice = input(
            f"Введите оружие, которое хотите выбрать: {[weapon for weapon in self.backpack]}"
        )
        self.weapon = self.backpack[choice]


class Thing:

    def __init__(self):
        self.type = self.__class__.__name__.lower()


class Weapon(Thing):

    def __init__(self, attack):
        super().__init__()
        self.attack = attack

    def __repr__(self):
        return f"{self.__class__.__name__} (attack = {self.attack})"


class Sword(Weapon):

    def __init__(self, attack=10):
        super().__init__(attack)


class Bow(Weapon):

    def __init__(self, attack):
        super().__init__(attack)


class Book(Weapon):

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

    def __init__(self):
        super().__init__()
        pass


def game() -> None:
    hero_class = choose_hero()
    default_sword = Sword()
    hero = Hero(HERO_START_HP, hero_class, default_sword)
    global monster_counter
    while hero.hp > 0 and monster_counter < 10:
        input("\n\tНажмите ENTER, чтобы перейти к следующему ходу\n")
        meeting = random_meeting()  # тут нужна фабрика, которая будет выдавать рандомно объекты вещей или оружия
        if isinstance(meeting, Apple):
            hero.hp += meeting.hp
            print(
                f"\nВы нашли яблоко и съели его.\n"
                f"Кол-во единиц здоровья увеличилось на {meeting.hp}."
            )
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
            if choice == "2":
                print(f"\nВы не стали подбирать новый {meeting.type}.")
            else:
                hero.pick_up_weapon(meeting)
                print(f"\nВы подобрали новый {meeting.type}.")
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
            if choice == "2":
                print(f"\nВы не стали подбирать {meeting.type}.")
            else:
                hero.pick_up_weapon(meeting)
                print(f"\nВы подобрали {meeting.type}.")
        elif isinstance(meeting, Monster):
            print(
                f"\nБОЙ! На вас напало {meeting.type}-чудовище с {meeting.hp} ед. "
                f"здоровья и с атакой в {meeting.attack} ед. урона."
            )
            choice = input(
                "\n\tВведите 1, чтобы вступить в схватку с чудовищем.\n"
                "\tВведите 2, чтобы убежать.\n"
            )
            while choice not in ("1", "2"):
                choice = input(
                    "\nНекорректный ввод.\n\tВведите 1, чтобы вступить "
                    "в схватку с чудовищем.\n"
                    "\tВведите 2, чтобы убежать.\n"
                )
            if choice == "1":
                while hero.hp > 0 and meeting.hp > 0:
                    hero.hp -= meeting.attack
                    meeting.hp -= hero.attack
                if hero.hp > 0:
                    monster_counter += 1
                    if monster_counter != 10:
                        print("\nВы одолели чудовище!")
            else:
                print("\nВы убежали.")
    if hero.hp <= 0:
        print("\nМонстр вас убил. ПОРАЖЕНИЕ!\n\nИгра окончена.\n")
    else:
        print(
            "\nПОБЕДА!\nВы одолели 10 чудовищ и спасли "
            "Королевство от уничтожения!\n\nИгра окончена.\n"
        )
    quit()


if __name__ == "__main__":
    if greeting():
        print("\nИгра началась, удачи!")
        game()
    else:
        print(
            "\nМного смельчаков пало в битве с монстрами...\n"
            "Но никто не смог остановить их.\n"
            "В итоге Королевство было разрушено чудовищами...\n\n"
            "Вы проиграли!\n\n"
            "Игра окончена."
            )
