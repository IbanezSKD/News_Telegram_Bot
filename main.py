
import asyncio
import aiohttp
import time
import TelegramB

@asyncio.coroutine
def call_url(url):
    f = open('url.txt', 'w', encoding="utf-8")
   #print('Starting {}'.format(url))
    response = yield from aiohttp.ClientSession().get(url)
    data = yield from response.text()
    #print('{}: {} bytes: {}'.format(url, len(data), data))
    sp_line = str('{}: {} bytes: {}'.format(url, len(data), data + "\n"))
    f.write(sp_line)
    f.close()
    return data

def main():
    flag = 0
    news = []
    startH = 0
    finH = 0
    finfinH = 0
    finT = 0
    link = ''
    title = ''
    startNameTitle = 0
    stop = 0
    urls = ['https://korrespondent.net/']
    news_bot = TelegramB.BotHandler('767933591:AAFhvDYZcynE4otuncc8TMZQOmCJ3FlDgDE')
    futures = [call_url(url) for url in urls]
    asyncio.run(asyncio.wait(futures))

    while True:
        time.sleep(180)
        f = open('url.txt', 'r', encoding="utf-8")
        flag = 0

        for line in f:

            if stop == 1:
                stop = 0
                break

            if flag == 0:
                if "class=\"time-articles" in line:
                    flag = 1
            else:
                if 'id="aShowMoreList"' in line:
                    break
                else:
                    for i in range(len(line) - 3):

                        if line[i] == 'h' and line[i + 1] == 'r' and line[i + 2] == 'e' and line[i + 3] == 'f':
                            startH = i + 6

                        if line[i] == '"' and line[i + 1] == '>' and startH > 0:
                            finH = i
                            link = line[startH: i]
                            startH = 0

                        if line[i] == '<' and line[i + 1] == '/' and line[i + 2] == 'a':
                            finT = i
                            for i in range(finT, finH, -1):
                                if line[i] == '>':
                                    startNameTitle = i + 1
                                    break
                            title = line[startNameTitle: finT]

                            if link in news:
                                stop = 1
                                finfinH = 0
                                break

                            news.append(link)
                            news_bot.send_message(440590142, '{}'.format(link))
                            print(title, '-----', link)
                            finfinH = 0
                            break

        time.sleep(1)
        f.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

