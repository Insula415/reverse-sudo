# reverse-sudo

Code something to revert a sudo chmod, like a bash command and it first makes a note of all the files and then does it. it'd be like "sudo superchmod", grabs all the permissions of that folder maybe using LHAT.

This code allows you to reverse a sudo chmod, in case of accidental permission changes. It first creates a backup of all the files in your current directory, then allows you to choose a state to revert back to.

<img src="1.png">
<img src="2.png">
