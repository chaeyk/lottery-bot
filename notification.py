import requests
import os
                    
class Notification: 

    def send_lotto_buying_message(self, body: dict) -> None:
        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":  
            return

        lotto_number_str = self.make_lotto_number_message(result["arrGameChoiceNum"])
        message = f"{result['buyRound']}회 로또 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{lotto_number_str}```"
        self.send_message(message)

    def make_lotto_number_message(self, lotto_number: list) -> str:
        assert type(lotto_number) == list

        # parse list without last number 3
        lotto_number = [x[:-1] for x in lotto_number]
        
        # remove alphabet and | replace white space  from lotto_number
        lotto_number = [x.replace("|", " ") for x in lotto_number]
        
        # lotto_number to string 
        lotto_number = '\n'.join(x for x in lotto_number)
        
        return lotto_number

    def send_win720_buying_message(self, body: dict) -> None:
        if body.get("resultCode") != '100':  
            return       

        win720_round = body.get("resultMsg").split("|")[3]

        win720_number_str = self.make_win720_number_message(body.get("saleTicket"))
        message = f"{win720_round}회 연금복권 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{win720_number_str}```"
        self.send_message(message)

    def make_win720_number_message(self, win720_number: str) -> str:
        return "\n".join(win720_number.split(","))

    def send_lotto_winning_message(self, winning: dict) -> None: 
        assert type(winning) == dict

        if winning["win"]:
            round = winning["round"]
            money = winning["money"]
            message = f"로또 *{round}회* - *{money}* 당첨 되었습니다 :tada:"
            self.send_message(message)
        else:
            self.send_message("로또 꽝")

    def send_win720_winning_message(self, winning: dict) -> None: 
        assert type(winning) == dict

        if winning["win"]:
            round = winning["round"]
            money = winning["money"]
            message = f"연금복권 *{round}회* - *{money}* 당첨 되었습니다 :tada:"
            self.send_message(message)
        else:
            self.send_message("연금복권 꽝")

    def send_message(self, message: str) -> None:
        self._send_chaeyk_webhook(message)

    def _send_discord_webhook(self, message: str) -> None:        
        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        payload = { "content": message }
        requests.post(webhook_url, json=payload)

    def _send_chaeyk_webhook(self, message: str) -> None:
        webhook_url = os.environ.get('CHAEYK_WEBHOOK_URL')
        payload = { "message": message }
        print(f'sending message: {payload}')
        requests.post(webhook_url, json=payload)
