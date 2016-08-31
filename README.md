**Hey!** This software was made to meet a particular need that I personally had, and it might not be terribly useful for anybody else.
* * *

intercom
==============
A simple server that combines your phone-powered intercom with Twilio to do useful things. Sort of.

This project might be useful to you if the following apply:

* You live in a home with an intercom system that calls a phone number whenever somebody wants access to the building.
* To grant people access, you answer the phone call and press some keys (e.g., pressing 9 grants access to the building).
* You've configured your intercom system to call a Twilio number.
* Sometimes you just want to blindly accept all people into the building for a limited amount of time. (For example, you've invited a bunch of friends over and you don't want to respond to the intercom when each of them arrives.)


# Bootstrapping the server

1. Clone this repository and `cd` into it.
1. Install `tox` globally on your system: `pip install tox>=2.3`
1. Run `tox`
1. Copy the config templates somewhere else: `cp -r configs $CONFIG_DIR`
1. Edit the files in `$CONFIG_DIR` to meet your needs.


# Running the server

## Locally

1. `cd` into the project directory.
1. Run `./dev/bin/intercom $CONFIG_DIR/global-dev.ini $CONFIG_DIR/app.ini`

## In production

This is going to depend on your web host. But basically you'll want to run...

```sh
intercom $CONFIG_DIR/global-prod.ini $CONFIG_DIR/app.ini
```

...as a daemon. Then, you'll likely need to configure some other server (or use your web host's config panel) to forward traffic to the port that the intercom server is listening on.

There's no support for WSGI presently, but [CherryPy itself supports WSGI](http://docs.cherrypy.org/en/latest/deploy.html#wsgi-servers), so it shouldn't be too hard to modify `intercom/__main__.py` to fit in with a WSGI server.


# Configuring Twilio

Configure a phone number in Twilio such that voice calls hit a "webhook" on your server. Assuming your server is handling requests at `http://intercom.com`, the URL will look like this:

```
http://intercom.com?PhoneNumberToDial=%2B15552223333&ExpectedFrom=%2B15558889999
```

Here, `%2B15552223333` is the URL encoded form of `+15552223333`. So `PhoneNumberToDial=%2B15552223333` declares that I want Twilio to call me at `+ 1 555 222 3333` when someone dials my intercom.

Similarly, `ExpectedFrom=%2B15558889999` encodes the phone number `+1 555 888 9999`. This should be the phone number of your intercom itself. Why do we care? This lets us prevent people using our Twilio number for unrelated calls — the server won't forward along the call unless it came from this number.

Both of these values could be included in the application config for the intercom server itself, I suppose. Right now, we let Twilio supply them.
