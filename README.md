# LockedSecretCalculatorVault
A python script to decrypt media files encrypted using the Android application 'LOCKED Secret Calculator Vault'. Will identify PIN / pattern. (https://play.google.com/store/apps/details?id=com.lkd.calculator&hl=en_GB&gl=US)
Original Blog Post: 

'LOCKED Secret Calculator Vault' mimics the functionality of a calculator whilst hidng the vault behind a user created PIN code. The files are encrypted using _"proven military-grade AES encryption which is used by governments & banks worldwide. Hide photo, Lock photos and videos, then put them into your private Calculator vault. Now they are in the safest place in the world! Nobody can reach them except you."_

## Script Usage

Script takes 3 arguments:

1. Data folder (/data/data/com.lkd.calculator)
2. Encrypted media folder (/sdcard/.locked_vault/)
3. Output folder

The script is designed to identify any PIN or pattern lock data within the relevant files. It will then decrypt any user encrypted files and output them with a 'best guess' file extension.

DataData for browser activity and 'notes' can be found in the encrypted database file: locked_vault.db 

Any questions, or issues let me know https://twitter.com/4n6chewtoy
