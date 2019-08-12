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
1. Install `tox` globally on your system: `pip install 'tox>=3.13'`
1. Run `tox`
1. Copy the config templates somewhere else: `cp -r configs $CONFIG_DIR`
1. Edit the files in `$CONFIG_DIR` to meet your needs.


# Running the server

## Locally

1. `cd` into the project directory.
1. Run `./dev/bin/intercom $CONFIG_DIR/global-dev.ini $CONFIG_DIR/app.ini`

## In production

This is going to depend on your web host. But basically you'll want to run the server as a daemon:

```sh
intercom $CONFIG_DIR/global-prod.ini $CONFIG_DIR/app.ini --daemon-pid-file $SOME_DIR/pid
```

Then, you'll likely need to configure some other server (or use your web host's config panel) to forward traffic to the port that the intercom server is listening on. While the server is running, `$SOME_DIR/pid` will hold the server's process ID. You can say `kill $(<$SOME_DIR/pid)` to stop the server.

There's no support for WSGI presently, but [CherryPy itself supports WSGI](http://docs.cherrypy.org/en/latest/deploy.html#wsgi-servers), so it shouldn't be too hard to modify `intercom/__main__.py` to fit in with a WSGI server.


# Configuring Twilio

Configure a phone number in Twilio such that voice calls hit a "webhook" on your server. Assuming your server is handling requests at `http://intercom.com`, the URL will look like this:

```
http://intercom.com?PhoneNumberToDial=%2B15552223333&ExpectedFrom=%2B15558889999
```

Here, `%2B15552223333` is the URL-encoded form of `+15552223333`. So `PhoneNumberToDial=%2B15552223333` declares that I want Twilio to call me at `+ 1 555 222 3333` when someone dials my intercom.

Similarly, `ExpectedFrom=%2B15558889999` encodes the phone number `+1 555 888 9999`. This should be the phone number of your intercom itself. Why do we care? This lets us prevent people using our Twilio number for unrelated calls — the server won't forward along the call unless it came from this number.

**Why do it this way?** Letting Twilio supply these values keeps clever people from learning your personal phone number. Twilio uses the `From` parameter to tell the intercom server who's dialing. Knowing this, a person could learn your intercom's phone number and visit `http://intercom.com?From=%2B15558889999`. The intercom server would think Twilio is reporting a call from your intercom, so it would emit a directive instructing Twilio to dial your personal phone number. Uh-oh, here come the prank calls!


# Granting temporary access to all callers

If you're having friends over, it can be a hassle to receive a phone call each time somebody arrives. That's why _grant periods_ were invented. After setting the grant code and length in your application settings, just navigate to...

```
http://intercom.com/grant?code=YOUR-SUPER-SECRET-GRANT-CODE
```

...and you'll start a grant period of the specified length. During this period, the intercom server will respond to all calls on your behalf, granting access blindly.
