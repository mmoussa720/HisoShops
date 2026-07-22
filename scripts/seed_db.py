import asyncio
from faker import Faker
from sqlalchemy import select
from src.infrastructure.database.session import local_session
from src.modules.users.schemas import UserCreate
from src.modules.users.services import UserService
from src.modules.users.models import User
from src.modules.categories.schemas import CategoryCreate
from src.modules.categories.services import CategoryService
from src.modules.categories.models import Category
from src.modules.products.schemas import ProductCreate
from src.modules.products.services import ProductService
from src.modules.products.models import Product
from src.modules.products.types import Size
from src.modules.reviews.schemas import ReviewCreate
from src.modules.reviews.services import ReviewService
from src.modules.reviews.models import Review
from src.modules.cart.schemas import CartCreate
from src.modules.cart.services import CartService
from src.modules.riders.schemas import RiderCreate
from src.modules.riders.services import RiderService
from src.modules.riders.models import Rider
from src.modules.orders.schemas import OrderCreate, OrderItemBase, OrderUpdate
from src.modules.orders.services import OrderService

fake = Faker()

CATEGORIES = [
    "Clothes", "Gaming", "Electronics", "Sports",
    "Beauty", "Books", "Home", "Toys", "Automotive", "Food",
]

PRODUCT_DATA = [
    ("Classic T-Shirt", "Comfortable cotton t-shirt", 19.99, Size.m),
    ("Gaming Keyboard", "Mechanical RGB keyboard", 129.99, None),
    ("Smartphone", "Latest model smartphone", 699.99, None),
    ("Yoga Mat", "Non-slip exercise mat", 29.99, None),
    ("Moisturizer", "Hydrating face moisturizer", 24.99, None),
    ("Mystery Novel", "Bestselling thriller book", 14.99, None),
    ("Desk Lamp", "LED desk lamp with dimmer", 39.99, None),
    ("LEGO Set", "Building block set for all ages", 49.99, None),
    ("Car Phone Mount", "Universal car phone holder", 15.99, None),
    ("Organic Coffee", "Premium arabica coffee beans", 18.99, None),
]


