import random

from Classes.Factory.enemy_factory import EnemyFactory
from Classes.Factory.hero_factory import HeroFactory
from Classes.kingdom import Kingdom
from Classes.Strategy.aggressive_strategy import AggressiveStrategy
from Classes.Strategy.balanced_strategy import BalancedStrategy
from Classes.Strategy.defensive_strategy import DefensiveStrategy
from Classes.weapon import Weapon


def play_game():
    kingdom = Kingdom("Мобиус", territory=100, food=100)
    strategy_list = [AggressiveStrategy(), BalancedStrategy(), DefensiveStrategy()]

    sword = Weapon("Стальной клинок", 15)
    staff = Weapon("Посох стихий", 10)
    heroes = [
        HeroFactory.create_hero("warrior", "Артур", sword),
        HeroFactory.create_hero("mage", "Мерлин", staff),
    ]

    WIN_THRESHOLD = 250
    turn = 1

    print("=" * 55)
    print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'КОРОЛЕВСТВО'")
    print("=" * 55)

    while kingdom.is_alive():
        if kingdom.territory >= WIN_THRESHOLD and kingdom.food >= WIN_THRESHOLD:
            print("\nПОБЕДА! Ваше королевство процветает и достигло величия!")
            break

        alive_heroes = [h for h in heroes if h.is_alive]
        if not alive_heroes:
            print("\nВсе герои погибли. Королевство не может защищаться.")
            break

        print(f"\n{'=' * 20} ХОД {turn} {'=' * 20}")
        print(kingdom)
        print("\nВаши герои:")
        for i, h in enumerate(alive_heroes, 1):
            print(f"  {i}. {h}")

        try:
            choice_hero = int(input("\nВыберите номер героя для разведки: ")) - 1
            if choice_hero < 0 or choice_hero >= len(alive_heroes):
                print("Неверный номер. Пропуск хода.")
                turn += 1
                continue
            hero = alive_heroes[choice_hero]
        except ValueError:
            print("Введите число. Пропуск хода.")
            turn += 1
            continue

        print(hero.scout())

        enemy = EnemyFactory.create_random_enemy()
        print(f"Обнаружен противник: {enemy}")

        strategy = random.choice(strategy_list)
        base_prob = kingdom.battle_probability(hero, enemy)
        final_prob = strategy.modify_probability(base_prob)
        print(f"Вероятность победы: {base_prob}% | С тактикой: {final_prob}%")

        action = input("Сражаться? (y/n): ").strip().lower()

        if action != "y":
            print(f"{hero.name} отступает. Опыт снижается.")
            hero.gain_experience(-20)
            kingdom.lose_resources(5, 5)
            turn += 1
            continue

        roll = random.uniform(0, 100)
        if roll <= final_prob:
            print(f"{hero.name} одерживает победу!")
            hero.gain_experience(50)
            kingdom.gain_resources(15, 15)
        else:
            print(f"{hero.name} проигрывает бой!")
            kingdom.lose_resources(10, 10)
            hero.gain_experience(-10)

            if random.random() < 0.4:
                hero.is_alive = False
                print(f"{hero.name} погибает в бою.")
            else:
                print(f"{hero.name} выживает, но получает тяжелые раны.")

        turn += 1
        input("\nНажмите Enter для продолжения...")

    if not kingdom.is_alive():
        print("\nКоролевство пало. Ресурсы исчерпаны.")


if __name__ == "__main__":
    play_game()
