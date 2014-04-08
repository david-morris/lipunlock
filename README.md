Lipunlock Auth: with the power of speech, use your phone as an authentication factor!
This isn't ready yet.  If you use this software as is, you will be cracked.
Developers: this is a PAM module.

Todo: 
Add an X509 cert on the computer to verify that an attacker isn't talking to the phone side.
Get the android app in the repo (it's already built.).
Add a beep on the android app
Make the android app just start listening instead of asking you to press a button.
Testing
Make a makefile after all those things have been done.
Add timing, so that the synchronicity of the app does not depend on the network speed.

Installation Instructions:
Don't.

But I really want to use this!
Use pam_permit instead. Currently, it's just as secure.