async def seed_db():
    user_service = UserService()
    category_service = CategoryService()
    product_service = ProductService()
    review_service = ReviewService()
    cart_service = CartService()
    rider_service = RiderService()
    order_service = OrderService()

    async with local_session() as db:
        # --- Seed Users ---
        user_ids = []
        print("=== Seeding Users ===")
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
                print(f"  Created user: {result['user_name']}")
            except Exception:
                await db.rollback()
                existing = await db.execute(
                    select(User).where(User.email == user_data.email)
                )
                user = existing.scalar_one_or_none()
                if user:
                    user_ids.append(user.id)
                    print(f"  Fetched existing user: {user.user_name}")

        # --- Seed Categories ---
        category_ids = {}
        print("\n=== Seeding Categories ===")
        for cat_name in CATEGORIES:
            try:
                result = await category_service.create_category(
                    CategoryCreate(name=cat_name, description=fake.sentence()),
                    db,
                )
                category_ids[cat_name] = result["id"]
                print(f"  Created category: {cat_name}")
            except Exception:
                await db.rollback()
                row = await db.execute(select(Category).where(Category.name == cat_name))
                existing = row.scalar_one_or_none()
                if existing:
                    category_ids[cat_name] = existing.id
                    print(f"  Fetched existing category: {cat_name}")

        cat_names = list(category_ids.keys())

        # --- Seed Products ---
        product_ids = []
        product_slugs = []
        product_prices = {}
        print("\n=== Seeding Products ===")
        for i in range(10):
            name, desc, price, size = PRODUCT_DATA[i]
            cat_name = cat_names[i % len(cat_names)]
            try:
                result = await product_service.create_product(
                    ProductCreate(
                        name=name,
                        description=desc,
                        price=price,
                        size=size,
                        quantity=fake.random_int(min=5, max=200),
                        category_ids=[category_ids[cat_name]],
                    ),
                    image_url=None,
                    db=db,
                )
                product_ids.append(result["id"])
                product_slugs.append(result["slug"])
                product_prices[result["id"]] = price
                print(f"  Created product: {result['name']}")
            except Exception:
                await db.rollback()
                row = await db.execute(select(Product).where(Product.name == name))
                existing = row.scalar_one_or_none()
                if existing:
                    product_ids.append(existing.id)
                    product_slugs.append(existing.slug)
                    product_prices[existing.id] = existing.price
                    print(f"  Fetched existing product: {existing.name}")

        # --- Seed Reviews ---
        print("\n=== Seeding Reviews ===")
        for i in range(10):
            user_idx = i % len(user_ids)
            product_idx = i % len(product_slugs)
            try:
                await review_service.create_review(
                    ReviewCreate(
                        rating=fake.random_int(1, 5),
                        comment=fake.sentence(),
                        product_slug=product_slugs[product_idx],
                    ),
                    user_id=user_ids[user_idx],
                    db=db,
                )
                print(f"  Created review #{i+1}")
            except Exception:
                await db.rollback()
                print(f"  Skipped review #{i+1} (likely duplicate user+product)")

        # --- Seed Cart Items ---
        print("\n=== Seeding Cart Items ===")
        for i in range(10):
            user_idx = i % len(user_ids)
            product_idx = i % len(product_ids)
            pid = product_ids[product_idx]
            try:
                await cart_service.add_to_cart(
                    CartCreate(
                        product_name=PRODUCT_DATA[product_idx][0],
                        size=PRODUCT_DATA[product_idx][3].value if PRODUCT_DATA[product_idx][3] else None,
                        quantity=fake.random_int(min=1, max=5),
                        unit_price=product_prices[pid],
                        product_id=pid,
                    ),
                    user_id=user_ids[user_idx],
                    db=db,
                )
                print(f"  Created cart item #{i+1}")
            except Exception:
                await db.rollback()
                print(f"  Skipped cart item #{i+1} (likely duplicate)")

        # --- Seed Riders ---
        rider_ids = []
        print("\n=== Seeding Riders ===")
        for _ in range(10):
            try:
                result = await rider_service.create_rider(
                    RiderCreate(
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        phone_number=fake.numerify("##########"),
                        email=fake.unique.email(),
                    ),
                    db=db,
                )
                rider_ids.append(result["id"])
                print(f"  Created rider: {result['first_name']} {result['last_name']}")
            except Exception:
                await db.rollback()
                existing_riders = await db.execute(select(Rider.id).limit(10))
                rider_ids = [r[0] for r in existing_riders.fetchall()]
                if rider_ids:
                    print(f"  Fetched {len(rider_ids)} existing riders")
                break

        # --- Seed Orders ---
        print("\n=== Seeding Orders ===")
        statuses = ["pending", "processing", "shipped", "delivered"]
        for i in range(10):
            user_idx = i % len(user_ids)
            product_idx = i % len(product_ids)
            pid = product_ids[product_idx]
            qty = fake.random_int(min=1, max=3)
            price = product_prices[pid]
            rider_id = rider_ids[i % len(rider_ids)] if rider_ids else None
            try:
                await order_service.create_order(
                    OrderCreate(
                        items=[
                            OrderItemBase(
                                product_id=pid,
                                quantity=qty,
                                price=price,
                            )
                        ],
                        rider_id=rider_id,
                    ),
                    customer_id=user_ids[user_idx],
                    db=db,
                )
                if i < len(statuses):
                    order_id = f"ORD-{i+1:05d}"
                    await order_service.update_order(
                        OrderUpdate(status=statuses[i]),
                        order_id,
                        db,
                    )
                print(f"  Created order #{i+1}")
            except Exception as e:
                await db.rollback()
                print(f"  Skipped order: {e}")

        await db.commit()
    print("\n=== Seeding complete ===")


if __name__ == "__main__":
    asyncio.run(seed_db())
