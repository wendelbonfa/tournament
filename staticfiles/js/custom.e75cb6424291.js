
function close_modal(obj) {
  $('#msgs').modal('hide')
  window.location.href = obj.baseURI;
}  

function edit_athele(obj, athele_id) {
  if (obj.value == "Remover") {
      $.ajax({
          type: 'POST',
          url: "/remove/",
          data: {
              delete: true,
              athleta: athele_id,
              csrfmiddlewaretoken: csrf_token,
          },
          success: function (json) {
              var message = JSON.parse(json);
              document.getElementById('msg_dialog').innerText = message['msg']
              $('#msgs').modal('show');
          },
      })
  }else{
      document.getElementById('name').value = document.getElementById('name_'+athele_id).innerText;
      document.getElementById('weight').value = document.getElementById('weight_'+athele_id).innerText;
      document.getElementById('rg').value = document.getElementById('rg_'+athele_id).innerText;
      document.getElementById('cpf').value = document.getElementById('cpf_'+athele_id).innerText;      
      var day = document.getElementById('age_'+athele_id).innerText.split("/")[0]
      var month = document.getElementById('age_'+athele_id).innerText.split("/")[1]
      var year = document.getElementById('age_'+athele_id).innerText.split("/")[2]
      document.getElementById('birth_date').value = year + "-"+ month + "-"+ day;
      try {
        document.getElementById('resp_name_gp').value = document.getElementById('resp_name_'+athele_id).innerText;
        document.getElementById('resp_rg_gp').value = document.getElementById('resp_rg_'+athele_id).innerText;
        document.getElementById('resp_cpf_gp').value = document.getElementById('resp_cpf_'+athele_id).innerText;      
      } catch (error) {}         
      var day = document.getElementById('issue_date_'+athele_id).innerText.split("/")[0]
      var month = document.getElementById('issue_date_'+athele_id).innerText.split("/")[1]
      var year = document.getElementById('issue_date_'+athele_id).innerText.split("/")[2]
      document.getElementById('issue_date').value = year + "-"+ month + "-"+ day;                
      var select_gender = document.getElementById('gender_'+athele_id).innerText;  
      var genders = document.getElementById('gender');
      for(var i=0; i<genders.options.length; i++) {
        if ( genders.options[i].text == select_gender ) {
          genders.selectedIndex = i;
          break;
        }
      }
  }
}

