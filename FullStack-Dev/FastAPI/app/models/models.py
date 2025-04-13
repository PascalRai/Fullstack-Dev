"""
SQLAlchemy models for the authentication and authorization system.

This module defines the database models for users, roles, and permissions using SQLAlchemy ORM.
It implements a Role-Based Access Control (RBAC) system with many-to-many relationships
between roles and permissions.

Models:
    - User: Represents system users with role-based authorization
    - Role: Defines user roles with associated permissions
    - Permission: Represents individual permissions that can be assigned to roles
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database.database import Base

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class User(Base):
    """
    User model representing system users.

    Attributes:
        id (int): Primary key for the user
        username (str): Unique username, max length 100 characters
        hashed_password (str): Encrypted password, max length 50 characters
        role_id (int): Foreign key to roles table
        role (Role): Relationship to Role model, each user has one role
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(100)) # requires 60 for hashed password
    role_id = Column(Integer, ForeignKey('roles.id')) # Unique role for each unique user
    role = relationship("Role", back_populates="users")
    # role and not roles; as User can't have multiple roles as association table is not present
    # and its not practical for a user to have multiple roles

class Role(Base):
    """
    Role model representing user roles in the system.

    Attributes:
        id (int): Primary key for the role
        name (str): Unique role name, max length 50 characters
        users (list[User]): One-to-many relationship with User model
        permissions (list[Permission]): Many-to-many relationship with Permission model
    """
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    # relationship with Permission model; acess through roles in Permission model
    # populates to role_permission association table (allows many-to-many relationship)
    
class Permission(Base):
    """
    Permission model representing individual system permissions.

    Attributes:
        id (int): Primary key for the permission
        name (str): Unique permission name, max length 100 characters
        roles (list[Role]): Many-to-many relationship with Role model
    """
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
