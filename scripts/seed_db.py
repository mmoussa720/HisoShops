import asyncio
from faker import Faker
from src.infrastructure.database.session import local_session
from src.modules.users.schemas import UserCreate
from src.modules.users.services import UserService
from src.modules.categories import CategoryService
from src.modules.products.schemas import ProductCreate
from src.modules.products.services import ProductService
from src.modules.reviews.schemas import ReviewCreate
from src.modules.reviews.services import ReviewService

fake = Faker()


async def seed_db():
    user_service = UserService()
    category_service = CategoryService()
    product_service = ProductService()
    review_service = ReviewService()

    async with local_session() as db:
        # --- Seed Users ---
        user_ids = []
        for _ in range(10):
            user_data = UserCreate(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                user_name=fake.user_name()[:20],
                email=fake.unique.email(),
                password="Password#123",
            )
            try:
                result = await user_service.create_user(user_data, db)
                user_ids.append(result["id"])
                print(f"Created user: {result['user_name']}")
            except Exception as e:
                await db.rollback()
                print(f"Skipped user: {e}")

        # --- Seed Categories ---
        categories_data = [
            {"name": "Clothes", "description": "Fashion and apparel for all seasons"},
            {"name": "Gaming", "description": "Gaming gear, consoles, and accessories"},
            {"name": "Electronics", "description": "Electronic devices and gadgets"},
            {"name": "Sports", "description": "Sports equipment and activewear"},
            {"name": "Beauty", "description": "Beauty and personal care products"},
            {"name": "Books", "description": "Books across all genres"},
        ]
        category_ids = {}
        for cat in categories_data:
            try:
                result = await category_service.create_category(
                    type("CatCreate", (), {"name": cat["name"], "description": cat["description"]})(),
                    db,
                )
                category_ids[cat["name"]] = result["id"]
                print(f"Created category: {cat['name']}")
            except Exception as e:
                await db.rollback()
                print(f"Skipped category {cat['name']}: {e}")

        # --- Seed Products ---
        products_data = [
            {"name": "Classic T-Shirt", "description": "Comfortable cotton t-shirt", "price": 19.99, "size": "M", "category": "Clothes", "quantity": 50},
            {"name": "Denim Jacket", "description": "Stylish denim jacket", "price": 89.99, "size": "L", "category": "Clothes", "quantity": 30},
            {"name": "Gaming Keyboard", "description": "Mechanical RGB keyboard", "price": 129.99, "size": None, "category": "Gaming", "quantity": 25},
            {"name": "Wireless Mouse", "description": "Ergonomic wireless mouse", "price": 49.99, "size": None, "category": "Gaming", "quantity": 40},
            {"name": "Smartphone", "description": "Latest model smartphone", "price": 699.99, "size": None, "category": "Electronics", "quantity": 15},
            {"name": "Bluetooth Speaker", "description": "Portable waterproof speaker", "price": 39.99, "size": None, "category": "Electronics", "quantity": 60},
            {"name": "Yoga Mat", "description": "Non-slip exercise mat", "price": 29.99, "size": None, "category": "Sports", "quantity": 100},
            {"name": "Running Shoes", "description": "Lightweight running shoes", "price": 119.99, "size": "L", "category": "Sports", "quantity": 20},
            {"name": "Moisturizer", "description": "Hydrating face moisturizer", "price": 24.99, "size": None, "category": "Beauty", "quantity": 80},
            {"name": "Lipstick Set", "description": "Matte lipstick collection", "price": 34.99, "size": None, "category": "Beauty", "quantity": 45},
            {"name": "Mystery Novel", "description": "Bestselling thriller book", "price": 14.99, "size": None, "category": "Books", "quantity": 200},
            {"name": "Cookbook", "description": "Gourmet recipes cookbook", "price": 24.99, "size": None, "category": "Books", "quantity": 75},
        ]
        product_slugs = []
        for prod in products_data:
            try:
                result = await product_service.create_product(
                    ProductCreate(
                        name=prod["name"],
                        description=prod["description"],
                        price=prod["price"],
                        size=prod["size"],
                        quantity=prod["quantity"],
                        category_ids=[category_ids[prod["category"]]],
                    ),
                    image_url=None,
                    db=db,
                )
                product_slugs.append(result["slug"])
                print(f"Created product: {prod['name']}")
            except Exception as e:
                await db.rollback()
                print(f"Skipped product {prod['name']}: {e}")

        # --- Seed Reviews ---
        for i, slug in enumerate(product_slugs):
            for j in range(min(3, len(user_ids))):
                try:
                    user_idx = (i * 3 + j) % len(user_ids)
                    await review_service.create_review(
                        ReviewCreate(
                            rating=fake.random_int(1, 5),
                            comment=fake.sentence(),
                            product_slug=slug,
                        ),
                        user_id=user_ids[user_idx],
                        db=db,
                    )
                    print(f"Created review for product slug {slug}")
                except Exception as e:
                    await db.rollback()
                    print(f"Skipped review: {e}")

        await db.commit()
    print("Seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed_db())
