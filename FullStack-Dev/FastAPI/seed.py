from sqlalchemy.orm import Session

from app.database.init_db import init_database
from app.models.models import Role, Permission, User
from app.database.database import SessionLocal

def create_if_not_exists(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
    return instance

def seed():
    db: Session = SessionLocal()

    # Default roles and permissions
    roles = ["admin", "seller", "customer"] # Only 3 users role initially set

    # seller can add, update and delete own products, delete own product reviews, browse other products
    # see order list of own product, update status of order

    # customer can browse other products, place order, status of order, order list, cancel order, review product

    # admin add, update, delete any products, review, browse products, list of products order of both customer and seller, 
    # update order status, and other all permissions (delete any user and change roles)
    permissions = permissions = {
        "admin": [
            "browse_products",
            "add_product",
            "update_any_product",
            "delete_any_product",
            "delete_any_review",
            "view_all_orders",
            "update_order_status",
            "view_users",
            "delete_user"
            "assign_roles"
        ],
        "seller": [
            "browse_products",
            "add_product",
            "update_own_product",
            "delete_own_product",
            "delete_review_on_own_product",
            "view_orders_on_own_products",
            "update_order_status"
        ],
        "customer": [
            "browse_products",
            "place_order",
            "cancel_order",
            "view_own_orders",
            "track_order_status",
            "review_product",
            "delete_own_review"
        ]
    }


    # Create roles
    for role_name in roles:
        role = create_if_not_exists(db, Role, name=role_name)

        # Assign permissions to role
        for perm_name in permissions[role_name]:
            perm = create_if_not_exists(db, Permission, name=perm_name)
            if perm not in role.permissions:
                role.permissions.append(perm)

        db.commit()
    
    # Create default admin user
    admin_role = db.query(Role).filter_by(name="admin").first()
    existing_admin = db.query(User).filter_by(username="pascal").first()

    if not existing_admin:
        hashed_password = '$2b$12$nE8PK/1chkfpDrFYGTuMNOOPicOAqFsD5qvNYrDUf6VaRqOl2oF6q' # hased password
        admin_user = User(
            username="pascal",
            hashed_password=hashed_password,
            role=admin_role
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Admin user 'pascal' created.")
    else:
        print("Admin user 'pascal' already exists.")
    db.close()

if __name__ == "__main__":
    init_database() # alembic requires to have table first to migrate
    seed() # once migration is completed, we dont require to initialize tables again!
