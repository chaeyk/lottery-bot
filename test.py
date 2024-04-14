from dotenv import load_dotenv
load_dotenv()

import notification
import os

webhook_url = os.environ.get('CHAEYK_WEBHOOK_URL')
response = {'round': 1, 'money': 200}
notify = notification.Notification()
notify.send_lotto_winning_message(response, webhook_url)
