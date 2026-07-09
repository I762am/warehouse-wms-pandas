import os
import random
from colorama import Fore, Style, init
import pandas as pd

init(autoreset=True)

ERP_FILE = "enterprise_erp.xlsx"
LOCATIONS_FILE = "warehouse_locations.xlsx"


def generate_huge_data():
    print(f"\n⏳ Генерируем 10 000 позиций с кодами от ПЛ-1 до ПЛ-10000...")

    erp_data = []
    loc_data = []

    for i in range(1, 10001):
        item_code = f"ПЛ-{i}"
        name = random.choice(["Керамогранит", "Кафель", "Мозаика"]) + f" СТИЛЬ-{i}"
        quantity = random.randint(1, 15)

        gate = f"B-{random.randint(1, 5)}"
        floor = random.randint(1, 10)
        row = f"Р-{random.randint(1, 50)}"

        erp_data.append({"Код_Товара": item_code, "Наименование": name, "Количество": quantity})
        loc_data.append({"Код_Товара": item_code, "Ворота": gate, "Этаж": floor, "Ряд": row})

    pd.DataFrame(erp_data).to_excel(ERP_FILE, index=False)
    pd.DataFrame(loc_data).to_excel(LOCATIONS_FILE, index=False)
    print(f" База на 10 000 товаров успешно создана! Коды: от ПЛ-1 до ПЛ-10000.")


def find_item_in_warehouse():
    if not os.path.exists(ERP_FILE) or not os.path.exists(LOCATIONS_FILE):
        print(
            Fore.RED
            + " Базы данных не найдены! Сначала запустите генерацию (Пункт 3)."
        )
        return

    item_code = input("\n🔎 Введи Код_Товара для поиска (например, ПЛ-10005): ").strip()

    df_erp = pd.read_excel(ERP_FILE)
    df_loc = pd.read_excel(LOCATIONS_FILE)

    res_erp = df_erp[df_erp["Код_Товара"].astype(str) == item_code]
    res_loc = df_loc[df_loc["Код_Товара"].astype(str) == item_code]

    if res_erp.empty or res_loc.empty:
        print(Fore.RED + f"❌ Товар {item_code} не найден в базах.")
        return

    erp_row = res_erp.iloc[0]
    loc_row = res_loc.iloc[0]

    qty = int(erp_row["Количество"])

    print(f"\n📦 Товар: {erp_row['Наименование']}")
    print(
        f"📍 Адрес хранения: Ворота {loc_row['Ворота']}, Этаж {loc_row['Этаж']}, Ряд {loc_row['Ряд']}"
    )

    if qty < 5:
        print(
            Fore.RED
            + Style.BRIGHT
            + f"⚠️ КРИТИЧЕСКИЙ ОСТАТОК: Всего {qty} шт! Позиция штучная, ищи внимательно."
        )
    else:
        print(Fore.GREEN + f"✅ Остаток на складе: {qty} шт.")


def update_coordinates():
    if not os.path.exists(LOCATIONS_FILE):
        print(Fore.RED + "❌ База адресов не найдена.")
        return

    item_code = input(
        "\n✏️ Введи Код_Товара, который перекладываешь: "
    ).strip()

    df_loc = pd.read_excel(LOCATIONS_FILE)
    mask = df_loc["Код_Товара"].astype(str) == item_code

    if df_loc[mask].empty:
        print(Fore.RED + f"❌ Товар {item_code} не найден.")
        return

    print(f"Товар найден. Введи новые координаты:")
    new_gate = input("Новые Ворота: ").strip()
    new_floor = input("Новый Этаж: ").strip()
    new_row = input("Новый Ряд: ").strip()

    df_loc.loc[mask, "Ворота"] = new_gate
    df_loc.loc[mask, "Этаж"] = new_floor
    df_loc.loc[mask, "Ряд"] = new_row

    df_loc.to_excel(LOCATIONS_FILE, index=False)
    print(Fore.GREEN + f"✅ Новое местоположение для {item_code} сохранено!")


def main():
    while True:
        print(f"\n--- WMS СИСТЕМА АДРЕСНОГО ХРАНЕНИЯ (СТАТУС: РАБОТАЕТ) ---")
        print("1. Найти плитку по коду")
        print("2. Переложить плитку (Обновить адрес)")
        print("3. Сгенерировать Big Data базу (10 000 товаров)")
        print("4. Выйти из программы")

        choice = input("\nВыбери действие (1-4): ").strip()

        if choice == "1":
            find_item_in_warehouse()
        elif choice == "2":
            update_coordinates()
        elif choice == "3":
            generate_huge_data()
        elif choice == "4":
            print("Выключение системы. До связи!")
            break
        else:
            print(Fore.YELLOW + "❌ Неверный ввод, выбери цифру от 1 до 4.")


if __name__ == "__main__":
    main()
