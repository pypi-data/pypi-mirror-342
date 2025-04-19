# -*- coding=utf-8 -*-
from flask import current_app
from xp_cms.services.base_service import XPService, db
from xp_cms.models.account import Account, AccountLogs, \
    RechargeRecord, BuyRecord

'''根据用户名查询余额'''


class AccountService(XPService):
    model = Account
    account_logs_model = AccountLogs
    recharge_record_model = RechargeRecord
    BuyRecord_model = BuyRecord

    @classmethod
    def add_balance(cls, user_id, amount, type, event, detail):
        try:
            user_account = cls.get_one_by_field(("user_id", user_id))
            setattr(user_account, type, getattr(user_account, type) + amount)
            # 记录账户变化
            change_data = {"account_type": type,
                           "event_type"  : event,
                           "amount"      : amount,
                           "detail"      : detail,
                           "user_id"     : user_id
                           }
            log_obj = cls.log_change(change_data)
            db.session.add(log_obj)
            db.session.add(user_account)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            return user_account

    @classmethod
    def log_change(cls, change_data):
        """change_data = {"account_type": type,
                  "event_type": event,
                  "amount": amount,
                  "detail": detail,
                  "user_id": user_id
                  }
        """
        account_log = cls.account_logs_model(**change_data)
        return account_log

    @classmethod
    def get_account_log(cls, user_id, page, page_size, type=None):
        condition = [{"field": "user_id", "value": user_id, "operator": "eq"}]
        logs = cls.get_many(condition,
                            page,
                            page_size)
        return logs

    @classmethod
    def get_account(cls, user_id):
        account = cls.get_one_by_field(("user_id", user_id))
        return account
