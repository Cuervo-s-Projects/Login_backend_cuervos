from datetime import datetime
from bson import ObjectId

class User:
    def __init__(
        self,
        username: str = '',
        email: str = '',
        password: str = '',
        last_name: str = '',
        first_name: str = '',
        age: str = '',
        date_birth: datetime = None, 
        is_active: bool = True,
        is_verified: bool = False,
        roles: list = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        metadata: dict = None,
        _id: ObjectId = None,
    ):
        self._id = _id or ObjectId()
        self.username = username.strip()
        self.email = email.lower().strip()
        self.password = password

        self.last_name = last_name
        self.first_name = first_name 

        self.age = age if age is not None else None
        self.date_birth = date_birth if date_birth is not None else None

        self.is_active = is_active
        self.is_verified = is_verified
        self.roles = roles if roles is not None else ['student']

        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.metadata = metadata if metadata is not None else {'last_login': None}

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'age': self.age,
            'date_birth': self.date_birth,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'roles': self.roles,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data.get('_id', None),
            username=data.get('username', '').strip(),
            email=data.get('email', '').lower().strip(),
            password=data.get('password', ''),
            last_name=data.get('last_name', ''),
            first_name=data.get('first_name', ''),
            age=data.get('date_birth', ''),
            date_birth=data.get('date_birth', ''),
            is_active=bool(data['is_active']) if 'is_active' in data else False,
            is_verified= bool(data['is_verified']) if 'is_verified' in data else False,
            roles=data.get('roles', ['user']),
            created_at=data.get('created_at', None),
            updated_at=data.get('updated_at', None),
            metadata=data.get('metadata', {'last_login': None})
        )

    def validate(self):
        errors = []
        if not self.username:
            errors.append("Username is required")
        if not self.email:
            errors.append("Email is required")
        if not self.password:
            errors.append("Password is required")
        return errors

    @property
    def is_authenticated(self):
        return True