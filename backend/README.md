### Build:

    docker build -t anagram-maker .

### Run:

    docker run -p 5000:5000 anagram-maker


### API-cals:
## create anagram:
# single:

    GET: /api/create?word=apfelbaum

# multiple:

    POST: api/create

    body: 
    {
	"words": ["tischbein", "anemone", "verbrechen", "raubkopie"]
    } 
