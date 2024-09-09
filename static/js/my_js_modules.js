my_element_disposer = {
  // pressupõe o uso de Tailwind CSS
  dispor_elementos_horizontalmente_com_largura_fixa: function(elementos){
    let imgz = '<div class="flex flex-wrap">'
    data.op.forEach(element => {
        imgz += `<img width=300 class='mt-2 mr-2' src='img/${element}'>`
    });
    imgz += '</div>'
    return imgz
  }
}



my_array_handlers = {
  subarray_aleatório: function (array, quantidade_elementos_a_ser_selecionada) {
    if (quantidade_elementos_a_ser_selecionada >= array.length) {
      return {
        subarray: array,
        array_de_elementos_restantes: []
      };
    }

    const array_de_elementos_restantes = array.slice();
    const subarray = [];
  
    // Extrai elementos aleatoriamente do array até atingir o número desejado
    while (subarray.length < quantidade_elementos_a_ser_selecionada) {
      const idx_aleatorio = Math.floor(Math.random() * array_de_elementos_restantes.length);
      const item_do_array = array_de_elementos_restantes.splice(idx_aleatorio, 1)[0];
      subarray.push(item_do_array);
    }
  
    return {
      subarray,
      array_de_elementos_restantes
    };
  }  
}



my_io = {
  ler_arquivo_json: function (json_file) {
    let rawdata = fs.readFileSync(json_file);
    let jsondata = JSON.parse(rawdata);
    return jsondata;
  },
  
  
  escrever_arquivo_json: function (json_file, data) {
    let data_pretty = JSON.stringify(data, null, 4);
    fs.writeFile(json_file, data_pretty, finished);
    function finished(err) {
      if (err) { throw err;}
    }
  }  
}




my_random = {
  criar_string_randomica: function (tamanho) {
    let resultado = '';
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let counter = 0;
    while (counter < tamanho) {
      resultado += caracteres.charAt(Math.floor(Math.random() * caracteres.length));
      counter += 1;
    }
    return resultado;
  }
}




my_backend_fetchers = {
  verificar_rota_e_mostrar_resultado_como_string: function(rota_de_verificação, container_de_exposição) {
    elemento_container = document.getElementById(container_de_exposição);
    
    fetch(rota_de_verificação)
      .then(r => r.json())
      .then(data => {
          if (data.op != undefined) {
              if (data.op instanceof Array) {
                elemento_container.innerHTML = my_element_disposer.dispor_elementos_horizontalmente_com_largura_fixa(array_de_elementos);
              } else {
                elemento_container.innerHTML = "<div class='items-center align-middle text-center flex-grow'><p>Aguardando envio dos elementos...</p></div>";
              }
          }
    })  
  },

  verificar_rota_e_obter_elementos: (rota_de_verificação, objeto_receptor) => {
    fetch(rota_de_verificação)
      .then(r => r.json())
      .then(data => { objeto_receptor = data })
  }

}




my_desk_routines = {
  apresentar_cartas_na_mesa: function() {
    my_backend_fetchers.verificar_rota_e_mostrar_elementos('/info_mesa', 'img_selecionada');
  }
}





my_front_helpers = {
  limpar_campo_texto_ou_similar: function (id_do_elemento) {
    try {
        el = document.getElementById(id_do_elemento);
        if ( el.type == 'text' || el.type == 'date' || el.type == 'number' ) {
            el.value = '';
        }
    } catch {}
  },
 
  limpar_radio_ou_checkbox: function (id_do_elemento) {
    let max_idx = numero_opcoes.get(id_do_elemento)
    let idx = 0;
    while ( idx <= max_idx ) {
        try {
            limpar_campo_opção_radio(`${id_do_elemento}${idx}`);
            idx = idx+1
        } catch { break }
    }
  },
  
  mostrar_elemento: function (id_do_elemento) {
    el = document.getElementById(id_do_elemento);
    el.style.display = 'block';
  },

  esconder_elemento: function (id_do_elemento) {
    el = document.getElementById(id_do_elemento);
    el.style.display = 'none';
  },
  
  rolar_até_o_elemento: function (id_do_elemento) {
    document.getElementById(id_do_elemento).scrollIntoView();
  }
}



