#from django.test import TestCase

# Create your tests here.

"""
Seeder for products app: Brand, Type, Category, Product, ProductTranslations.

Run either as:
    python manage.py shell -c "exec(open('products/test.py').read())"
or standalone (needs DJANGO_SETTINGS_MODULE):
    python products/test.py
"""
import os
import sys
import random
from decimal import Decimal

# ---- Django bootstrap (only for standalone `python products/test.py`) ----
if __name__ == "__main__":
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, PROJECT_ROOT)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
    import django
    django.setup()
# -------------------------------------------------------------------------

from django.db import transaction
from products.models import Brand, Type, Product, ProductTranslations
from category.models import Category


LANGUAGES = ["hy", "en", "ru"]

# ---------------- 50 Brands ----------------
BRANDS = [
    ("Կոկա-Կոլա",       "Coca-Cola",     "Кока-Кола"),
    ("Պեպսի",           "Pepsi",         "Пепси"),
    ("Նեստլե",          "Nestle",        "Нестле"),
    ("Դանոն",           "Danone",        "Данон"),
    ("Միլկա",           "Milka",         "Милка"),
    ("Օրեո",            "Oreo",          "Орео"),
    ("Լեյս",            "Lay's",         "Лейс"),
    ("Հայնց",           "Heinz",         "Хайнц"),
    ("Բարիլլա",         "Barilla",       "Барилла"),
    ("Նեսկաֆե",         "Nescafe",       "Нескафе"),
    ("Մարս",            "Mars",          "Марс"),
    ("Սնիկերս",         "Snickers",      "Сникерс"),
    ("Կիտ-Կատ",         "KitKat",        "Кит-Кат"),
    ("Ֆերրերո",         "Ferrero",       "Ферреро"),
    ("Կինդեր",          "Kinder",        "Киндер"),
    ("Կիտրոն",          "Fanta",         "Фанта"),
    ("Սպրայթ",          "Sprite",        "Спрайт"),
    ("Ռեդ Բուլ",        "Red Bull",      "Ред Булл"),
    ("Լիպտոն",          "Lipton",        "Липтон"),
    ("Յակոբս",          "Jacobs",        "Якобс"),
    ("Լավազա",          "Lavazza",       "Лавацца"),
    ("Իլլի",            "Illy",          "Илли"),
    ("Տվինինգս",        "Twinings",      "Твинингс"),
    ("Ահմադ",           "Ahmad Tea",     "Ахмад"),
    ("Գրինֆիլդ",        "Greenfield",    "Гринфилд"),
    ("Ռիչարդ",          "Richard",       "Ричард"),
    ("Մայսթեր",         "Maister",       "Майстер"),
    ("Հայգ",            "Haig",          "Хайг"),
    ("Չիվիտ",           "Chivit",        "Чивит"),
    ("Ալփեն Գոլդ",      "Alpen Gold",    "Альпен Голд"),
    ("Ռիտեր Սպորտ",     "Ritter Sport",  "Риттер Спорт"),
    ("Լինդթ",           "Lindt",         "Линдт"),
    ("Տոբլերոն",        "Toblerone",     "Тоблерон"),
    ("Պերնո Ռիկար",     "Pernod Ricard", "Перно Рикар"),
    ("Կամպարի",         "Campari",       "Кампари"),
    ("Ջեկ Դենիելս",     "Jack Daniel's", "Джек Дэниелс"),
    ("Ջոննի Ուոքեր",    "Johnnie Walker","Джонни Уокер"),
    ("Բալանթայնս",      "Ballantine's",  "Балантайнс"),
    ("Բակարդի",         "Bacardi",       "Бакарди"),
    ("Սմիրնոֆ",         "Smirnoff",      "Смирнофф"),
    ("Աբսոլուտ",         "Absolut",       "Абсолют"),
    ("Հայկական կոնյակ", "Armenian Cognac","Армянский коньяк"),
    ("Արարատ",          "Ararat",        "Арарат"),
    ("Նոյ",             "Noy",           "Ной"),
    ("Կիլիկիա",         "Kilikia",       "Киликия"),
    ("Գյումրի",          "Gyumri",        "Гюмри"),
    ("Բջնի",            "Bjni",          "Бжни"),
    ("Ջերմուկ",         "Jermuk",        "Джермук"),
    ("Սևան",            "Sevan",         "Севан"),
    ("Դիլիջան",         "Dilijan",       "Дилижан"),
]

