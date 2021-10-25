# Response Team

## Part 1/4

Files :

- [access.log](rt1/access.log)
- [Readme.txt](rt1/Readme.txt)

The log file is quite long... Let's extract only domain names with the shell command:

```
cat access.log | awk -F" " '{print $8}' |  awk -F"/" '{print $3}' | sort | uniq
```

Now there are 143 words to read instead of 2898 lines. We can see `frplab.com:37566` witch is a strange domain. Here are the details :

```
$ cat access.log | grep frplab.com
2021-08-18 09:37:53 221 192.168.42.164 TCP_MISS/200 357 HEAD http://frplab.com:37566/sdhjkzui1782109zkjeznds - HIER_DIRECT/192.93.161.254 application/octet-stream "Microsoft BITS/7.8" "SQUID-CS" 191 -
2021-08-18 09:37:53  35 192.168.42.164 TCP_MISS/200 813 GET http://frplab.com:37566/sdhjkzui1782109zkjeznds - HIER_DIRECT/192.93.161.254 application/octet-stream "Microsoft BITS/7.8" "SQUID-CS" 242 -
```

I guess that's what we are looking for. Let's compute the flag.

```
$ echo http://frplab.com:37566/sdhjkzui1782109zkjeznds | sha256sum
0cb9c24ae4d9d05096a9a837dcd0169e792369dcf48f7da456fda96638f47d18  -
```



## Part 2/4

 ```
 Step2:
 Can we find more information on the download ?
 
 Rules:
 To unlock the step3, you have to identify the name of the job.
 Just use that name (casesensitive) to unlock the step3
 ```

Files :

- [a lot of .evtx files](./Logs/)

I work on Linux so I wanted to find a tool to read these Windows events log files. I found [this Python library](https://github.com/williballenthin/python-evtx). Let's install it:

```
$ pip install python-evtx
```

Now, let's convert every file to a readable format:

```
$ cd Logs
$ for i in *.evtx; do evtx_dump.py $i > xml/$i; done
```

And now we can grep information about the download:

```
$ cd xml
$ grep frplab.com *
Microsoft-Windows-Bits-Client%4Operational.evtx-<EventRecordID>68</EventRecordID>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Correlation ActivityID="{46704613-5f8b-4911-b908-f19d666e51e2}" RelatedActivityID=""></Correlation>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Execution ProcessID="432" ThreadID="5788"></Execution>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Channel>Microsoft-Windows-Bits-Client/Operational</Channel>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Computer>DESKTOP-HVT7JDU</Computer>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Security UserID="S-1-5-18"></Security>
Microsoft-Windows-Bits-Client%4Operational.evtx-</System>
Microsoft-Windows-Bits-Client%4Operational.evtx-<EventData><Data Name="transferId">{46704613-5f8b-4911-b908-f19d666e51e2}</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="name">qsljdsyy19872IFDND172537438eueir</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="Id">{e85da2b3-0ea1-413f-ae2c-294eca2190e3}</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx:<Data Name="url">http://frplab.com:37566/sdhjkzui1782109zkjeznds</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="peer"></Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="fileTime">2021-08-17 14:36:04</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="fileLength">456</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="bytesTotal">456</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="bytesTransferred">0</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="bytesTransferredFromPeer">0</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-</EventData>
Microsoft-Windows-Bits-Client%4Operational.evtx-</Event>
Microsoft-Windows-Bits-Client%4Operational.evtx-
Microsoft-Windows-Bits-Client%4Operational.evtx-<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event"><System><Provider Name="Microsoft-Windows-Bits-Client" Guid="{ef1cc15b-46c1-414e-bb95-e76b077bd51e}"></Provider>
--
Microsoft-Windows-Bits-Client%4Operational.evtx-<EventRecordID>69</EventRecordID>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Correlation ActivityID="{46704613-5f8b-4911-b908-f19d666e51e2}" RelatedActivityID=""></Correlation>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Execution ProcessID="432" ThreadID="4040"></Execution>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Channel>Microsoft-Windows-Bits-Client/Operational</Channel>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Computer>DESKTOP-HVT7JDU</Computer>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Security UserID="S-1-5-18"></Security>
Microsoft-Windows-Bits-Client%4Operational.evtx-</System>
Microsoft-Windows-Bits-Client%4Operational.evtx-<EventData><Data Name="transferId">{46704613-5f8b-4911-b908-f19d666e51e2}</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="name">qsljdsyy19872IFDND172537438eueir</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="Id">{e85da2b3-0ea1-413f-ae2c-294eca2190e3}</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx:<Data Name="url">http://frplab.com:37566/sdhjkzui1782109zkjeznds</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="peer"></Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="hr">0</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="fileTime">2021-08-17 14:36:04</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="fileLength">456</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="bytesTotal">456</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="bytesTransferred">456</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="proxy"></Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="peerProtocolFlags">0</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="bytesTransferredFromPeer">0</Data>
Microsoft-Windows-Bits-Client%4Operational.evtx-<Data Name="AdditionalInfoHr">0</Data>
```

After few tries to unzip the ciphered archive we guess the flag is the event name: `qsljdsyy19872IFDND172537438eueir`.
