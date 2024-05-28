import subprocess
import re
import telebot

bot_token = ''
chat_id = ''
pattern_login  = r'(\w{3}\s\d{1,2})\s(\d{2}:\d{2}:\d{2})\s\w+\ssshd\[\d+\]:\sAccepted\s\w+\sfor\s(\w+)\sfrom\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
pattern_logout = r'(\w{3}\s\d{1,2})\s(\d{2}:\d{2}:\d{2})\s\w+\ssshd\[\d+\]:\s.*\sfor\s(\w+)'    

def send_notification(message: str):
    bot = telebot.TeleBot(bot_token)
    bot.send_message(chat_id, message)


def main():
    log_path = "/var/log/auth.log"
    process = subprocess.Popen(['tail', '-f', log_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in process.stdout:
        if b'Accepted' in i:
            #print(i.decode())
            match_login  = re.match(pattern_login, i.decode())
            if match_login:
                date = match_login.group(1)
                time = match_login.group(2)
                user = match_login.group(3)
                ip = match_login.group(4)
                login_string = f"[{date}-{time}] sshd: {user}@{ip} is now login"
                print(login_string)
                send_notification(login_string)
        elif b'session closed' in i:
            match_logout = re.match(pattern_logout, i.decode()) 
            if match_logout:
                date = match_login.group(1)
                time = match_login.group(2)
                user = match_login.group(3)
                ip = match_login.group(4)
                logout_string = f"[{date}-{time}] sshd: {user} logout"
                print(logout_string)
                send_notification(logout_string)

if __name__ == '__main__':
    main()