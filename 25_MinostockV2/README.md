# 25. MinostockV2

Author: pin3apple07

Phase 3 | forensics

Flag: `labyrinth{why_d035_n0_0n3_d0_m4c05_df1r}`

## Description

The key you obtain leads you to  room with a strange creature. It has the body of a lion, the wings of a great bird, and the head and torso of a woman. It gives you a file to test your investigation skill. If you can answer its questions, it says it will provide you passage to the Minotaur. Can you pass the Sphinx's trial?

Handout: https://drive.google.com/file/d/1le2u-qJdMR75nE5zvNcEHXCCKqsXa9uf

## Solve

So the handout gives us 2 folders `Users` and `var`, in the Users folder there was just 1 user namely `raahat.khan`, further in the raahat.khan folder were various files and folders related to the user, namely Documents, Downloads, etc.

In the `var` folder there was `db/dslocal/nodes/Default/Users/raahat.khan.plist`

Following is the complete directory structure as a tree:

```
pineapple@macbook handout % tree
.
├── Users
│   └── raahat.khan
│       ├── Desktop
│       │   ├── Screenshot 2026-10-05 at 9.53.08 AM.png
│       │   ├── Screenshot 2026-10-05 at 9.55.43 AM.png
│       │   └── Screenshot_1.png
│       ├── Documents
│       ├── Downloads
│       │   ├── Beyond_Carving_Deterministic_Deleted_File_Recovery.pdf
│       │   ├── StockMonitor_Setup.dmg.download
│       │   │   ├── Info.plist
│       │   │   └── StockMonitor_Setup.dmg
│       │   ├── StockPulse_Installer.command
│       │   └── zoomusInstallerFull.pkg
│       ├── Library
│       │   ├── LaunchAgents
│       │   │   ├── com.google.keystone.agent.plist
│       │   │   ├── com.microsoft.autoupdate2.plist
│       │   │   ├── com.spotify.webhelper.plist
│       │   │   ├── com.stockpulse.helper.plist
│       │   │   ├── us.zoom.updater.gui.504.login.check.plist
│       │   │   └── us.zoom.updater.gui.504.plist
│       │   ├── Preferences
│       │   │   └── com.apple.LaunchServices.QuarantineEventsV2
│       │   └── Safari
│       │       └── History.db
│       └── Pictures
│           ├── Stock_source-d84b531c2d3441a7a0611e8af4d9d750.jpg
│           └── stocks-climbing-green-bull-market-1200x686-1-930x620.jpg
└── var
    └── db
        └── dslocal
            └── nodes
                └── Default
                    └── users
                        └── raahat.khan.plist

18 directories, 19 files
pineapple@macbook handout % 
```

In the whole handout there were multiple _plist_ files, which stands for `Property list`, this is macOS equivalent of _Registry_ in Windows, every entity in macOS tends to have a plist file, which contains data about the particular entity including user preferences, application states, and bundle metadata, it is present in all Apple OSs, for example every app bundle has one `Info.plist`, every user has its own `<username>.plist`.


### Stage 1
Let's get to the questions, the first question was: _What is the full name of the compromised account?_, its obvious that we'll find it in the plist file for raahat.khan, now to look at plist file there's different ways for different OSs, for macOS we have `plutil` and using it as `plutil -p <filename>`, the plist file can be looked at in a human readable format as below:


