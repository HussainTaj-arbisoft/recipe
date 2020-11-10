import datetime
import decimal
import random
import time

from account.models import User
from recipe.models import Ingredient, Recipe, Review

RECIPE_INSTRUCTIONS_LOREM = r"""
# Tamen spem remis semel longave cum pisces

## Euhan mactati ab alios dolorem erat suspenderat

Lorem markdownum aeris innumerasque feretro igni; solumque protinus Pelion. Illa
cornus. Ipsi iuvencos iactantem deos, **quod in** suum **utendum**. Seducta
hostilique invisi Broteasque animi concitus mactassent ensem, de latus, *te se*
videres Schoeneia nunc.

> Vidistis electra suo nymphas satiata quas dici multorum vertice exsiluere
> prosiluit sunt dis, nec iuga, poscimus. Victum auras tot tellus fecundaque,
> praefoderat cecidit talia astris ut mecum pecoris hominem
> [esse](http://urbes.org/velpenna)?

Ait et vale. Charaxi fuit moenia Maeonios, quisquis! Et nulla: torsit et
contulit hastam consequitur aptius petiit Maenaliosque languentique admonitu
dixit est primusque dixit est di cunctantem. Deas constantia vi tecum vesci
venturi, pharetras et medio, labitur iam manant nubila, ne tum.

Visu sacra petis condidit iniuria sedes: et laure pariter iocos pereat sunt
armos lucis? Nostris ceras: mole quam, aera arma, postquam a Iolen profusis.

## Nantemque mea nullo haud

Caelo tamen odoro precatus Europaei fugit *huc quae ludere* aequorei volenti
[levius](http://www.inrita.io/ne) ut vix adest. Alienae inmunitamque quis
dixerat tum Rhodanumque illa captivis referre eluserat! Quoque in expulit Minyae
dant Est Virbius pictis. Et pars vento quid, arreptum et **numen vapor quibus**
ab gemitus, ab nam fontis! Hora mihi Iuppiter herbosaque neque, sub cubito
concutit Aeacide sicut aequora?

- Est erat sed stamen Cereris solitaeque haec
- Tempore Tantalides audito
- Tetenderat prima voluit uni manus
- Resupinum sonis

Et **timuere** rupibus, intorquet adversaque frustraque passi, nec populus.
Suspirat concita puerile: bella et munere fiducia strigis pumice nolet malo
retro sua tuos augustae, [venturi](http://os.com/).

Medium gentes non more solebat sed Alcidae inque, vera respiramina, qui cornua.
Post creverunt petentem sunt, caedis totumque nodosa. Potuisse Balearica huius
acrior umentes enixa non artior oppositumque pellite posuit, nec. Parvam qui
admiremur, flava, insula negat; et amisit cervice, cum corpus gratulor forma
sustinet sub.

Celebrabant iura scopulum locum. Nunc *undas* sanguine auro et silvae in feror
recenti. Est laborum nocte, tua aqua io dotem placet latentem coxerat pallam,
nec hic? Stagno utque, remigioque nitenti datum. At hoc matrisque locis dixit
fluidoque pennis, dum hunc.
"""


FOOD_IMAGE_URLS = [
    "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
    "https://health.clevelandclinic.org/wp-content/uploads/sites/3/2019/06/cropped-GettyImages-643764514.jpg",
    "https://www.helpguide.org/wp-content/uploads/fast-foods-candy-cookies-pastries-768.jpg",
    "https://c.ndtvimg.com/2020-04/dih4ifhg_pasta_625x300_22_April_20.jpg",
    "https://www.rnz.co.nz/assets/news_crops/60885/eight_col_32917696_l.jpg",
    "https://jbssa.com/images/home/banner-PilgrimsCall-mob2.jpg",
    "https://static01.nyt.com/images/2020/01/24/dining/yk-gochujang-chicken-and-vegetables/merlin_167664060_7435c624-7225-4cb1-b104-4d67761185a4-articleLarge.jpg",
    "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg",
]


TAGS = ["tag-a", "tag-b", "tag-c", "tag-d", "tag-e", "tag-f", "tag-g", "tag-h"]


def seed_user(users_count: int = 50):
    User.objects.all().delete()
    print("Old Users Deleted.")

    print(f"Seeding {users_count} users...")
    for user_number in range(users_count):
        user = User(
            first_name=f"User {user_number}",
            email=f"user{user_number}@test.com",
            username=f"user{user_number}@test.com",
        )
        user.set_password(f"testuser")

        user.save()

        print(f"Progress: {((user_number+1)/users_count * 100):.2f}%", end="\r")
    print()


def seed_recipe(recipes_count: int = 200, ingredients_range: (int, int) = (5, 15)):
    Recipe.objects.all().delete()
    Ingredient.objects.all().delete()
    print("Old Recipes and Ingredients deleted.")

    users = User.objects.all()

    print(f"Seeding {recipes_count} recipes...")
    for recipe_number in range(recipes_count):
        recipe = Recipe(
            title=f"Recipe Number {recipe_number} title.",
            instructions=RECIPE_INSTRUCTIONS_LOREM,
            author=random.choice(users),
            prep_time=datetime.timedelta(minutes=random.randint(20, 70)),
            pub_date=time.localtime(),
            image_url=random.choice(FOOD_IMAGE_URLS),
            slug=f"recipe-number-{recipe_number}-title",
        )
        recipe.save()
        recipe.tags.set(*random.choices(k=random.randint(1, 4), population=TAGS))

        for ingredient_number in range(
            random.randint(ingredients_range[0], ingredients_range[1])
        ):
            dec = decimal.Decimal(random.randint(1, 99))
            ingredient = Ingredient(
                name=f"ingredient {ingredient_number}",
                amount=dec,
                unit=random.choice(Ingredient.UNIT_CHOICES)[0],
                recipe=recipe,
            )
            ingredient.save()

        print(f"Progress: {((recipe_number + 1)/recipes_count * 100):.2f}%", end="\r")
    print()


def seed_review(review_count_range: (int, int) = (5, 15)):
    Review.objects.all().delete()
    print("Old reviews Deleted")

    recipes = Recipe.objects.all()
    users = User.objects.all()

    count = 0
    total = len(recipes)

    print(f"Seeding reviews for {total} recipes...")
    for recipe in recipes:
        for review_number in range(random.randint(*review_count_range)):
            review = Review(
                recipe=recipe,
                rating=random.randint(1, 5),
                comment=f"Comment {review_number}",
                user=random.choice(users),
            )
            review.save()

        count += 1
        print(f"Progress: {((count)/total * 100):.2f}%", end="\r")
    print()


def seed_superuser():
    user = User(is_superuser=True, email="admin@test.com", username="admin")
    user.set_password("admin")
    user.save()

    print("Super user created.")
    print(f"Username: {user.username}")
    print("Password: admin")


def seed_all_default():
    seed_user()
    seed_recipe()
    seed_review()
    seed_superuser()


# # Usage
#
# $ python manage.py shell
#
"""
from recipe_project.db_seeder import *
seed_all_default()
"""
