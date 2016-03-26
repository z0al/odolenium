# Odolenium

## Introduction

Odolenium is a simple, API to interact with [Odoo](http://odoo.com) using
[Selenium](http://seleniumhq.org) web driver.

**Warning** at the moment, odolenium only supports Odoo v9

## Getting started

You should have Python 3 installed in order to use Odolenium, then follow the
steps bellow:

* Clone this repository using git
```sh
$ git clone https://gitlab.com/ahmed_taj/odolenium.git
```

* Then, change to odolenium directory
```sh
$ cd odolenium
```

* It's better to test odolenium first using this command
```sh
$ python3 setup.py test
```

**Note** most test cases assume you have odoo server installed and running
with the following configration:

    url = http://localhost:8069
    admin_password = admin
    user = admin
    password = admin
    database = db1

* If everything went fine, you can now install it using:

```sh
$ python3 setup.py install
```

## Example

```python3
from selenium.webdriver import Firefox
import odolenium

o = odolenium.OdooUI(Firefox(),{
    'url':'http://localhost:8069',
    'admin_password':'admin'
    }
)
o.login('admin','admin','test')
```

You should see something like the following output

```log
2016-03-26 12:47:55,816 INFO Odolenium: Setting up XML-RPC connection to http://localhost:8069/
2016-03-26 12:47:55,820 INFO Odolenium: Connection succeed
2016-03-26 12:47:55,822 INFO Odolenium: Found version 9.0c Odoo server
2016-03-26 12:47:55,822 INFO Odolenium: Trying to log in over XML-RPC
2016-03-26 12:47:56,060 INFO Odolenium: Logged in as 'admin'
2016-03-26 12:47:56,060 INFO Odolenium: Searching for 'web_selenium' module
2016-03-26 12:47:56,077 INFO Odolenium: trying to install module 'web_selenium'
1 module(s) selected
1 module(s) to process:
  to install	web_selenium
2016-03-26 12:47:57,967 INFO Odolenium: Done
2016-03-26 12:47:57,968 INFO Odolenium: GET http://localhost:8069
```
And of course new Firefox window that is going to automatically
login with the given credentials.

## Contributing

There are many ways to contribute, either by creating an issue, improve documentation
or adding a feature. for more details see CONTRIBUTING.md .

## License

This project is released under the terms and conditions of MIT license.


