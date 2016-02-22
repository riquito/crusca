Crusca, the picky commit reader
===============================

[![Build Status](https://api.travis-ci.org/riquito/crusca.svg?branch=master)](https://travis-ci.org/riquito/crusca) [![Coverage Status](https://coveralls.io/repos/github/riquito/crusca/badge.svg?branch=master)](https://coveralls.io/github/riquito/crusca?branch=master)

Disheartened by yet another commit with the wrong message's format? You don't
want to spend your time pointing out to your mates that you agreed to follow
some conventions? Worry no more, Crusca will be glad to lift the burden from
your shoulders.

Thanks to a ~~neural network~~ ~~smart~~ stupid simple algorithm it can check
that the commits' messages follow your guidelines and set a failed status on
the commits who don't.

### Requirements

python >= 3.4

### Install

    # clone the repository
    git clone git@github.com:riquito/crusca.git
    cd crusca

    # install required packages
    sudo apt-get install -y python3 python-virtualenv
    virtualenv -p $(which python3) ~/.crusca-env
    source ~/.crusca-env

    # install crusca dependencies
    pip install -r requirements.txt
    
    # copy default configuration
    cp config/config.yml.dist config/config.yml

### Run (you probably want to read `configuration` before)

    source ~/.crusca-env
    ./crusca

### Run tests

    source ~/.crusca-env
    python -m unittest discover

### Check coverage

    source ~/.crusca-env
    coverage run --branch --include='src/*'  -m unittest discover
    coverage report

### Setup the webhook on Github

You'll need to create a new webhook: https://github.com/[owner]/[repo]/settings/hooks/new

The payload url is http[s]://your.domain/push-event

### Configuration (config/config.yml)

`AUTH_TOKEN` is a [Github OAUTH token](https://github.com/settings/tokens/new). You just need the scope repo:status

`RULES` is a list of the enforced rules. The available rules are

##### bad_start

Check a list of words that must not be first. Useful if you want to enforce
for example `present simple`, or avoid `fixup!` or `Merge` commits.
Case insensitive.

e.g. bad_start: ['fixup!', 'added', 'fixed', 'removed']

##### bad_word

Check that certain words are not present in the message.
Case insensitive.

e.g. bad_words: ['wip']

##### capital_letter

Ensure that the first letter of the commit's message is a capital letter.
It doesn't take any argument. Only ASCII characters are checked.

e.g. capital_letter: ~

##### ending_dot

Check if the last character is, or is not, a dot.

e.g. ending_dot: false # require that the message does NOT end with a dot

e.g. ending_dot: true  # require that the message DOES end with a dot

### Deploy with Apache and mod_wsgi

In this example crusca has been cloned in
`/var/www/crusca/crusca`
and the virtualenv is at
`/var/www/crusca/env`

    # example app.wsgi

    activate_this = '/var/www/crusca/env/bin/activate_this.py'
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})
    
    import os, sys
    sys.path.insert(0, '/var/www/crusca/crusca')
    
    os.environ['ENVIRONMENT'] = 'PRODUCTION'
    
    from src.crusca import main
    application = main()
    
Here is an Apache's virtualhost file. Paths and the user must be changed.

    # example crusca.virtualhost.conf

    <VirtualHost *:80>
        ServerName crusca.example.com
    
        WSGIDaemonProcess crusca_app user=riquito group=riquito threads=1 processes=10
        WSGIScriptAlias / /var/www/crusca/app.wsgi
    
        <Directory /var/www/crusca>
            WSGIScriptReloading On
            WSGIProcessGroup crusca_app
            WSGIApplicationGroup %{GLOBAL}
    	    Require all granted        
        </Directory>
    
        LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" common
        CustomLog /var/log/apache2/crusca-access.log common        
        ErrorLog  /var/log/apache2/crusca-error.log
    
    </VirtualHost>

### License

Apache 2.0, see LICENSE file
