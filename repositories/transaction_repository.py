from base_repository import BaseRepository
from helpers.date_helper import DateHelper
from models.transaction import Transaction


class TransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Transaction)

    def _filter_handlers(self):
        handler = super()._filter_handlers()
        handler.update({
            'account_id': lambda query, value: query.where(self.model.account_id == value),
            'transaction_category_id': lambda query, value: query.where(self.model.transaction_category_id == value),
            'transaction_type': lambda query, value: query.where(self.model.type == value),
            'status': lambda query, value: query.where(self.model.status == value),
            'date': lambda query, value: query.where(self.model.date == value),
        })
        return handler

    def create(
        self,
        account,
        transaction_category=None,
        transaction_type='',
        date='',
        name='',
        alias=None,
        value=0,
        status=''
    ):
        return self.model.create(
            account=account,
            transaction_category=transaction_category,
            transaction_type=transaction_type,
            date=date,
            name=name,
            alias=alias,
            value=value,
            status=status
        )
