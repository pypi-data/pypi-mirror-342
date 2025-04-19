# -*- coding=utf-8 -*-
import decimal
from .wechatpay import WechatPay
import json

import requests

class Wxpay:
    """
    创建微信支付对象
    """


    def __init__(self, app=None):
        self.model = None
        self.notify_url = None
        self.config = None
        if  app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.config = app.config['WXPAY']
        self.model = WechatPay(self.config)
        #
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions['wxpay'] = self


    def pay_order(self, order):

        params = {
            'appid': self.config['APP_ID'],
            'mchid': self.config['MCH_ID'],
            'description'            : order.subject,
            'out_trade_no'    : order.order_no,
            'amount'       : {"total": int(decimal.Decimal(order.total_price)*100),
                              'currency': 'CNY'},
            'notify_url' : self.config['WXPAY_NOTIFY_URL']
        }
        return self.model.place_order(params)

    def confirm_pay(self, request):
        signature = request.headers.get('Wechatpay-Signature')
        timestamp = request.headers.get('Wechatpay-Timestamp')
        nonce = request.headers.get('Wechatpay-Nonce')
        serial_no = request.headers.get('Wechatpay-Serial')
        data = request.data
        res, order_data = self.model.pay_notify(signature, timestamp, nonce, serial_no, data)
        data = {'out_trade_no': order_data['out_trade_no'],
                'total_price': order_data['amount']['payer_total']/100}
        if res:
            message = {"code": "SUCCESS", "message": ""}
        else:
            message = {"code": "FAIL", "message": "验签失败"}
        return res, data, json.dumps(message)