# ---------------- 50 Types ----------------
TYPES = [
    ("Ըմպելիքներ",          "Beverages",            "Напитки"),
    ("Կաթնամթերք",          "Dairy",                "Молочные"),
    ("Քաղցրավենիք",         "Sweets",               "Сладости"),
    ("Խորտիկներ",           "Snacks",               "Закуски"),
    ("Մակարոն",             "Pasta",                "Макароны"),
    ("Պահածո",               "Canned Food",          "Консервы"),
    ("Սուրճ",               "Coffee",               "Кофе"),
    ("Թեյ",                 "Tea",                  "Чай"),
    ("Սոուսներ",            "Sauces",               "Соусы"),
    ("Սառեցված",            "Frozen",               "Замороженные"),
    ("Հացաբուլկեղեն",       "Bakery",               "Хлебобулочные"),
    ("Միս",                 "Meat",                 "Мясо"),
    ("Երշիկեղեն",           "Sausages",             "Колбасы"),
    ("Ձուկ",                "Fish",                 "Рыба"),
    ("Ծովամթերք",           "Seafood",              "Морепродукты"),
    ("Միրգ",                "Fruits",               "Фрукты"),
    ("Բանջարեղեն",          "Vegetables",           "Овощи"),
    ("Հատիկեղեն",           "Legumes",              "Бобовые"),
    ("Հացահատիկ",           "Cereals",              "Крупы"),
    ("Ալյուր",              "Flour",                "Мука"),
    ("Համեմունք",           "Spices",               "Специи"),
    ("Յուղ",                "Oil",                  "Масло"),
    ("Քացախ",               "Vinegar",              "Уксус"),
    ("Մեղր",                "Honey",                "Мёд"),
    ("Ջեմ",                 "Jam",                  "Варенье"),
    ("Շոկոլադ",             "Chocolate",            "Шоколад"),
    ("Կոնֆետ",              "Candy",                "Конфеты"),
    ("Թխվածք",              "Cookies",              "Печенье"),
    ("Տորթ",                "Cake",                 "Торт"),
    ("Պաղպաղակ",            "Ice Cream",            "Мороженое"),
    ("Յոգուրտ",             "Yogurt",               "Йогурт"),
    ("Պանիր",               "Cheese",               "Сыр"),
    ("Կարագ",               "Butter",               "Масло сливочное"),
    ("Ձու",                 "Eggs",                 "Яйца"),
    ("Հյութ",               "Juice",                "Сок"),
    ("Գազավորված",          "Soda",                 "Газированная"),
    ("Հանքային ջուր",       "Mineral Water",        "Минеральная вода"),
    ("Էներգետիկ",           "Energy Drink",         "Энергетик"),
    ("Գարեջուր",            "Beer",                 "Пиво"),
    ("Գինի",                "Wine",                 "Вино"),
    ("Օղի",                 "Vodka",                "Водка"),
    ("Կոնյակ",              "Cognac",               "Коньяк"),
    ("Վիսկի",               "Whiskey",              "Виски"),
    ("Ռոմ",                 "Rum",                  "Ром"),
    ("Մանկական սնունդ",     "Baby Food",            "Детское питание"),
    ("Կենդանիների կեր",     "Pet Food",             "Корм для животных"),
    ("Կենցաղային քիմիա",    "Household",            "Бытовая химия"),
    ("Կոսմետիկա",           "Cosmetics",            "Косметика"),
    ("Հիգիենա",             "Hygiene",              "Гигиена"),
    ("Դեղորայք",            "Medicine",             "Лекарства"),
]

