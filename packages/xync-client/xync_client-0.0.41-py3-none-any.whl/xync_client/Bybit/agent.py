from asyncio import run
from enum import IntEnum
from time import sleep

import pyotp
from bybit_p2p import P2P
from x_model import init_db
from xync_schema import models

from xync_client.Abc.Base import FlatDict
from xync_schema.models import Cur, Actor

from xync_client.Abc.Agent import BaseAgentClient
from xync_client.Abc.types import BaseOrderReq
from xync_client.Bybit.etype.ad import AdPostRequest, AdUpdateRequest, AdDeleteRequest
from xync_client.Bybit.etype.order import OrderRequest, PreOrderResp, OrderResp, CancelOrderReq
from xync_client.loader import PG_DSN


class NoMakerException(Exception):
    pass


class AdsStatus(IntEnum):
    REST = 0
    WORKING = 1


class AgentClient(BaseAgentClient):  # Bybit client
    host = "api2.bybit.com"
    headers = {"cookie": ";"}  # rewrite token for public methods
    api: P2P
    last_ad_id: list[str] = []
    update_ad_body = {
        "priceType": "1",
        "premium": "118",
        "quantity": "0.01",
        "minAmount": "500",
        "maxAmount": "3500000",
        "paymentPeriod": "30",
        "remark": "",
        "price": "398244.84",
        "paymentIds": ["3162931"],
        "tradingPreferenceSet": {
            "isKyc": "1",
            "hasCompleteRateDay30": "0",
            "completeRateDay30": "",
            "hasOrderFinishNumberDay30": "0",
            "orderFinishNumberDay30": "0",
            "isMobile": "0",
            "isEmail": "0",
            "hasUnPostAd": "0",
            "hasRegisterTime": "0",
            "registerTimeThreshold": "0",
            "hasNationalLimit": "0",
            "nationalLimit": "",
        },
        "actionType": "MODIFY",
        "securityRiskToken": "",
    }

    def __init__(self, actor: Actor, **kwargs):
        super().__init__(actor, **kwargs)
        self.api = P2P(testnet=False, api_key=actor.agent.auth["key"], api_secret=actor.agent.auth["sec"])

    """ Private METHs"""

    def fiat_new(self, payment_type: int, real_name: str, account_number: str) -> FlatDict:
        method1 = self._post(
            "/fiat/otc/user/payment/new_create",
            {"paymentType": payment_type, "realName": real_name, "accountNo": account_number, "securityRiskToken": ""},
        )
        if srt := method1["result"]["securityRiskToken"]:
            self._check_2fa(srt)
            method2 = self._post(
                "/fiat/otc/user/payment/new_create",
                {
                    "paymentType": payment_type,
                    "realName": real_name,
                    "accountNo": account_number,
                    "securityRiskToken": srt,
                },
            )
            return method2
        else:
            print(method1)

    def get_payment_method(self, fiat_id: int = None) -> dict:
        list_methods = self.get_user_pay_methods()
        if fiat_id:
            fiat = [m for m in list_methods if m["id"] == fiat_id][0]
            return fiat
        return list_methods[1]

    def creds(self):
        data = self.api.get_user_payment_types()
        return data["result"] if data["ret_code"] == 0 else data

    async def ott(self):
        t = await self._post("/user/private/ott")
        return t

    # 27
    async def fiat_upd(self, fiat_id: int, detail: str, name: str = None) -> dict:
        fiat = self.get_payment_method(fiat_id)
        fiat["realName"] = name
        fiat["accountNo"] = detail
        result = await self._post("/fiat/otc/user/payment/new_update", fiat)
        srt = result["result"]["securityRiskToken"]
        await self._check_2fa(srt)
        fiat["securityRiskToken"] = srt
        result2 = await self._post("/fiat/otc/user/payment/new_update", fiat)
        return result2

    # 28
    async def fiat_del(self, fiat_id: int) -> dict | str:
        data = {"id": fiat_id, "securityRiskToken": ""}
        method = await self._post("/fiat/otc/user/payment/new_delete", data)
        srt = method["result"]["securityRiskToken"]
        await self._check_2fa(srt)
        data["securityRiskToken"] = srt
        delete = await self._post("/fiat/otc/user/payment/new_delete", data)
        return delete

    async def switch_ads(self, new_status: AdsStatus) -> dict:
        data = {"workStatus": new_status.name}
        res = await self._post("/fiat/otc/maker/work-config/switch", data)
        return res

    def online_ads(self) -> str:
        online = self._get("/fiat/otc/maker/work-config/get")
        return online["result"]["workStatus"]

    @staticmethod
    def get_rate(list_ads: list) -> float:
        ads = [ad for ad in list_ads if set(ad["payments"]) - {"5", "51"}]
        return float(ads[0]["price"])

    async def my_fiats(self, cur: Cur = None):
        upm = await self._post("/fiat/otc/user/payment/list")
        return upm["result"]

    def get_user_ads(self, active: bool = True) -> list:
        uo = self._post("/fiat/otc/item/personal/list", {"page": "1", "size": "10", "status": "2" if active else "0"})
        return uo["result"]["items"]

    def get_security_token_create(self):
        data = self._post("/fiat/otc/item/create", self.create_ad_body)
        if data["ret_code"] == 912120019:  # Current user can not to create add as maker
            raise NoMakerException(data)
        security_risk_token = data["result"]["securityRiskToken"]
        return security_risk_token

    def _check_2fa(self, risk_token):
        # 2fa code
        bybit_secret = self.agent.auth["2fa"]
        totp = pyotp.TOTP(bybit_secret)
        totp_code = totp.now()

        res = self._post(
            "/user/public/risk/verify", {"risk_token": risk_token, "component_list": {"google2fa": totp_code}}
        )
        if res["ret_msg"] != "success":
            print("Wrong 2fa, wait 5 secs and retry..")
            sleep(5)
            self._check_2fa(risk_token)
        return res

    def _post_ad(self, risk_token: str):
        self.create_ad_body.update({"securityRiskToken": risk_token})
        data = self._post("/fiat/otc/item/create", self.create_ad_body)
        return data

    # создание объявлений
    def post_create_ad(self, token: str):
        result__check_2fa = self._check_2fa(token)
        assert result__check_2fa["ret_msg"] == "success", "2FA code wrong"

        result_add_ad = self._post_ad(token)
        if result_add_ad["ret_msg"] != "SUCCESS":
            print("Wrong 2fa on Ad creating, wait 9 secs and retry..")
            sleep(9)
            return self._post_create_ad(token)
        self.last_ad_id.append(result_add_ad["result"]["itemId"])

    def ad_new(self, ad: AdPostRequest):
        data = self.api.post_new_ad(**ad.model_dump())
        return data["result"]["itemId"] if data["ret_code"] == 0 else data

    def ad_upd(self, upd: AdUpdateRequest):
        data = self.api.update_ad(**upd.model_dump())
        return data["result"] if data["ret_code"] == 0 else data

    def get_security_token_update(self) -> str:
        self.update_ad_body["id"] = self.last_ad_id
        data = self._post("/fiat/otc/item/update", self.update_ad_body)
        security_risk_token = data["result"]["securityRiskToken"]
        return security_risk_token

    def post_update_ad(self, token):
        result__check_2fa = self._check_2fa(token)
        assert result__check_2fa["ret_msg"] == "success", "2FA code wrong"

        result_update_ad = self.update_ad(token)
        if result_update_ad["ret_msg"] != "SUCCESS":
            print("Wrong 2fa on Ad updating, wait 10 secs and retry..")
            sleep(10)
            return self._post_update_ad(token)
        # assert result_update_ad['ret_msg'] == 'SUCCESS', "Ad isn't updated"

    def update_ad(self, risk_token: str):
        self.update_ad_body.update({"securityRiskToken": risk_token})
        data = self._post("/fiat/otc/item/update", self.update_ad_body)
        return data

    def ad_del(self, ad_id: AdDeleteRequest):
        data = self.api.remove_ad(**ad_id.model_dump())
        return data

    async def order_request(self, br: BaseOrderReq) -> OrderResp:
        res0 = await self._post("/fiat/otc/item/simple", data={"item_id": str(br.ad_id)})
        if res0["ret_code"] == 0:
            res0 = res0["result"]
        res0 = PreOrderResp.model_validate(res0)
        req = OrderRequest(
            itemId=br.ad_id,
            tokenId=br.coin_exid,
            currencyId=br.cur_exid,
            side=str(OrderRequest.Side(int(br.is_sell))),
            amount=str(br.fiat_amount or br.asset_amount * float(res0.price)),
            curPrice=res0.curPrice,
            quantity=str(br.asset_amount or round(br.fiat_amount / float(res0.price), br.coin_scale)),
            flag="amount" if br.amount_is_fiat else "quantity",
        )
        # вот непосредственно сам запрос на ордер
        res = await self._post("/fiat/otc/order/create", data=req.model_dump())
        if res["ret_code"] == 0:
            return OrderResp.model_validate(res["result"])
        elif res["ret_code"] == 912120030 or res["ret_msg"] == "The price has changed, please try again later.":
            return await self.order_request(br)

    async def cancel_order(self, order_id: str) -> bool:
        cr = CancelOrderReq(orderId=order_id)
        res = await self._post("/fiat/otc/order/cancel", cr.model_dump())
        return res["ret_code"] == 0

    def get_order_info(self, order_id: str) -> dict:
        data = self._post("/fiat/otc/order/info", json={"orderId": order_id})
        return data["result"]

    def get_chat_msg(self, order_id):
        data = self._post("/fiat/otc/order/message/listpage", json={"orderId": order_id, "size": 100})
        msgs = [
            {"text": msg["message"], "type": msg["contentType"], "role": msg["roleType"], "user_id": msg["userId"]}
            for msg in data["result"]["result"]
            if msg["roleType"] not in ("sys", "alarm")
        ]
        return msgs

    def block_user(self, user_id: str):
        return self._post("/fiat/p2p/user/add_block_user", {"blockedUserId": user_id})

    def unblock_user(self, user_id: str):
        return self._post("/fiat/p2p/user/delete_block_user", {"blockedUserId": user_id})

    def user_review_post(self, order_id: str):
        return self._post(
            "/fiat/otc/order/appraise/modify",
            {
                "orderId": order_id,
                "anonymous": "0",
                "appraiseType": "1",  # тип оценки 1 - хорошо, 0 - плохо. При 0 - обязательно указывать appraiseContent
                "appraiseContent": "",
                "operateType": "ADD",  # при повторном отправлять не 'ADD' -> а 'EDIT'
            },
        )

    def get_orders_active(self, begin_time: int, end_time: int, status: int, side: int, token_id: str):
        return self._post(
            "/fiat/otc/order/pending/simplifyList",
            {
                "status": status,
                "tokenId": token_id,
                "beginTime": begin_time,
                "endTime": end_time,
                "side": side,  # 1 - продажа, 0 - покупка
                "page": 1,
                "size": 10,
            },
        )

    def get_orders_done(self, begin_time: int, end_time: int, status: int, side: int, token_id: str):
        return self._post(
            "/fiat/otc/order/simplifyList",
            {
                "status": status,  # 50 - завершено
                "tokenId": token_id,
                "beginTime": begin_time,
                "endTime": end_time,
                "side": side,  # 1 - продажа, 0 - покупка
                "page": 1,
                "size": 10,
            },
        )


def listen(data: dict):
    print(data)


async def main():
    _ = await init_db(PG_DSN, models, True)
    actor = await models.Actor.filter(ex_id=9, agent__isnull=False).prefetch_related("ex", "agent").first()
    cl: AgentClient = actor.client()
    coin = await models.Coin.get(ticker="USDT")
    bor = BaseOrderReq(
        ad_id="1861440060199632896",
        # asset_amount=40,
        fiat_amount=3000,
        amount_is_fiat=True,
        is_sell=False,
        cur_exid="RUB",
        coin_exid=coin.ticker,
        coin_scale=coin.scale,
    )
    res: OrderResp = await cl.order_request(bor)
    cl.cancel_order(res.orderId)
    await cl.close()


if __name__ == "__main__":
    run(main())
