# byte.fm favorite program downloader

Easy way of downloading the latest releases of your favorite programs form [byte.fm](https://byte.fm).

**Requires a ["Freunde von Byte.FM"](https://www.byte.fm/freunde/mitglied-werden/) membership.**

## Configuration

### Installing dependencies

Google Chrome is used as a selenium webdriver. [Find out how to install the webdriver here.](https://chromedriver.chromium.org/home)

Furthermore, install the required Python 3 dependencies:

``` 
$ pip3 install urllib3 selenium
``` 

### Creating a configuration file

Create a configuration file named `config.yml` looking like this:

``` 
username: your_username
password: your_password
directory: /target/download/directory
shows:
    - show1
    - show2
``` 

containing your byte.fm credentials.

## Running it

``` 
$ python3 main.py
``` 
