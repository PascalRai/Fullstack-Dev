from sqlalchemy.orm import Session

from app.models.models import Role, Permission
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

    # admin add, update, delete any products, review, browse products, list of products order of both customer and seller, update order status, and other all permissions
    permissions = {
        "admin": [
        ],
        "seller": [
        ],
        "customer": [
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

    db.close()

if __name__ == "__main__":
    seed()