```
pineapple@macbook handout % plutil -p var/db/dslocal/nodes/Default/users/raahat.khan.plist
{
  "_writers_AvatarRepresentation" => [
    0 => "raahat.khan"
  ]
  "_writers_hint" => [
    0 => "raahat.khan"
  ]
  "_writers_inputSources" => [
    0 => "raahat.khan"
  ]
  "_writers_jpegphoto" => [
    0 => "raahat.khan"
  ]
  "_writers_passwd" => [
    0 => "raahat.khan"
  ]
  "_writers_picture" => [
    0 => "raahat.khan"
  ]
  "_writers_unlockOptions" => [
    0 => "raahat.khan"
  ]
  "_writers_UserCertificate" => [
    0 => "raahat.khan"
  ]
  "accountPolicyData" => [
    0 => {length = 426, bytes = 0x3c3f786d 6c207665 7273696f 6e3d2231 ... 2f706c69 73743e0a }
  ]
  "authentication_authority" => [
    0 => ";ShadowHash;HASHLIST:<SALTED-SHA512-PBKDF2,SRP-RFC5054-4096-SHA512-PBKDF2>"
    1 => ";SecureToken;"
    2 => ";Kerberosv5;;raahat.khan@LKDC:SHA1.D2C799C9933612E26D36FA2C94B4B89F57E416BB;LKDC:SHA1.D2C799C9933612E26D36FA2C94B4B89F57E416BB;"
  ]
  "AvatarRepresentation" => [
    0 => ""
  ]
  "generateduid" => [
    0 => "E3E9360A-B369-4FDD-990D-1CCB48D64C7E"
  ]
  "gid" => [
    0 => "20"
  ]
  "HeimdalSRPKey" => [
    0 => {length = 559, bytes = 0x3082022b a0820204 04820200 fe527b63 ... 32a8a204 02020fa0 }
  ]
  "hint" => [
    0 => ""
  ]
  "home" => [
    0 => "/Users/raahat.khan"
  ]
  "inputSources" => [
    0 => "<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
	<dict>
		<key>InputSourceKind</key>
		<string>Keyboard Layout</string>
		<key>KeyboardLayout ID</key>
		<integer>0</integer>
		<key>KeyboardLayout Name</key>
		<string>U.S.</string>
	</dict>
</array>
</plist>
"
  ]
  "jpegphoto" => [
    0 => {length = 133459, bytes = 0xffd8ffe0 00104a46 49460001 01000048 ... 4d34d3fc 4f73ffd9 }
  ]
  "KerberosKeys" => [
    0 => {length = 356, bytes = 0x30820160 a1030201 01a08201 57308201 ... 6861742e 6b68616e }
  ]
  "name" => [
    0 => "raahat.khan"
  ]
  "passwd" => [
    0 => "********"
  ]
  "picture" => [
    0 => "/Library/User Pictures/Flowers/Dandelion.heic"
  ]
  "realname" => [
    0 => "Sheikh Raahat Khan"
  ]
  "record_daemon_version" => [
    0 => "9054000"
  ]
  "ShadowHashData" => [
    0 => {length = 905, bytes = 0x62706c69 73743030 d2010203 0a5f101e ... 00000000 0000034b }
  ]
  "shell" => [
    0 => "/bin/zsh"
  ]
  "uid" => [
    0 => "504"
  ]
  "unlockOptions" => [
    0 => "0"
  ]
}
pineapple@macbook handout % 

```

From this output we can look at the "realname" field and get the answer of the first question which was: `Sheikh Raahat Khan`.


More ways to use the plutil command:

```
pineapple@macbook handout % tldr plutil

  plutil

  View, convert, validate, or edit property list ("plist") files.
  More information: https://keith.github.io/xcode-man-pages/plutil.1.html.

  Display the contents of one or more plist files in human-readable format:

    plutil -p file1.plist file2.plist ...

  Convert one or more plist files to XML format, overwriting the original
  files in-place:

    plutil -convert xml1 file1.plist file2.plist ...

  Convert one or more plist files to binary format, overwriting the original
  files in-place:

    plutil -convert binary1 file1.plist file2.plist ...

  Convert a plist file to a different format, writing to a new file:

    plutil -convert xml1|binary1|json|swift|objc path/to/file.plist -o path/to/new_file.plist

  Convert a plist file to a different format, writing to stdout:

    plutil -convert xml1|binary1|json|swift|objc path/to/file.plist -o -

pineapple@macbook handout % 
```

For linux users there's an installable utility via package managers called `plistutil`, can be used to convert it between binary,XML,json and OpenStep formats.

For windows or anything else the plist files can be parsed and generated via a python library `plistlib`.

The second question was: _What is the unique identifier (GUID) associated with the compromised user account?_, which can be retrieved from the "generateduid" field from the plutil output:

```
"generateduid" => [
    0 => "E3E9360A-B369-4FDD-990D-1CCB48D64C7E"
  ]
```

Answer to the second question being: `E3E9360A-B369-4FDD-990D-1CCB48D64C7E`.

The third question was: _What shell is configured for this account_, again from the plist file the answer can be retrieved from the "shell" field:

```
"shell" => [
    0 => "/bin/zsh"
  ]
```

Answer to the third question being `/bin/zsh`.


### Stage 2
Further after the details about the compromised user, we get a question about the attack, the 4th question was: _What is the domain of the malicious application that was downloaded?_, now to answer this question lets look at the Users/Downloads folder and we see:

```
pineapple@macbook Downloads % ls
Beyond_Carving_Deterministic_Deleted_File_Recovery.pdf
StockMonitor_Setup.dmg.download
StockPulse_Installer.command
zoomusInstallerFull.pkg
pineapple@macbook Downloads % 
```

One of these could be the malicious application, now there's 2 ways one could take to find the malicious one, before that lets analyze the stuff in downloads folder, one is a normal pdf, another is a zoom installer package both seem legit, the other two, one of them is a `.command` file and the other is a `.download` folder, from these the StockPulse_Installer.command seems a little suspicious because `.command` files in macOS are the ones we click on and it runs a shell command, which can be an easy way to trick someone into running shell commands, [read](https://superuser.com/questions/1193152/mac-command-file-extension-can-have-what-scripts) about it, then we have the .download folder, which has:

