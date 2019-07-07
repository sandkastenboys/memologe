# Memologe
Meme Bot for Discord and Telegram

[![Build Status](https://img.shields.io/travis/sandkastenboys/memologe.svg?maxAge=1200)](https://travis-ci.org/sandkastenboys/memologe)

## Add bot to your Group / Discord Server

Coming Soon ...

## Setup

This is a server application so it only runs on linux.

```sybase
$ git clone https://github.com/sandkastenboys/memologe.git
```
Via [Docker](https://hub.docker.com/r/einspaten/memologe)

```sybase
$ cd Memologe
$ nano docker-compose.yml //enter your tokens and configure the bot
$ ./start.sh
```

## Features

#### Commands
    
  !Warning! in Telegram "/" replaces your command key ($).  
    
  - **$post <link> <tags>**         
  seperate multiple tags with ';'
  - **$random <how_many = 1>**         
  posts random meme
  - **$category <id> <tags>**           
  adds these tags to the meme so that it can be found more easily
  - **$search <tag> <how_many = 1>**     
  searches memes based on tag
  - **$size**                            
  amount of memes in the db
  - **$info <id>**                       
  returns relevant information about the meme with this id
  - **$posters**                         
  returns list of most active users of this bot
  - **$tags**                            
  returns all tags in the database
  - **$idtomeme <id>**
  returns meme with this id
 
You also can rate memes by pressing downVote / UpVote or the corresponding arrow emoji.

This bot allows you too download your memes and save it an e.g an external hard drive.

## Bug Reports

Create an [ISSUE](https://github.com/sandkastenboys/memologe/issues/new?assignees=&labels=bug&template=bug_report.md&title=)
