# Memologe
Meme Bot for Discord and Telegram

![Travis](https://api.travis-ci.com/SpartanerSpaten/Memologe.svg?branch=master)

## Add bot to your Group / Discord Server

Coming Soon ...

## Setup

This is a server application so it only runs on linux.

```sybase
$ git clone https://github.com/SpartanerSpaten/Memologe.git
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
    
  - **$post_meme <link> <tags>**         
  seperate multiple tags with ';'
  - **$ran_meme <how_many = 1>**         
  posts random meme
  - **$cate_meme <id> <tags>**           
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
  - **$id2meme <id>**
  returns meme with this id
 
You also can rate memes by pressing downVote / UpVote or the corresponding arrow emoji.

This bot allows you too download your memes and save it an e.g an external hard drive.

## Bug Reports

Create an [ISSUE](https://github.com/SpartanerSpaten/Memologe/issues/new?assignees=&labels=bug&template=bug_report.md&title=)
