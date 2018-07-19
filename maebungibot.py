import sys  
import irc.bot  
import requests  
  
  
class TwitchBot(irc.bot.SingleServerIRCBot):  
    def __init__(self, username, client_id, token, channel):  
        self.client_id = client_id  
        self.token = token  
        self.channel = '#' + channel  
        self.hogumastack = 0  
  
        #채널 ID를 얻기 위해 v5 API 호출  
        url = 'https://api.twitch.tv/kraken/users?login=' + channel  
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}  
        r = requests.get(url, headers=headers).json()  
        self.channel_id = r['users'][0]['_id']  
  
        # IRC bot 연결 생성  
        server = 'irc.chat.twitch.tv'  
        port = 6667  
        print('서버 ' + server + ', 포트 ' + str(port) + '에 연결 중...')  
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)  
  
    def on_welcome(self, c, e):  
        print(self.channel + '에 연결되었습니다.')  
  
        #봇을 사용하기 전에 채널 권한 부여가 필요  
        c.cap('REQ', ':twitch.tv/membership')  
        c.cap('REQ', ':twitch.tv/tags')  
        c.cap('REQ', ':twitch.tv/commands')  
        c.join(self.channel)  
  
    def on_pubmsg(self, c, e):  
        # If a chat message starts with an exclamation point, try to run it as a command  
        if e.arguments[0][:1] == '!':  
        cmd = e.arguments[0\].split(' ')[0][1:]  
        print('Received command: ' + cmd)  
        self.do_command(e, cmd)  
        return  
  
    def do_command(self, e, cmd):  
        c = self.connection  
  
        # Poll the API to get current game.  
        if cmd == "game":  
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id  
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}  
            r = requests.get(url, headers=headers).json()  
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])  
  
        # Poll the API the get the current status of the stream  
        elif cmd == "title":  
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id  
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}  
            r = requests.get(url, headers=headers).json()  
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])  
  
        # Provide basic information to viewers for specific commands        
        elif cmd == "!매붕이":
            message = "안녕!"
            c.privmsg(self.channel, message)  
  
        # The command was not recognized  
        else:  
            c.privmsg(self.channel, "Did not understand command: " \+ cmd)


                          def main():  
    username = "maebung_i_bot" # 별 의미 없습니다. 봇 계정의 이름은 twitch 사이트에서 조정해주면 됩니다.  
    client_id = "k1tu1gf5eopwz1fxm1u8ai28ljus7o" # Client ID  
    token = "oauth:hlx6ca4ony16wpzh5l5vtf4p95aqi6" # oauth: 는 빼고 뒷부분만 적어주시면 됩니다.  
    channel = "maejaeng" # 봇이 접속할 채널입니다. 테스트할 땐 본인의 트위치 계정을 적어주세요.
  
    bot = TwitchBot(username, client_id, token, channel)  
    bot.start()  
    
if __name__ == "__main__":  
    main()

