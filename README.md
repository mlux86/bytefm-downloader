# byte.fm favorite program downloader

Easy way of downloading the latest releases of your favorite programs form [byte.fm](https://byte.fm).

**Requires a ["Freunde von Byte.FM"](https://www.byte.fm/freunde/mitglied-werden/) membership.**

## Configuration

### Installing dependencies

Firefox is used as a selenium webdriver. Hence, it needs to be installed
along `geckodriver`.

Furthermore, install the required Python 3 dependencies:

``` 
$ pip3 install urllib3 selenium pyyaml
``` 

### Creating a configuration file

Create a configuration file named `config.yml` looking like this:

``` 
username: your_username
password: your_password
``` 

containing your byte.fm credentials.

## Running it

``` 
$ python3 main.py
``` 
