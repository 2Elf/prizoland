Integration tests
================

### Установка 

Создаем виртуальное окружение `integration`, и устанавливаем зависимости:

```bash
mkvirtualenv integration
workon integration
pip install -r requirements.txt
```

Selenium тесты выполняются в Firefox, выполним установку если оный отсутствует в системе:

```bash
sudo apt-get install firefox
```

Для выполнения тестов на headless сервере нам понадобится виртуальный дисплей.
Нужно установить Xvfb сервер, он держит базовый виртуальный дисплей в памяти и, таким образом приложения,
которым необходимы функциональные возможности графических средств, могут работать на машинах без X server.

```bash
sudo apt-get install Xvfb
```

Для его работы в моем случае понадобилась установка дополнительных пакетов.
Фейк Х сервер использует компоненты трушного Х сервера, скорее всего нужно будет установить его ядро.

```bash
ssudo aptitude install xserver-xorg-core
```
И ряд дополнительных либ и фонтов

```bash
sudo apt-get install -y x11-xkb-utils
 
# add fonts
sudo apt-get install -y xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic
sudo apt-get install -y x-ttcidfont-conf cabextract ttf-mscorefonts-installer
#(you'll have to enable the multiverse repo to get ttf-mscorefonts-installer)
#Accept the EULA terms for ttf-mscorefonts-installer.
#Then:
sudo dpkg-reconfigure --default-priority x-ttcidfont-conf aptitude install xserver-xorg-core
```

### Запуск Xvfb сервера

Запустим Xvfb попросив его использовать дисплей с номером 5, например (скорее всего не используется)

```bash
Xvfb :5 -screen 0 1024x768x8
```


`-screen 0 1024x768x8` Создает экран номер 0 на дисплее 5 с разрешением 1024x768 и 8-битной разрядностью цветов.
Очевидно, эти показатели могут быть такими, какие вы хотите.

Очень просто сделать так чтобы Selenium использовал виртуальный дисплей. 
Установка переменной среды под названием "DISPLAY" в Linux говорит любому запускаемому графическому приложению запускаться на указанном дисплее.
Установим ее значение равным тому какой дисплей и экран держит в памяти Xvfb.

```bash
DISPLAY=:5.0
```

### Настройка

Настройки хранятся в [`conf/main.py`]

Настройки которые вам скорее всего нужно изменить:

```python
HOST = 'viotest.local'  #  Хост по которому доступен проэкт, у меня проэт развернут локально и viotest.local переадресуется на 127.0.0.1 .
PORT = 8000  # Дефолтный порт по которому доступен
```


### Использование

Тесты выполняется запуском скрипта launcher.py в корне директории, который выполняет все 'test_*.py' юнит тесты из корневого каталога и вложеных директорий.

```bash
python launcher.py
```

Очевидно , что тесты могут быть запущены любым другим unittest.TestLoader(), который подхватит 'test_*.py' тесты.
