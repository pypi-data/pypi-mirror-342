import uuid

from bson.objectid import ObjectId
from datetime import datetime, date
from mongo_client.client import Client
from itertools import tee

db = Client().connect()


class Field:
    def __init__(self, required=False, default=None, blank=False):
        self.required = required
        self.default = default
        self.blank = blank

    def to_python(self, value):
        return value


class CharField(Field):
    def __init__(self, max_length=None, blank=False, **kwargs):
        super().__init__(**kwargs)  # Pass only the valid kwargs to Field
        self.max_length = max_length
        self.blank = blank  # Store blank information if necessary

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Expected a string")
        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"Value exceeds max length of {self.max_length}")
        return value


class IntegerField(Field):
    def __init__(self, default=None):
        super().__init__(default=default)

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, int):
            raise ValueError("Expected an integer")
        return value


class FloatField(Field):
    def __init__(self, default=None, required=False):
        super().__init__(required, default)

    def to_python(self, value):
        if self.required and value is None:
            raise ValueError("This field is required")
        if value is None:
            return None
        if not isinstance(value, float):
            raise ValueError("Expected an float")
        return value


class BooleanField(Field):
    def __init__(self, default=None, required=False):
        super().__init__(required, default)

    def to_python(self, value):
        if self.required and value is None:
            raise ValueError("This field is required")
        if value is None:
            return None
        if not isinstance(value, bool):
            raise ValueError("Expected an boolean")
        return value


class ListField(Field):
    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValueError("Expected an list")
        return value


class JSONField(Field):
    def to_python(self, value):
        if value is None:
            return None
        if type(value) not in [list, dict]:
            raise ValueError("Expected an list or dict")
        return value


class UUIDField(Field):
    def __init__(self, default=None, required=False):
        super().__init__(required, default)

    def to_python(self, value):
        if self.required and value is None:
            raise ValueError("This field is required")
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            raise ValueError("Expected an UUID")
        return value


class DateField(Field):
    def __init__(self, default=None, required=False):
        super().__init__(required, default)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                # Try to parse a date string into a date object
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Expected a valid date string in 'YYYY-MM-DD' format")
        if not isinstance(value, date):
            raise ValueError("Expected a date object or a valid date string")
        return value


class DateTimeField(Field):
    def __init__(self, auto_now=False, auto_now_add=False, **kwargs):
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

    def to_python(self, value):
        if self.auto_now:
            return datetime.now()
        if self.auto_now_add and value is None:
            return datetime.now()
        if value is None:
            return None

        if isinstance(value, str):
            try:
                # Try to parse a datetime string into a datetime object
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(
                    "Expected a valid datetime string in 'YYYY-MM-DD HH:MM:SS' format"
                )
        if not isinstance(value, datetime):
            raise ValueError("Expected a datetime object or a valid datetime string")
        return value


