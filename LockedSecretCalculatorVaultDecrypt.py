####
# A python script designed to decrypt media files encrypted using the Android application
# 'LOCKED Secret Calculator Vault'. Script is not dependant on PIN / Pattern but it will decrypt it.
# Original blog post: https://theincidentalchewtoy.wordpress.com/2022/02/05/decrypting-locked-secret-calculator-vault/
####

## Import all required modules
import sys
import os
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import filetype 
from pathlib import Path

## Known constants
standardKey = '526e7934384e693861506a59436e5549'
standardIV = '526e7934384e693861506a59436e5549'

### Take arguments
##/data/data/com.lkd.calculator
cwd = sys.argv[1]
## /sdcard/.locked_vault
media_dir = sys.argv[2]
## output folder
output_dir = sys.argv[3]


### Decryption function
def decryptData(encryptedInput):
    ### The PIN is encrypted using a standard key and IV (which are both the same.
    cipher = AES.new(bytes.fromhex(standardKey), AES.MODE_CBC, bytes.fromhex(standardIV))
    ### Decrypt the data
    decryptedData = cipher.decrypt(encryptedInput)
    ### Return the decrypted value
    return(decryptedData)

### Copy the file after the file extension has been determined
def copyWithExt(dataToWrite, outputPath):
    ### Determine the correct file extension
    fileExtension = filetype.guess(dataToWrite)
    ### Open the new file for writing
    with open ((os.path.join(outputPath + f'.{fileExtension.extension}')) , 'wb') as fileOut:
        ### Write the data to the new file
        fileOut.write(dataToWrite)
        ### Close the output file
        fileOut.close()
        

#### DECRYPTING THE PIN ####
### Check for shared_preferences subfolder
if('shared_prefs' in next(os.walk(cwd))[1]):
    ### If shared_preferences folder exisits, check for the file 'share_locked_vault.xml'
    if(os.path.join(cwd, 'shared_prefs\share_locked_vault.xml')):
        shared_prefs = (os.path.join(cwd, 'shared_prefs\share_locked_vault.xml'))
        tree = ET.parse(shared_prefs)
        root = tree.getroot()
        print('------------------------------------------------------------------------------')
        
        #### PIN ####
        ### If the file exisits, read the contents of <string name="57DFEA9AEC99CD87013E3862B9DE5B7D">  
        try:
            encryptedPIN = root.findall('./string[@name="57DFEA9AEC99CD87013E3862B9DE5B7D"]')[0].text
            ### Print the encrypted PIN
            print(f'The encrypted PIN is:\t\t{encryptedPIN}')
            ###Decrypt the PIN
            decryptedPIN = unpad(decryptData(bytes.fromhex(encryptedPIN)), AES.block_size)
            print(f'The decrypted PIN is:\t\t{(decryptedPIN).decode("utf-8")}')
        except IndexError:
            print(f'\t\t**There is no PIN present**\t\t')
        
        #### PATTERN ####
        ### If the file exisits, read the contents of <string name="85B064D26810275C89F1F2CC15E20B442E98874398F16F6717BBD5D34920E3F8"> 
        try:
            encryptedPattern = root.findall('./string[@name="85B064D26810275C89F1F2CC15E20B442E98874398F16F6717BBD5D34920E3F8"]')[0].text
            ### Print the encrypted Pattern
            print(f'The encrypted Pattern is:\t{encryptedPattern}')
            ###Decrypt the Pattern
            decryptedPattern = unpad(decryptData(bytes.fromhex(encryptedPattern)), AES.block_size)
            print(f'The decrypted Pattern is:\t{(decryptedPattern).decode("utf-8")}')
        except IndexError:
            print(f'\t\t**There is no Pattern present**\t\t')
        print('------------------------------------------------------------------------------\n')
    else:
      print('\n\shared_prefs\' file could not be found, exiting')
      exit  
else:
    print('\n\shared_prefs\' file could not be found, exiting')
    exit

#### DECRYPTING THE FILES ####
### Two areas to decrypt, that database and the media files. It will only target the one database but all the media
### Check to see if the database is present
for dirpath, dirnames, filenames in os.walk(media_dir):
    ### For each folder in the media directory
    for directories in dirnames:
        print(f'Found folder:\t\t\t\'{directories}\'\n')
        print('------------------------------------')
        print(f'Checking for files in \'{directories}\'')
        print('------------------------------------')
        ### Check if there are any files in the folder
        if not(os.listdir(os.path.join(dirpath,directories))):
            print('Folder contains no files\n')
            print('------------------------------------')
        else:
            print('Found files...will attempt to decrypt')
            print('Creating output folder for decrypted files')
            ### If the folder doesn't exist, create it.
            if not os.path.exists(os.path.join(output_dir,directories)):
                os.makedirs(os.path.join(output_dir,directories))
                print('Created external directory')
            else:
                print('Directory already exists, skipping creation')
            ### For each file in the directory
            for files in (os.listdir(os.path.join(dirpath,directories))):
                ### If the file ends with db skip it
                if files.endswith(".db"):
                    print(f'This is the DB file which can be dealt with using DB Browser (sqlcipher)')
                    print(f'Not decrypted')
                else:
                    print(f'Found file:\t\t\t{files}')
                    ### If the file starts with 'h-' it is not encrypted
                    if(files.startswith("h-")):
                        print('File does not require decryption, attempting to copy')
                        ### Open the file for reading
                        with open ((os.path.join(dirpath,directories, files)), 'rb') as currentFile:
                            ### Copy the file and append extension
                            copyWithExt(currentFile.read(), os.path.join(output_dir,directories,files))
                            ### Close the working file
                            currentFile.close()
                            ### Status print
                            print(f'File Copied Successfully')
                    ### If the file doesn't start with 'h-' continue to decrypt it.
                    else:
                        print(f'Attempting to decrypt:\t\t{files}')
                        ### Open file to be decrypted
                        with open ((os.path.join(dirpath,directories, files)), 'rb') as currentFile:
                            ### Decrypt the data
                            decryptedData = decryptData(currentFile.read())
                            ### Create the decrypted file
                            copyWithExt(decryptedData, os.path.join(output_dir,directories,files))
                            ### Close the working file
                            currentFile.close()
                            ### Status print
                            print(f'File Decrypted Successfully') 