function edit_representative(obj, representative_id) {
    if (obj.value == "Remover") {
        $.ajax({
            type: 'POST',
            url: "/remove/",
            data: {
                delete: true,
                representative_id: representative_id,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function (json) {
                var message = JSON.parse(json);
                document.getElementById('msg_dialog').innerText = message['msg']
                $('#msgs').modal('show');
            },
        })

    }else{
        document.getElementById('rep_name').value = document.getElementById('name_'+representative_id).innerText;
        document.getElementById('rep_cpf').value = document.getElementById('cpf_'+representative_id).innerText;
        document.getElementById('rep_celphone').value = document.getElementById('celphone_'+representative_id).innerText;
    }
  }

function load_categories() {
    department = document.getElementById('department').value;
    $.ajax({
        type: 'POST',
        url: "/load_categories/",
        data: {
            department: department,
            csrfmiddlewaretoken: csrf_token,
        },
        success: function (json) {
            var categories = JSON.parse(json);
            new_checkbox = document.getElementById('checkboxes');
            new_checkbox.innerHTML = "";
            for(var i=0; i<categories.length; i++) {                 
                const new_input = document.createElement("input");
                new_input.type = "checkbox"; 
                new_input.setAttribute("class", 'checkbox');
                new_input.setAttribute("name", 'categories');
                new_input.id = categories[i].pk;
                new_input.value = categories[i].pk;
                const new_label = document.createElement("label");
                new_label.for = categories[i].pk;
                new_label.textContent = categories[i].fields.name;
                new_checkbox.appendChild(new_input);
                new_checkbox.appendChild(new_label);
            }
        },
    })
}

function load_categories_prize_draw() {
    department = document.getElementById('department').value;
    new_table = document.getElementById('table_groups'); 
    new_table.innerHTML = "";  
    $.ajax({
        type: 'POST',
        url: "/load_categories/",
        data: {
            department: department,
            csrfmiddlewaretoken: csrf_token,
        },
        success: function (json) {
            var categories = JSON.parse(json);
            select = document.getElementById('category');
            select.innerHTML = "";
            for(var i=0; i<categories.length; i++) {                
                const new_option = document.createElement("option");
                new_option.value = categories[i].pk;
                new_option.innerHTML = categories[i].fields.name;            
                select.appendChild(new_option);            
            }
        },
    })
}

function clear_prize_draw() {
    new_table = document.getElementById('table_groups'); 
    new_table.innerHTML = "";  
}

function recreategroups(categories, athletes, groupschampionship, athletes_) {
    select = document.getElementById('category');
    select.innerHTML = "";
    for(var i=0; i<categories.length; i++) {                
        const new_option = document.createElement("option");
        new_option.value = categories[i].pk;
        new_option.innerHTML = categories[i].fields.name;            
        select.appendChild(new_option);            
    }
    new_checkbox = document.getElementById('checkboxes');
    new_checkbox.innerHTML = "";
    for(var i=0; i<athletes.length; i++) {  
        const new_div = document.createElement("div");
        new_div.style = "display: inline-block;";
        const new_input = document.createElement("input");
        new_input.type = "checkbox"; 
        new_input.setAttribute("class", 'checkbox');
        new_input.setAttribute("name", 'athletes');
        new_input.id = athletes[i].pk;
        new_input.value = athletes[i].pk;
        const new_label = document.createElement("label");
        new_label.for = athletes[i].pk;
        new_label.textContent = athletes[i].fields.name;
        new_checkbox.appendChild(new_div);
        new_checkbox.appendChild(new_input);
        new_checkbox.appendChild(new_label);
    } 
    new_table = document.getElementById('table_groups'); 
    new_table.innerHTML = "";
    new_tbody = document.createElement('tbody'); 
    new_table.appendChild(new_tbody);
    var tr = document.createElement('tr');
    for (var i = 0; i < 2; i++) {
      var th = document.createElement('th');
      if (i == 0)
      {
          th.textContent = 'Grupos';  
      }else{
          th.textContent = 'Atletas';
      }         
      tr.appendChild(th);  
    } 
    new_tbody.appendChild(tr);
    for(var i=0; i<groupschampionship.length; i++) {
        var tr = document.createElement("tr");
        for (var x = 0; x < 2; x++) {
            var td = document.createElement('td');
            if (x == 0)
            {
                td.textContent = groupschampionship[i].fields.name; 
            }else{
                for(var y=0; y<groupschampionship[i].fields.athletes.length; y++) {
                    for(var a=0; a<athletes_.length; a++) {
                        if (groupschampionship[i].fields.athletes[y] == athletes_[a].pk)
                        {
                            p = document.createElement("p");
                            p.textContent = athletes_[a].fields.name;
                            td.appendChild(p);
                        }
                    }
                }
            }
            tr.appendChild(td);
        }  
        new_tbody.appendChild(tr);
    }   
}

function load_categories_grous() {
    department = document.getElementById('department').value;
    $.ajax({
        type: 'POST',
        url: "/load_groups/",
        data: {
            department: department,
            csrfmiddlewaretoken: csrf_token,
            change: "department"
        },
        success: function (json) {
            var categories = JSON.parse(JSON.parse(json)['categories']);
            var athletes = JSON.parse(JSON.parse(json)['athletes']);
            var groupschampionship = JSON.parse(JSON.parse(json)['groupschampionship']);
            var athletes_ = JSON.parse(JSON.parse(json)['athletes_']);
            recreategroups(categories, athletes, groupschampionship, athletes_);
        },
    })
}

function load_athletes_groups() {
    department = document.getElementById('department').value;
    category = document.getElementById('category').value;    
    $.ajax({
        type: 'POST',
        url: "/load_groups/",
        data: {
            department: department,
            category: category,
            csrfmiddlewaretoken: csrf_token,
            change: "category"
        },
        success: function (json) {
            var categories = JSON.parse(JSON.parse(json)['categories']);
            var athletes = JSON.parse(JSON.parse(json)['athletes']);
            var groupschampionship = JSON.parse(JSON.parse(json)['groupschampionship']);
            var athletes_ = JSON.parse(JSON.parse(json)['athletes_']);          
            recreategroups(categories, athletes, groupschampionship, athletes_);
        },
    })
}

function prize_draw() {
    $.ajax({
        type: 'POST',
        url: "/prize_draw/",
        data: {
            championship: document.getElementById("championship").value,
            category: document.getElementById("category").value,
            gender: document.getElementById("gender").value,
            csrfmiddlewaretoken: csrf_token
        },
        success: function (json) {
          var mensagem = JSON.parse(json)['csv_list'];
          new_table = document.getElementById('table_groups'); 
          new_table.innerHTML = "";
          new_tbody = document.createElement('tbody'); 
          new_table.appendChild(new_tbody);
          var tr = document.createElement('tr');
          let titles = ['Ordem', 'Inscrição', 'Nome', 'Academia'];
          for (var i = 0; i < titles.length; i++) {
            var th = document.createElement('th');
            th.textContent = titles[i];        
            tr.appendChild(th);  
          } 
          new_tbody.appendChild(tr);
          
          for(var i = 1; i < (Object.keys(mensagem).length+1); i++) {
              var tr = document.createElement("tr");
              var position = mensagem[i];
              var td = document.createElement('td');
              td.textContent = String(i).padStart(2, '0'); 
              tr.appendChild(td);            
              for (var x = 0; x < position.length; x++) {
                  var td = document.createElement('td');
                  td.textContent = mensagem[i][x]; 
                  tr.appendChild(td);
              }  
              new_tbody.appendChild(tr);
          }      
        },
    })
}    

function grades() {
    $.ajax({
        type: 'POST',
        url: "/grades/",
        data: {
            championship: document.getElementById("championship").value,
            category: document.getElementById("category").value,
            gender: document.getElementById("gender").value,
            csrfmiddlewaretoken: csrf_token
        },
            success: function (json) {
            var mensagem = JSON.parse(json)
            new_table = document.getElementById('table_groups'); 
            new_table.innerHTML = "";
            new_tbody = document.createElement('tbody'); 
            new_table.appendChild(new_tbody);
            var tr = document.createElement('tr');
            let titles = ['Ordem', 'Inscrição', 'Nome', 'Academia', 'Estilo/Sistema', 'Notas'];
            let subtitles = ['FUNDAMENTOS', 'DESEMPENHO'];
            for (var i = 0; i < titles.length; i++) {
              var th = document.createElement('th');
              th.textContent = titles[i];        
              if (i == 5){
                  th.colSpan ="2"; 
                  th.style="text-align:center";
              }else{
                  th.rowSpan ="2";
                  th.valign="middle";
              }
              tr.appendChild(th);  
            } 
            new_tbody.appendChild(tr);
            var tr = document.createElement('tr');
            for(var y = 0; y < subtitles.length; y++) {
                var th = document.createElement('th');
                th.textContent = subtitles[y];  
                tr.appendChild(th);
            }
            new_tbody.appendChild(tr);
            for(var i = 0; i < (mensagem.length); i++) {
              var tr = document.createElement("tr");
              var position = mensagem[i];           
              for (var x = 0; x < position.length; x++) {
                  var td = document.createElement('td');
                  if (x == 0){
                      td.textContent = String(mensagem[i][x]).padStart(2, '0'); 
                  } else if (x == 1) {
                      td.textContent = String(mensagem[i][x]).padStart(5, '0');   
                  }else{
                      td.textContent = mensagem[i][x]; 
                  }
                  tr.appendChild(td);
              }  
              var td = document.createElement('td'); 
              var input = document.createElement('input'); 
              input.type="number";
              input.placeholder="0";
              input.min="0";
              input.step="0.01";
              td.appendChild(input);
              tr.appendChild(td); 
              var td = document.createElement('td');              
              var input = document.createElement('input'); 
              input.type="number";
              input.placeholder="0";
              input.min="0";
              input.step="0.01";
              td.appendChild(input);            
              tr.appendChild(td);              
              new_tbody.appendChild(tr);
          }                    
        },
    })
}  

function deductions() {
    $.ajax({
        type: 'POST',
        url: "/deductions/",
        data: {
            championship: document.getElementById("championship").value,
            category: document.getElementById("category").value,
            gender: document.getElementById("gender").value,
            csrfmiddlewaretoken: csrf_token
        },
            success: function (json) {
            var mensagem = JSON.parse(json)
            var orders = JSON.parse(mensagem['orders'])
            var deductions = JSON.parse(mensagem['deductions'])
            new_table = document.getElementById('table_groups'); 
            new_table.innerHTML = "";
            new_tbody = document.createElement('tbody'); 
            new_table.appendChild(new_tbody);
            var tr = document.createElement('tr');
            let titles = ['Ordem', 'Inscrição', 'Nome', 'Academia', 'Estilo/Sistema', 'Adicionar', 'Notas', 'Enviar'];
            for (var i = 0; i < titles.length; i++) {
              var th = document.createElement('th');
              th.textContent = titles[i];        
              tr.appendChild(th);  
            } 
            new_tbody.appendChild(tr);
            for(var i = 0; i < (orders.length); i++) {
              var tr = document.createElement("tr");
              var position = orders[i];           
              for (var x = 0; x < position.length; x++) {
                  var td = document.createElement('td');
                  if (x == 0){
                      td.textContent = String(orders[i][x]).padStart(2, '0'); 
                  } else if (x == 1) {
                      td.textContent = String(orders[i][x]).padStart(5, '0');   
                  }else{
                      td.textContent = orders[i][x]; 
                  }
                  tr.appendChild(td);
              }  
              var td = document.createElement('td'); 
              for(var y = 0; y < (deductions.length); y++) {              
                  var button = document.createElement('button'); 
                  button.textContent = "+";
                  button.id = orders[i][2];
                  button.title = deductions[y].fields['handwriting'];
                  button.name=deductions[y].fields['grade'];
                  button.addEventListener('click', function() {
                      score(this);
                  });
                  button.style = "margin-right: 10px; width: 25px";
                  td.appendChild(button);
                  var p = document.createElement('p'); 
                  p.textContent = deductions[y].fields['handwriting'];
                  p.style.display = "inline-flex";
                  td.appendChild(p); 
                  var button = document.createElement('button'); 
                  button.textContent = "-";
                  button.id = orders[i][2];
                  button.title = deductions[y].fields['handwriting'];
                  button.name=deductions[y].fields['grade'];
                  button.addEventListener('click', function() {
                      subtractionscore(this);
                  });
                  button.style = "margin-left: 10px; width: 25px";                
                  td.appendChild(button);
                  var br = document.createElement('br');
                  td.appendChild(br);
              }              
              tr.appendChild(td); 
              var td = document.createElement('td');              
              var input = document.createElement('input'); 
              input.type="number";
              input.id = "input_"+orders[i][2];
              input.placeholder="0";
              input.min="0";
              input.disabled = true;
              input.step="0.01";
              input.value="0";
              td.appendChild(input); 
              var br = document.createElement('br');
              td.appendChild(br);                     
              for(var y = 0; y < (deductions.length); y++) {   
                  var p = document.createElement('p');
                  p.id = "p_"+deductions[y].fields['handwriting']+"_"+orders[i][2];
                  p.textContent = p.textContent + deductions[y].fields['handwriting'] + " ";
                  p.style = "display: inline-flex; padding-right: 3px;";
                  td.appendChild(p); 
              }                 
              tr.appendChild(td);     
              var td = document.createElement('td'); 
              var button = document.createElement('button'); 
              button.textContent = "Enviar Notas";
              button.id = orders[i][2];              
              button.addEventListener('click', function() {
                  sendscore(this);
              });            
              td.appendChild(button);              
              tr.appendChild(td);   
              new_tbody.appendChild(tr);
          }                    
        },
    })
} 

function score(obj) {
  var p = document.getElementById("p_"+obj.title+"_"+obj.id);
  var newtext = "";
  if (p.textContent.split("x").length == 1) {
      newtext = "1x" + obj.title;     
  }else{
      var sum = parseFloat(p.textContent.split("x")[0]) + 1;
      newtext = sum + "x" + p.textContent.split("x")[1];
  }  
  p.textContent = newtext;
  var calculo = parseFloat(document.getElementById("input_"+obj.id).value) + parseFloat(obj.name);    
  document.getElementById("input_"+obj.id).value = calculo.toFixed(2);    
}

function subtractionscore(obj) {
  var p = document.getElementById("p_"+obj.title+"_"+obj.id);
  var newtext = "";
  if (p.textContent.split("x").length == 1) {
      newtext = obj.title;
  }else{
      var calculo = parseFloat(document.getElementById("input_"+obj.id).value) - parseFloat(obj.name);    
      document.getElementById("input_"+obj.id).value = calculo.toFixed(2);            
      var sub = parseFloat(p.textContent.split("x")[0]) - 1;
      if (sub == 0) {
        newtext = obj.title;
      }else{
        newtext = sub + "x" + p.textContent.split("x")[1];      
      }
  }  
  p.textContent = newtext; 

  
}


function summaries() {
    $.ajax({
        type: 'POST',
        url: "/summaries/",
        data: {
            championship: document.getElementById("championship").value,
            category: document.getElementById("category").value,
            gender: document.getElementById("gender").value,
            csrfmiddlewaretoken: csrf_token
        },
            success: function (json) {
            var mensagem = JSON.parse(json)
            new_table = document.getElementById('table_groups'); 
            new_table.innerHTML = "";
            new_tbody = document.createElement('tbody'); 
            new_table.appendChild(new_tbody);
            var tr = document.createElement('tr');
            let titles = ['Ordem', 'Inscrição', 'Nome', 'Academia', 'Estilo/Sistema', 'FUNDAMENTOS', 'DESEMPENHO', 'Deduções', 'Nota Final', 'Desenpate'];
            let subtitles = ['Nota 1', 'Nota 2', 'Nota 3', 'Média', 'Nota 1', 'Nota 2', 'Nota 3', 'Média', '1°', '2°', '3°'];
            for (var i = 0; i < titles.length; i++) {
              var th = document.createElement('th');
              th.textContent = titles[i];        
              if ((i == 5) || (i == 6)) {
                  th.colSpan ="4"; 
                  th.style="text-align:center";
              }else{
                  if (i == 9){
                    th.colSpan ="3"; 
                    th.style="text-align:center";                    
                  }else{
                    th.rowSpan ="2";
                    th.valign="middle";
                  }                  
              }
              tr.appendChild(th);  
            } 
            new_tbody.appendChild(tr);
            var tr = document.createElement('tr');
            for(var y = 0; y < subtitles.length; y++) {
                var th = document.createElement('th');
                th.textContent = subtitles[y];  
                tr.appendChild(th);
            }
            new_tbody.appendChild(tr);
            for(var i = 0; i < (mensagem.length); i++) {
              var tr = document.createElement("tr");
              var position = mensagem[i];           
              for (var x = 0; x < position.length; x++) {
                  var td = document.createElement('td');
                  if (x == 0){
                      td.textContent = String(mensagem[i][x]).padStart(2, '0'); 
                  } else if (x == 1) {
                      td.textContent = String(mensagem[i][x]).padStart(5, '0');   
                  }else{
                      td.textContent = mensagem[i][x]; 
                  }
                  tr.appendChild(td);
              }           
              for (var x = 0; x < 13; x++) {
                  var td = document.createElement('td'); 
                  var input = document.createElement('input'); 
                  input.type="number";
                  input.placeholder="0";
                  input.min="0";
                  input.style.width="50px";
                  input.step="0.01";
                  td.appendChild(input);
                  tr.appendChild(td);  
              }    
              
              new_tbody.appendChild(tr);
          }                    
        },
    })
}  


function check_age(date) {
    var birth_year = parseInt(date.value.split("-")[0])
    var birth_month = parseInt(date.value.split("-")[1])
    var currentdate = new Date();
    var corrent_year = currentdate.getFullYear();
    var corrent_month = currentdate.getMonth()+1;
    amount_month = corrent_month - birth_month;
    if (amount_month < 0){
        amount_month = amount_month *-1
    }
    amount_years = corrent_year - birth_year
    if (amount_years == 18){
        if(amount_month < 12){
            document.getElementById("resp_name_gp").style.display = "block";
            document.getElementById("resp_rg_gp").style.display = "block";
            document.getElementById("resp_rg_file_gp").style.display = "block";
            document.getElementById("resp_cpf_gp").style.display = "block";
            document.getElementById("resp_cpf_file_gp").style.display = "block";        
        }else{
            document.getElementById("resp_name_gp").style.display = "none";
            document.getElementById("resp_rg_gp").style.display = "none";
            document.getElementById("resp_rg_file_gp").style.display = "none";
            document.getElementById("resp_cpf_gp").style.display = "none";
            document.getElementById("resp_cpf_file_gp").style.display = "none";
        }
    }
    if (amount_years < 18){
        document.getElementById("resp_name_gp").style.display = "block";
        document.getElementById("resp_rg_gp").style.display = "block";
        document.getElementById("resp_rg_file_gp").style.display = "block";
        document.getElementById("resp_cpf_gp").style.display = "block";
        document.getElementById("resp_cpf_file_gp").style.display = "block"; 
    }
    if (amount_years > 18){
        document.getElementById("resp_name_gp").style.display = "none";
        document.getElementById("resp_rg_gp").style.display = "none";
        document.getElementById("resp_rg_file_gp").style.display = "none";
        document.getElementById("resp_cpf_gp").style.display = "none";
        document.getElementById("resp_cpf_file_gp").style.display = "none";        
    }


}