class QuerySet:
    """A wrapper for query results, allowing for further operations like `.first()`. """

    def __init__(
        self, model_class, documents_cursor, filter_criteria=None, sort_criteria=None, query=None, collection=None
    ):
        self.model_class = model_class
        self.documents_cursor = documents_cursor  # Cursor from the MongoDB query
        self.filter_criteria = filter_criteria or {}
        self.sort_criteria = sort_criteria or []
        self.query = query
        self.collection = collection

    def __iter__(self):
        """Allow the QuerySet to be iterable."""
        """Make the QuerySet iterable."""
        try:
            docs = [self.model_class(**doc) for doc in self.documents_cursor]
            return iter(docs)
        except Exception as e:
            return iter([])

    def first(self):
        """Return the first document if available."""
        first_document = next(self.documents_cursor, None)
        if first_document:
            return self.model_class(**first_document)
        return None
    
    def last(self):
        """Return the last document if available."""
        last_document = None
        for doc in self.documents_cursor:
            last_document = doc
        if last_document:
            return self.model_class(**last_document)
        return None
    
    def copy_queryset(self):
        """Return a copy of the current QuerySet."""
        cloned_cursor, cursor_copy = tee(self.documents_cursor)
        return QuerySet(
            self.model_class,
            cloned_cursor,
            filter_criteria=self.filter_criteria,
            sort_criteria=self.sort_criteria,
        ), QuerySet(
            self.model_class,
            cursor_copy,
            filter_criteria=self.filter_criteria,
            sort_criteria=self.sort_criteria,
        )

    def exclude(self, **kwargs):
        """Exclude documents matching the given kwargs."""
        excluded_docs = [
            doc
            for doc in self.documents_cursor
            if not all(item in doc.items() for item in kwargs.items())
        ]
        return [self.model_class(**doc) for doc in excluded_docs]

    def count(self):
        """Count the number of documents in the QuerySet."""
        # Use count_documents with the filter criteria if available
        if self.filter_criteria:
            return self.documents_cursor.collection.count_documents(
                self.filter_criteria
            )
        # Fallback to counting the cursor length if filter criteria are not stored
        return len(list(self.documents_cursor))
    
    def __len__(self):
        return self.count()

    def delete(self):
        """Delete all documents in the QuerySet."""
        for doc in self.documents_cursor:
            self.model_class(**doc).delete()

    def order_by(self, *fields):
        """
        Order the QuerySet by the specified fields.
        Use '-' prefix for descending order and no prefix for ascending.
        """
        # Create sort criteria from the fields
        sort_criteria = []
        for field in fields:
            if field.startswith("-"):
                sort_criteria.append((field[1:], -1))  # Descending
            else:
                sort_criteria.append((field, 1))  # Ascending

        # Determine the collection to use
        if not hasattr(self, 'collection') or self.collection is None:
            # If we don't have a collection directly, try to get it from the cursor
            if hasattr(self.documents_cursor, 'collection'):
                collection = self.documents_cursor.collection
            else:
                # Try to get collection from model_class
                try:
                    collection = db[self.model_class.Meta.collection_name]
                except (AttributeError, KeyError):
                    raise ValueError("Cannot order results: no collection available")
        else:
            collection = self.collection

        # Create a new query with the same filter criteria and apply sorting
        # This avoids the issue with consumable cursors
        sorted_cursor = collection.find(self.filter_criteria).sort(sort_criteria)
        
        # Return a new QuerySet with the sorted cursor
        return QuerySet(
            self.model_class,
            sorted_cursor,
            filter_criteria=self.filter_criteria,
            sort_criteria=sort_criteria,
            query=self.filter_criteria,
            collection=collection
        )
        
    def values_list(self, *fields, flat=False):
        """
        Return a list of tuples containing the values for the specified fields.
        If flat=True and only one field is provided, return a flat list of values.
        
        Example:
            # Returns [(1, 'name1'), (2, 'name2'), ...]
            Model.objects.filter(...).values_list('id', 'name')
            
            # Returns [1, 2, ...] with flat=True
            Model.objects.filter(...).values_list('id', flat=True)
        """
        if not fields:
            raise ValueError("values_list() requires at least one field name")
            
        if flat and len(fields) > 1:
            raise ValueError("'flat' is not valid when values_list is called with more than one field")
        
        result = []
        
        # Handle consumable cursor issue by creating a fresh query if possible
        if hasattr(self, 'collection') and self.collection is not None and hasattr(self, 'filter_criteria'):
            # Create a fresh cursor with the same filter criteria
            cursor = self.collection.find(self.filter_criteria)
            
            # Apply any sort criteria if available
            if hasattr(self, 'sort_criteria') and self.sort_criteria:
                cursor = cursor.sort(self.sort_criteria)
        else:
            # If we can't create a fresh cursor, use the existing one
            # Note: This might be empty if the cursor has already been consumed
            cursor = self.documents_cursor
            
        # Process the cursor to extract the requested fields
        for doc in cursor:
            if flat:
                # With flat=True, return a flat list of single values
                field = fields[0]
                result.append(doc.get(field))
            else:
                # Return a list of tuples with values for each field
                values = tuple(doc.get(field) for field in fields)
                result.append(values)
                
        return result
        


