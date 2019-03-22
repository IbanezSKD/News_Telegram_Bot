
import asyncio
import aiohttp
import time
import TelegramB

# Функция которая записывает в url.txt html код переданного сайта
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

    # Различные флаги (начала - конца ссылки)

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

    urls = ['https://korrespondent.net/'] # Сайт с которого будем брать новости
    news_bot = TelegramB.BotHandler('767933591:AAFhvDYZcynE4otuncc8TMZQOmCJ3FlDgDE') # Токен телеграм бота

    while True:
        futures = [call_url(url) for url in urls]
        asyncio.run(asyncio.wait(futures))
        time.sleep(180)

        f = open('url.txt', 'r', encoding="utf-8") # !Были проблеммы с кодировкой отдельных символов
        flag = 0


        for line in f:

            if stop == 1:
                stop = 0
                break

            if flag == 0:
                if "class=\"time-articles" in line: # Артикль начала новостей
                    flag = 1
            else:
                if 'id="aShowMoreList"' in line: # Артикль конца новостей
                    break
                else:
                    for i in range(len(line) - 3):

                        if line[i] == 'h' and line[i + 1] == 'r' and line[i + 2] == 'e' and line[i + 3] == 'f': # Начало ссылки
                            startH = i + 6

                        if line[i] == '"' and line[i + 1] == '>' and startH > 0:
                            finH = i
                            link = line[startH: i] # Ccылка
                            startH = 0

                        if line[i] == '<' and line[i + 1] == '/' and line[i + 2] == 'a': # Начало темы ссылки
                            finT = i
                            for i in range(finT, finH, -1):
                                if line[i] == '>':
                                    startNameTitle = i + 1
                                    break
                            title = line[startNameTitle: finT] # Тема ссылки

                            if link in news: # Проверка есть ли новость в списке новостей
                                stop = 1
                                finfinH = 0
                                break

                            news.append(link) # Добавление в список всех новостей
                            news_bot.send_message(-1001455367918, '{}'.format(link)) # Отправка сообщения телеграм бота
                            print(title, '-----', link)
                            finfinH = 0
                            break

        f.close()
        time.sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

