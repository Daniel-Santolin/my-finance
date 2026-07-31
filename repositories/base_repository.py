from helpers.date_helper import DateHelper

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def _basic_filter_handlers(self):
        return {
            'id': lambda query, value: query.where(self.model.id == value),
            'created_at': lambda query, value: query.where(self.model.created_at == value),
            'updated_at': lambda query, value: query.where(self.model.updated_at == value),
            'deleted_at': lambda query, value: query.where(self.model.deleted_at == value),
        }

    def _filter_handlers(self):
        return self._basic_filter_handlers()

    def apply_filters(self, query, **filters):
        handlers = self._filter_handlers()

        include_deleted = filters.pop('include_deleted', False)
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_null())

        for key, value in list(filters.items()):
            if value is None:
                continue
            handler = handlers.get(key)
            if handler is None:
                raise ValueError(f"Unsupported filter field: {key}")
            query = handler(query, value)

        return query

    def _resolve_sort(self, sort):
        if sort is None:
            return None

        sort = sort.lower()
        if not hasattr(self.model, sort):
            raise ValueError(f'Unsupported sort field: {sort}')

        return getattr(self.model, sort)

    def _resolve_direction(self, direction):
        if direction is None:
            return None

        direction = direction.lower()
        if direction not in ['asc', 'desc']:
            raise ValueError(f'Unsupported sort direction: {direction}')
        return direction

    def apply_sort(self, query, sort, direction):
        sort = self._resolve_sort(sort)
        direction = self._resolve_direction(direction)

        if sort is None or direction is None:
            return query
        if direction == 'asc':
            return query.order_by(sort.asc())
        if direction == 'desc':
            return query.order_by(sort.desc())

    def get(self, id, **filters):
        return self.apply_filters(self.model.select(), id=id, **filters).first()

    def list(self, **filters):
        sort = filters.pop('sort', 'created_at')
        direction = filters.pop('direction', 'desc')

        query = self.apply_filters(self.model.select(), **filters)
        query = self.apply_sort(query, sort, direction)
        return list(query)

    def update(self, id, **fields):
        if not fields:
            return self.get(id)

        fields['updated_at'] = DateHelper().data_atual_texto()
        self.model.update(**fields).where(self.model.id == id).execute()
        return self.get(id)

    def soft_delete(self, id):
        deleted_at = DateHelper().data_atual_texto()
        self.model.update(deleted_at=deleted_at).where(self.model.id == id).execute()
        return self.get(id, include_deleted=True)

    def restore(self, id):
        fields = {
            'deleted_at': None,
            'updated_at': DateHelper().data_atual_texto()
        }
        self.model.update(**fields).where(self.model.id == id).execute()
        return self.get(id)

    def hard_delete(self, id):
        self.model.delete().where(self.model.id == id).execute()