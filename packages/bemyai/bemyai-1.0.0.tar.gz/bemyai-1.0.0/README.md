### Be My AI

#### Console
```bash
bm login -l ru "your_email@domain.tld "1yourpassword3"
bm -l ru recognize "path/to/photo.jpg"
```

##### Example
```
# building
E:\bemyai>poetry build

# installing
E:\bemyai>pip install .\dist\bemyai-0.1.8-py3-none-any.whl

# I'm already logged in

# Recognizing...
E:\bemyai>bm -l ru recognize E:\aribook1_b.jpg
На фотографии изображена обложка книги с изображением Арианы Гранде. В верхней части обложки написано "100% НЕОФИЦИАЛЬНО" на фоне розового прямоугольника. Ниже следует текст:

Ариана — не просто очередная эстрадная принцесса, она —
одна из крупнейших мировых звезд
и самая популярная женщина в Инстаграме.

Далее идет желтый прямоугольник с текстом:

Любой альбом и любой сингл всегда занимает верхние строки в чартах,
Ариана является иконой стиля, достойной защитницей прав женщин,
добровольцем, актрисой и выжившей жертвой теракта.
В своей жизни она ставит на первое место семью, включая
семерых спасенных ею собак!

С помощью четырех октав Ариана, вероятно, может считаться пушкой
в мире поп-музыке.
И если кто-то думает
что способен приблизиться
к ее коронованной особе,
то пусть еще раз послушает
песню Арианы Гранде
Thank You, Next!

В нижней части обложки на розовом фоне написано "100% ИДОЛ". Также присутствует штрих-код с ISBN номером 978-5-04-114282-3 и ссылка на веб-сайт www.vk.com/eskmo_kids.

# You can ask GPT about this image in the chat
# Type Q for exit
# Or pass `-ni` to return the response and exit
# in this case, you can ask a question with an ask command
# e.g.
# bm ask "Your question"
E:\bemyai>
```

#### Python
```python
import sys
import asyncio
from bemyai import BeMyAI
from loguru import logger
logger.remove()
logger.add(sys.stderr, format="{message}", level="INFO")

async def main():
    # you can specify another language,
    # for example, Russian
    
    # get token
    bm = BeMyAI(response_language="en")
    result = await bm.login(
        "test@example.com",
        "yourpassword"
    )
    # and save result.token for future requests
    
    # authorization by token
    bm = BeMyAI("your_token", response_language="en")
    
    # recognize photo
    sid, chat_id = await bm.take_photo("pic.jpg")
    for i in range(2):
        async for bm_response in bm.receive_messages(sid):
            message = bm_response
            if message.user:
                continue
            print( message.data )
            if i == 0:
                # We ask a question
                sid, chat_id, _message = await bm.send_text_message(
                    chat_id,
                    "Describe it in more detail"
                )

if __name__ == "__main__":
    asyncio.run(main())
    
```

##### Example output

I saved the python example,
specified my token and the Russian language,
specified the path to the image and got this result:

```
dl folder already exists
get app user config from internet
recognizing new photo: JPEG, 1215x2160, RGB
create new chat
resizing image
image processed: jpeg, 1125x2000
requested upload image config
get app user config from cache
Starting upload image to Amazon
Uploaded successfully
removeing processed image
upload image finished
Got new message
Got new message
На фотографии изображена книга с названием "Ариана Гранде. Главная книга фаната". На обложке множество фотографий Арианы Гранде в разных образах. В верхнем левом углу написано "100% неофициально". В нижнем правом углу обложки есть маркировка "18+".
Got new message
Got new message
На обложке книги изображено семь различных фотографий певицы Арианы Гранде. Она показана в разных нарядах и прическах, в том числе с её знаменитым высоким хвостом. На одной из фотографий она в большом белом банте на голове. На другой - в черном топе и с кепкой. Есть изображение, где она поет в микрофон, закрыв глаза и подняв голову вверх. Цвета обложки - розовый, белый и черный. На обложке также присутствуют розовые и белые геометрические элементы, а также надписи розового цвета.

E:\bemyai>
```
