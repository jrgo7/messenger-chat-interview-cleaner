# Messenger Chat Interview Cleaner

Let's say you're an interviewer and want to copypaste a Messenger chat from one
of your interviewees. Directly copypasting the chat will lead to a lot of extra
stuff getting pasted, like:

```
You sent
{{A message you sent}}
{{Nickname of Recipient}}
{{A message the recipient sent}}
{{Nickname of Recipient}}
{{Name of Recipient}}
{{A message the recipient sent}}
```

This program hopes to assist in cleaning out those extra stuff.

## Sample Usage

1. Run `main.py`.
2. Copy-paste from Messenger into a .txt file. Open that text file using the app.
   1. Alternatively, use the provided `demo.txt` file in this directory.
3. Right click on any lines to mark them as an "Interviewer:", "Interviewee:", or for deletion.
4. Click on "Process transcript", and then "Save as...".
