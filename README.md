# aws_signin
A disgusting script that lets you signin to the AWS console using your keys from the command line.

## How to use it

Load your AWS keys as environment variables, then run

    aws_signin.py

This will print out a signed url that will automatically sign you into the AWS console.

Because it just prints the url, you can feed it to other things; for example, get it to open in firefox automatically:

    aws_signin.py | xargs firefox
    
Or copy to the clipboard:

    aws_signin.py | xclip -selection clipboard

Then you can use Firefox's built-in container tabs to open multiple AWS accounts in different tabs, just paste the url in and you're golden.