```
pineapple@macbook Downloads % ls
Beyond_Carving_Deterministic_Deleted_File_Recovery.pdf
StockMonitor_Setup.dmg.download
StockPulse_Installer.command
zoomusInstallerFull.pkg
pineapple@macbook Downloads % cd StockMonitor_Setup.dmg.download/ 
pineapple@macbook StockMonitor_Setup.dmg.download % ls
Info.plist		StockMonitor_Setup.dmg
pineapple@macbook StockMonitor_Setup.dmg.download % 
```

It has a setup dmg file and an Info.plist, so what is this directory, a `.download` item on a Mac is a temporary file bundle or folder that macOS (especially Safari) uses while a file is actively downloading or if a download is paused or interrupted.

[Read](https://apple.stackexchange.com/questions/233383/weird-download-files-keep-emerging-in-downloads-folder) about it.

So now it narrows down to `StockPulse_Installer.command`, now the question asks us for the domain not the file name, now lets talk about the 2 ways to get it I mentioned before.

One includes looking at the xattr(extended attributes of the file):

```
pineapple@macbook Downloads % xattr -l StockPulse_Installer.command    
com.apple.lastuseddate#PS: ?}?j
com.apple.metadata:kMDItemDownloadedDate: bplist00?3A?9Iv??

com.apple.metadata:kMDItemWhereFroms: bplist00?_;http://stockpulse-analytics.io/StockPulse_Installer.command_http://stockpulse-analytics.io/
                                                             I
com.apple.quarantine: 0081;6accb9ff;Safari;02E0E154-CAE3-4149-B1AD-285BD00E5B0C
pineapple@macbook Downloads %
```

From here we directly get that it got downloaded from `stockpulse-analytics.io`, using `Safari`, now the limitation to this solve is that `xattr` don't exist in NTFS, i.e windows, so to look at xattr from there either you have to directly look at it using the tar file, right after extracting it, it gets erased.

So the solve that universally works but is a little more work, includes a little intuition that the file was downloaded from `Safari`, once you get that you can look at the History.db in `Library/Preferences/Safari`, its a sqlite database, query for `history_visits` and you find few `http://` visits which is insecure, and one of them is `stockpulse-analytics.io`, hence the answer for Q4.


For the next question we needed the exact timestamp it was installed at, to get that we again have 2 ways, lets look at the one which is valid for all OSs, so there is something called a QuarantineEvent in macOS, a quarantine event happens the exact moment a file is written to the disk from an untrusted source, before the file is ever opened or executed.

The triggers for a quarantine event include web downloads, emails and messages, airdrop and when sandboxed apps download data.

Now all of this data is captured in a database which we saw in the tree earlier, namely `com.apple.LaunchServices.QuarantineEventsV2`, now we can look at this sqlite database using `DB browser for sqlite`:


<img width="1012" height="604" alt="Screenshot 2026-10-13 at 3 45 12 AM" src="https://github.com/user-attachments/assets/fd4963be-8feb-4d56-8240-84be732607ef" />

Now to figure out which one is our target we need to go back and look at the timestamp of visit to `stockpulse-analytics.io`, we'll see that the visit time is `812814828.588006` macOS time:

<img width="1010" height="155" alt="Screenshot 2026-10-13 at 4 02 48 AM" src="https://github.com/user-attachments/assets/57781ea9-0eed-4fcd-8143-e59c14aca75b" />

Now the closest to this should be the download time in the quarantine database which is the first one itself the time being `812814854.929657` again macOS time, now converting this to UTC we get `2026-10-04 13:54:14.929657 UTC`, till seconds being the answer to the 5th question.

[Read](https://nhimg.org/glossary/quarantine-events-database/) about the quarantine events db.


Lets discuss the other way to do this exact same thing in an easier way, valid mostly for macOS users, for this we need to understand something called Apple Spotlight its a built-in, system-wide search and quick-launch utility available across Apple operating systems like macOS, iOS, iPadOS, and visionOS.

[Read](https://en.wikipedia.org/wiki/Spotlight_(Apple)) about it.

Now, Apple Spotlight uses standardized metadata attributes (prefixed with kMDItem) to index and search files, apps, and content, these can be queried using the `mdls` command, something to make note of is, that both xattr and these spotlight attributes are different concepts, so how it works is that a file contains exif, id3 and codec data and then contains xattrs, then spotlight importers reads both and indexes them, so xattrs are filesystem level key-value pairs tacked onto the outside of the file wrapper, the other is directly embedded into the file's data payload.

In the xattr output of the .command file we can see some of these attributes aswell:


```
pineapple@macbook Downloads % xattr -l StockPulse_Installer.command    
com.apple.lastuseddate#PS: ?}?j
com.apple.metadata:kMDItemDownloadedDate: bplist00?3A?9Iv??

com.apple.metadata:kMDItemWhereFroms: bplist00?_;http://stockpulse-analytics.io/StockPulse_Installer.command_http://stockpulse-analytics.io/
                                                             I
com.apple.quarantine: 0081;6accb9ff;Safari;02E0E154-CAE3-4149-B1AD-285BD00E5B0C
pineapple@macbook Downloads % 
```

`com.apple.metadata:kMDItemDownloadedDate`, this is what we're looking for but its not really readable, so we can directly query for it using mdls:

```
pineapple@macbook Downloads % mdls -name kMDItemDownloadedDate StockPulse_Installer.command                                            
kMDItemDownloadedDate = (
    "2026-10-04 13:54:14 +0000"
)
pineapple@macbook Downloads % 
```

And we get the exact same timestamp directly in UTC, same as before confirms that both paths work.

The next question was _What application was used to perform the download?_, again there's two ways to get this, either directly from the xattr, it says `Safari`, as from the output above, or we can look at the LSQuarantineAgentName in the quarantine events db, which says `Safari`, so that becomes answer to question 6.

Similarly question 7: _What is the UUID of the executed file?_, can be answered using the field `LSQuarantineEventIdentifier` from the db, for the identified download, the answer being: `A63D1D95-5072-49D5-9515-AEC2E3A5D187`, now there's a catch in this how would one identify if its the same file that got executed?

Here is where LaunchAgents come in, a launch agent is created when the file is executed or run, so in the LaunchAgents we can see `com.stockpulse.helper.plist`, which is again just a plist file, that is how we confirm that both the executed and downloaded file were in fact the same.

### Stage 3
Now for question no. 8 _What is the label of the persistence mechanism used?_, we can answer this question by looking at the launch agent created on execution:

```
pineapple@macbook LaunchAgents % plutil -p com.stockpulse.helper.plist    
{
  "Label" => "com.stockpulse.helper"
  "ProgramArguments" => [
    0 => "/Users/raahat.khan/Downloads/StockPulse_Installer.command"
  ]
  "RunAtLoad" => 1
}
pineapple@macbook LaunchAgents % 
```

Label of the persistence mechanism: `com.stockpulse.helper`, the next question: _What command/path does this persistence mechanism execute?_, can be answered using the "ProgramArguments" field of the plist file the path was:

```
/Users/raahat.khan/Downloads/StockPulse_Installer.command
```
Persistence is a full fledged forensic analysis and fs concept, read about it [here](https://gruve.ai/in/ai-security-essentials/persistence-mechanisms/)

For the final question i.e the 10th question: _What is the name of a file whose download was started but never completed, and when was the download initiated. (Format:<filename>/YYYY-MM-DD HH:MM:SS)_, is something we've already touched at the beginning, about the .download folder which was created, it gets created when a download gets interrupted as mentioned before, so the file name for that was: `StockMonitor_Setup.dmg`, and the initiation time can be checked in the plist file:

```
pineapple@macbook StockMonitor_Setup.dmg.download % plutil -p Info.plist
{
  "DownloadEntryDateAddedKey" => 2026-10-05 04:01:38 +0000
  "DownloadEntryErrorCodeDictionaryKey" => -999
  "DownloadEntryErrorDomainDictionaryKey" => "NSURLErrorDomain"
  "DownloadEntryIdentifier" => "8F75C2C3-E0A4-4780-88F1-D6420FF3DAD4"
  "DownloadEntryPath" => "/Users/raahat.khan/Downloads/StockMonitor_Setup.dmg.download/StockMonitor_Setup.dmg"
  "DownloadEntryProfileUUIDStringKey" => "DefaultProfile"
  "DownloadEntryProgressBytesSoFar" => 6160384
  "DownloadEntryProgressTotalToLoad" => 52428800
  "DownloadEntryRemoveWhenDoneKey" => 0
  "DownloadEntrySandboxIdentifier" => "05297175-4752-4061-AA1F-DF9EF065C201"
  "DownloadEntryShouldUseRequestURLAsOriginURLIfNecessaryKey" => 0
  "DownloadEntryURL" => "http://stockmonitor-pro.io/StockMonitor_Setup.dmg"
}
pineapple@macbook StockMonitor_Setup.dmg.download % 

```

The field "DownloadEntryDateAddedKey", gives the timestamp, so the final answer being `StockMonitor_Setup.dmg/2026-10-05 04:01:38`.

After submitting this we get the final flag: `labyrinth{why_d035_n0_0n3_d0_m4c05_df1r}`
