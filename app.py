import subprocess
import re
import telebot
from datetime import datetime

bot_token = ''
chat_id = ''
pattern_login  = r'(\w{3}\s\d{1,2})\s(\d{2}:\d{2}:\d{2})\s\w+\ssshd\[\d+\]:\sAccepted\s\w+\sfor\s(\w+)\sfrom\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
pattern_logout = r'(\w{3}\s\d{1,2})\s(\d{2}:\d{2}:\d{2})\s\w+\ssshd\[\d+\]:\s.*\sfor\s(\w+)'    
pattern_session = r"(\w+ \d{2}) (\d{2}:\d{2}:\d{2}) .+ (systemd-logind\[\d+\]): (.+)"

def time_elapsed(start: str, stop: str):
    time_format = "%H:%M:%S"
    print(f'{start}, {stop}')
    start_time = datetime.strptime(start, time_format)
    end_time = datetime.strptime(stop, time_format)
    time_difference = end_time - start_time
    minutes_difference = time_difference.total_seconds() / 60
    hours = minutes_difference // 60
    minutes = minutes_difference % 60
    return f'Waktu Login: {int(hours)} jam {int(minutes)} menit'

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
                login_string = f"[{date}-{time}] Dinpokan: {user}@{ip} is now login"
                print(login_string)
                send_notification(login_string)
                
        elif b'New session' in i:
            match_session = re.match(pattern_session, i.decode())
            if match_session:
                date = match_session.group(1)
                time_start = match_session.group(2)
                service = match_session.group(3)
                message = match_session.group(4)
                session_string = f"[{date}-{time_start}]{service}: {message}"
                print(time)
                print(session_string)
        elif b'session closed' in i:
            match_logout = re.match(pattern_logout, i.decode())
            if match_logout:
                date = match_logout.group(1)
                time_end = match_logout.group(2)
                user = match_logout.group(3)
                logout_string = f"[{date}-{time_end}] Diinpokan: {user} logout. {time_elapsed(time_start, time_end)}"
                print(logout_string)
                send_notification(logout_string)

if __name__ == '__main__':
    main()
