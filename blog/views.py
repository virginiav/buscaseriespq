from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON


# Create your views here.
def index(request):
    context=(None)
    if request.method =='POST':
        stringbusca = request.POST.get('palavrachave')
        busca = stringbusca
        print(busca)
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
                    PREFIX dbpprop: <http://dbpedia.org/property/>

                    SELECT DISTINCT 
                        ?name 
                        ?numberOfEpisodes
                        ?numberOfSeasons
                        ?abstract 

                    WHERE {
                        ?instance a <http://dbpedia.org/ontology/TelevisionShow>.
                        ?instance foaf:name ?name .
                        FILTER REGEX (?name, '^""" + busca + """$', 'i').

                    
                        ?instance dbpedia-owl:numberOfEpisodes ?numberOfEpisodes .
                        ?instance dbpedia-owl:numberOfSeasons ?numberOfSeasons .
                        ?instance dbpedia-owl:abstract ?abstract .
                        FILTER (LANG(?abstract) = 'pt').
                    }
                    """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)

        context

        try:

            context = {'consult': results['results']['bindings'][0]['name']['value'],
                       'abs': results['results']['bindings'][0]['abstract']['value'],
                       'eps': results['results']['bindings'][0]['numberOfEpisodes']['value'],
                       'temps': results['results']['bindings'][0]['numberOfSeasons']['value'],
                       }
        except:

            erroms = 'Dados não Encontrados!'
            context = {'erromsg': erroms}

    return render(request, 'blog/index.html', context)