# ---------------- 20 Categories ----------------
CATEGORIES = [
    ("Ըմպելիքներ",          "Beverages",           "Напитки"),
    ("Կաթնամթերք",          "Dairy",               "Молочные продукты"),
    ("Քաղցրավենիք",         "Sweets",              "Сладости"),
    ("Խորտիկներ",           "Snacks",              "Закуски"),
    ("Մակարոնեղեն",         "Pasta",               "Макароны"),
    ("Պահածոներ",           "Canned Food",         "Консервы"),
    ("Սուրճ",               "Coffee",              "Кофе"),
    ("Թեյ",                 "Tea",                 "Чай"),
    ("Սոուսներ և համեմունք","Sauces & Spices",     "Соусы и специи"),
    ("Սառեցված",            "Frozen",              "Замороженные"),
    ("Հացաբուլկեղեն",       "Bakery",              "Хлебобулочные"),
    ("Միս և երշիկեղեն",     "Meat & Sausages",     "Мясо и колбасы"),
    ("Ձուկ և ծովամթերք",     "Fish & Seafood",      "Рыба и морепродукты"),
    ("Միրգ և բանջարեղեն",   "Fruits & Vegetables", "Фрукты и овощи"),
    ("Մանկական սնունդ",     "Baby Food",           "Детское питание"),
    ("Կենդանիների կեր",     "Pet Food",            "Корм для животных"),
    ("Կենցաղային քիմիա",    "Household",           "Бытовая химия"),
    ("Կոսմետիկա",           "Cosmetics",           "Косметика"),
    ("Ալկոհոլային",         "Alcohol",             "Алкоголь"),
    ("Հացահատիկ և հատիկ",   "Cereals & Grains",    "Крупы и злаки"),
]


def run(product_count: int = 3000, batch_size: int = 500):
    with transaction.atomic():
        # ---------- Brands (50) ----------
        for hy, en, ru in BRANDS:
            Brand.objects.get_or_create(
                name_hy=hy,
                defaults={"name_en": en, "name_ru": ru},
            )
        brands = list(Brand.objects.all())

        # ---------- Types (50) ----------
        for hy, en, ru in TYPES:
            Type.objects.get_or_create(
                value_hy=hy,
                defaults={"value_en": en, "value_ru": ru},
            )
        types = list(Type.objects.all())

        # ---------- Categories (20) ----------
        for hy, en, ru in CATEGORIES:
            Category.objects.get_or_create(
                name_hy=hy,
                defaults={"name_en": en, "name_ru": ru},
            )
        categories = list(Category.objects.all())

        # ---------- Products (3000) ----------
        existing_articles = set(
            Product.objects.values_list("article", flat=True)
        )

        to_create = []
        for i in range(1, product_count + 1):
            article = f"ART-{i:05d}"
            if article in existing_articles:
                continue
            to_create.append(
                Product(
                    article=article,
                    brand=random.choice(brands),
                    type=random.choice(types),
                    price=Decimal(str(round(random.uniform(1.0, 50.0), 2))),
                    is_available=random.choice([True, False]),
                )
            )

        Product.objects.bulk_create(to_create, batch_size=batch_size)
        print(f"Created {len(to_create)} new products "
              f"(skipped {product_count - len(to_create)} existing).")

        products = list(Product.objects.all())

        # ---------- Translations ----------
        # Only create ones that don't exist yet (product, language) is unique.
        existing_pairs = set(
            ProductTranslations.objects.values_list("product_id", "language")
        )

        translations = []
        for p in products:
            for lang in LANGUAGES:
                if (p.id, lang) in existing_pairs:
                    continue
                translations.append(
                    ProductTranslations(
                        product=p,
                        language=lang,
                        name=f"Product {p.article} [{lang}]",
                        description=(
                            f"Auto-generated description for "
                            f"{p.article} in {lang}."
                        ),
                    )
                )

        ProductTranslations.objects.bulk_create(
            translations, batch_size=1000, ignore_conflicts=True
        )
        print(f"Created {len(translations)} new translations.")

        # ---------- Attach products to categories (M2M) ----------
        for cat in categories:
            k = random.randint(20, 80)          # how many per category
            k = min(k, len(products))
            picks = random.sample(products, k=k)
            cat.products.add(*picks)

    print("=" * 60)
    print(f"Brands:        {Brand.objects.count()}")
    print(f"Types:         {Type.objects.count()}")
    print(f"Categories:    {Category.objects.count()}")
    print(f"Products:      {Product.objects.count()}")
    print(f"Translations:  {ProductTranslations.objects.count()}")
    print("=" * 60)


if __name__ == "__main__":
    run()