This is a sample python flask API that stores requests in a database.

Build:
	docker build -t anagram-maker .

Run:
	docker run -p 5000:5000 anagram-maker

Build&Run(docker-compose) - recommended:
starts also a database container 
    docker-compse up -d


Environment:
set environment variables in docker-compose file

How to use API:
    
Create anagram from word:
	curl localhost:5000/create?word=myword

Get random anagram:
    curl localhost:5000/get

check if word belongs to anagram:
    curl "localhost:5000/check?word=myword&anagram=yrdwom"
you need to use quotation marks, otherwise curl will cut everything after '&'
