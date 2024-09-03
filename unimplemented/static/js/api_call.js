function obter_info() {
             
    el = document.getElementById('etdinfo');

    fetch('/api/obter_informacao_estudante')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao obter os dados da API');
            }
            return response.json();
        })
        .then(data => {
            for ( let linha of data ) {
                el.innerHTML += linha.nome;    
                el.innerHTML += '<br>';    
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}

obter_info()