class MongoManager:
    def __init__(self, model_class):
        self.model_class = model_class
        self.collection = db[model_class.Meta.collection_name]

    def all(self):
        """Fetch all documents from the collection."""
        documents_cursor = self.collection.find()
        return QuerySet(self.model_class, documents_cursor)

    def filter(self, **kwargs):
        """
        Filter documents by the given kwargs, supporting `__in` for fields.
        """
        mongo_query = {}

        for key, value in kwargs.items():
            if "__" in key:
                field_name, lookup = key.split("__", 1)

                if lookup == "in":
                    if field_name == "_id" or field_name.endswith("_id"):
                        value = [ObjectId(v) for v in value]
                    mongo_query[field_name] = {"$in": value}

                elif lookup == "contains":
                    if not isinstance(value, str):
                        raise ValueError(
                            "The `contains` filter expects a string value."
                        )
                    mongo_query[field_name] = {"$regex": f"{value}"}

                elif lookup == "icontains":
                    if not isinstance(value, str):
                        raise ValueError(
                            "The `icontains` filter expects a string value."
                        )
                    # Case-insensitive matching using $regex and $options: "i"
                    mongo_query[field_name] = {"$regex": f"{value}", "$options": "i"}

                else:
                    raise ValueError(f"Unsupported lookup: {lookup}")
            else:
                if key == "_id" or key.endswith("_id"):
                    value = ObjectId(value)
                mongo_query[key] = value

        # Query MongoDB with the converted query
        try:
            return QuerySet(
                self.model_class,
                self.collection.find(mongo_query),
                filter_criteria=kwargs,
                query=mongo_query,
                collection=self.collection
            )
        except Exception as e:
            print("Error Executing Query:", str(e))
            return QuerySet(self.model_class, [], filter_criteria=kwargs)

    def exclude(self, **kwargs):
        """Exclude documents by the given kwargs."""
        documents_cursor = self.collection.find()
        return QuerySet(
            self.model_class,
            [
                doc
                for doc in documents_cursor
                if not all(item in doc.items() for item in kwargs.items())
            ],
        )

    def get(self, **kwargs):
        """Get a single document matching the kwargs."""
        document = self.collection.find_one(kwargs)
        if document:
            return self.model_class(**document)
        raise ValueError(f"No {self.model_class.Meta.collection_name} instance found matching: {kwargs}")

    def create(self, **kwargs):
        """Create a new document in the collection."""
        current_time = datetime.now()
        document = {}
        fields = self.model_class._get_fields()
        for key, field in fields.items():
            value = kwargs.get(key, field.default)

            # Handle auto_now_add fields
            if isinstance(field, DateTimeField):
                if field.auto_now_add:
                    value = current_time
                if field.auto_now:
                    value = current_time

            # Handle required fields
            if value is None and field.required:
                raise ValueError(f"Field '{key}' is required.")

            document[key] = value
        result = self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return self.model_class(**document)


class MongoModel:
    objects = None

    def __init__(self, **kwargs):
        self._id = kwargs.get("_id")
        for key, value in self._get_fields().items():
            field_value = kwargs.get(key, value.default)
            setattr(self, key, field_value)

    def save(self):
        current_time = datetime.now()
        data = {}
        for key, field in self._get_fields().items():
            value = getattr(self, key)

            if isinstance(field, DateTimeField):
                # Handle auto_now
                if field.auto_now:
                    value = current_time
                    setattr(self, key, value)
            if isinstance(field, DateTimeField):
                if field.auto_now_add and self._id is None:
                    value = current_time
                    setattr(self, key, value)

            # Prepare data for saving
            data[key] = value

        if self._id:
            self.objects.collection.update_one(
                {"_id": ObjectId(self._id)}, {"$set": data}
            )
        else:
            result = self.objects.collection.insert_one(data)
            self._id = result.inserted_id

    def delete(self):
        if self._id:
            self.objects.collection.delete_one({"_id": ObjectId(self._id)})
        else:
            raise ValueError("Cannot delete an unsaved object.")

    @classmethod
    def _initialize_manager(cls):
        """Initialize the `objects` attribute with a MongoManager."""
        cls.objects = MongoManager(cls)

    @classmethod
    def _get_fields(cls):
        """Get all fields defined in the class."""
        return {
            key: value
            for key, value in cls.__dict__.items()
            if isinstance(value, Field)
        }
