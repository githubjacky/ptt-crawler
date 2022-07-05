## dependencies
*use your favorite virtual environment tool to install the dependencies, my choice will be the [pipenv](https://github.com/pypa/pipenv)*
```sh
pipenv install
```
**note that the current working directory should be 'src'**


## usage
1. input your ptt id and password
2. select the board and what kinds of content you want to see(0 is the specific option according to my preference)
    - 3)date
    - 5)content 
    - 15)push_content
    - 16)boo_content
    - 17)arrow_content
![screen shot](./img/01.png)
3. select the format


### command to execute the script(with [pipenv](https://github.com/pypa/pipenv))
*using pipenv*
```sh
pipenv run python src/main.py
```


# reference
- https://github.com/PttCodingMan/PyPtt
