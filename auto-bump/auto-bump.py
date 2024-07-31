import requests
import os
import random
import json
import time
import logging
import colorama
from colorama import *

init()

def title(string):
    os.system("title " + str(string))

title("Auto Bump - Made By Damix")

def cprint(color=None, sign=None, msg=None, width=None):
    if msg is not None:
        if color is not None:
            color = color.lower()
            if color == "red":
                print("["+ Fore.RED + sign + Fore.RESET + "]", msg)
            elif color == "yellow":
                print("["+ Fore.YELLOW + sign + Fore.RESET + "]", msg)
            elif color == "green":
                print("["+ Fore.GREEN + sign + Fore.RESET + "]", msg)
        else:
            if width is not None:
                print(msg.center(int(width)))
            else:
                print(msg)
    else:
        print()

user_agents = []

py_dir = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename=str(os.path.join(py_dir, "logs", "run-time.log")), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(str(os.path.join(py_dir, "logs", "run-time.log")))

config = os.path.join(py_dir, "config")
guild_id = os.path.join(config, "guildID", "guild_ID.json")
discordservers_com = os.path.join(config, "discordservers_com", "cookies.json")

user_agents_file = os.path.join(py_dir, "user_agents", "user_agents.txt")

if not os.path.exists(user_agents_file):
    os.makedirs("user_agents")
    open(user_agents_file, "w", encoding="utf-8").close()
    response = requests.get("https://raw.githubusercontent.com/Damix-hash/roblox-stuff/main/user-agents")
    if response.ok:
        user_agents = response.text.strip().split("\n")
        with open(user_agents_file, "a", encoding="utf-8") as user_agent_list:
            for user_agent in user_agents:
                user_agent_list.write(user_agent + "\n")
else:
    with open(user_agents_file, "r", encoding="utf-8") as user_agent_list:
        user_agents = user_agent_list.read().strip().split("\n")

def get_user_agent():
    return random.choice(user_agents)

def seconds_to_time(n):
    seconds = n
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    
    if minutes < 10:
        minutes = "0" + str(minutes)
    
    if seconds < 10:
        seconds = "0" + str(seconds)

    return str(hours) + ":" + str(minutes) + ":" + str(seconds)

def live_timer(n):
    n = int(n)
    while n > 0:
        print("["+ Fore.YELLOW + '>' + Fore.RESET + "]", f"Sleeping For: {seconds_to_time(n)}", end="\r")
        time.sleep(1)
        n -= 1

def beautify_amount(n):
    number_indicator = ''
    if n != 0:
        if n == 1:
            number_indicator = "st"
        elif n == 2:
            number_indicator = "nd"
        elif n == 3:
            number_indicator = "rd"
        else:
            number_indicator = "th"

    return str(n) + str(number_indicator)

with open(guild_id, 'r') as file:
    guild_id_json = json.load(file)
        
with open(discordservers_com, 'r') as file:
    discordservers_com_json = json.load(file)

guildID = guild_id_json["guild_ID"]
discord_user = discordservers_com_json["discord-user"]
discord_servers_session = discordservers_com_json["discord-servers-session"]
discord_servers_session_sig = discordservers_com_json["discord-servers-session_sig"]
    
def main():
    with requests.Session() as session:
        session.cookies.set("discordservers-session", str(discord_servers_session))
        session.cookies.set("discordservers-session.sig", str(discord_servers_session_sig))
        session.cookies.set("discord-user", str(discord_user))
        session.headers.update({"referer": f"https://discordservers.com/server/{guildID}/bump"})

        discordservers_com_give_gems = f"https://discordservers.com/api/gems/give"

        discordservers_com_headers = {
                "User-Agent": get_user_agent(),
                "Accept": "application/json",
                "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
                "Content-Type": "application/json",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Alt-Used": "discordservers.com",
                "Priority": "u=0",
                "Cache-Control": "max-age=0"
        }

        error_count = 0 # if 5 times error then break
        bump_count = 0 # how many times did it bump

        while True:
            try:
                discordservers_com_response = session.post(discordservers_com_give_gems, headers=discordservers_com_headers, json={"server": str(guildID)})
                status = discordservers_com_response.status_code
                data = discordservers_com_response.json()

                info = f"STATUS: {status} DATA: {data}"
                last_err = ''

                if data:
                    logger.info(str(info))

                    if data.get("amount") == 25:
                        bump_count += 1
                        bumped = f"Bumped {beautify_amount(bump_count)} time today!"
                        cprint("green", ">", bumped)
                        logger.info(bumped)

                    elif data.get("time_left"):
                        sleep = f"Sleeping for: {seconds_to_time(data['time_left'])}"
                        logger.info(str(sleep))

                        live_timer(data['time_left'])
                else:
                    logging.warning(f"{status} Request didn't get DATA.")
                    cprint("red", "!", "Please check if COOKIES in config is valid!")
                    time.sleep(5)
                
            except Exception as e:
                logger.error(str(e))
                if error_count > 4:
                    last_err = str(e)
                    logger.warning("Stopping Program.")
                    break
                else:
                    error_count += 1
                    logger.warning(f"Error Count: {str(error_count)}")
                continue
                
    logger.info("PROGRAM STOPPED!!! Bumps:", str(bump_count), "Errors:", str(error_count), "Last Error Status:", str(last_err))
    exit()

if __name__ == "__main__":
    cprint("green", "!", "Running Auto Bumper!")
    cprint("green", ">", f"For additional information please check run-time.log file.")
    main()
