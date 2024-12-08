import PopulateResponseTable from "./PopulateResponseTable.js";

let data = [];
const fields = ["filename", "coordinate", "value", "sheetname", "savepath"];
const tbody = document.getElementById("listItens");
const btnLimpa = document.getElementById("btnClear");
const btnCarrega = document.getElementById("btnLoad");

function addItem() {
    let values = fields.map((element) => document.getElementById(element).value);
    let tr = createTr(values);
    tbody.appendChild(tr);
    clearFields();
    tableLister();
}

function createTr(fields) {
    `fields[0] = filename, fields[1] = coordinate, fields[2] = value, fields[3] = sheetname`
    let newTr = document.createElement("tr"),
        newTdAOption = document.createElement("td");
    
    let tdList = fields.map((element) => {
            let td = document.createElement("td");
            td.textContent = element;
            td.setAttribute("contenteditable", "true");
            return td;
        });

    newTdAOption.innerHTML = '<button type="button" class="btn btn-danger btn-sm" onclick="remItem('+`'${fields[0]}'`+')"><i class="fas fa-minus"></i></button>';
    newTr.setAttribute("id", fields[0]);
    newTr.append(...tdList, newTdAOption);
    return newTr;
}

function tableLister() {
    if (tbody.childElementCount > 0){
        btnCarrega.removeAttribute("hidden");
        btnLimpa.removeAttribute("hidden");
    } else {
        btnCarrega.setAttribute("hidden", "");
        btnLimpa.setAttribute("hidden", "");
    }
}

function cleanTable() {
    tbody.innerHTML = "";
    tableLister();
}

function clearFields() {
    fields.map((element) => {
        document.getElementById(element).value="";
    });
}

function process_form(){
    if (confirm("Confirm to send data?")){
        sendDataLoad();
        cleanTable();
    } else {
        alert("Operations was canceled!");
    }   
}

function addCheck(){
    const filenameCheck = document.getElementById("filename").value
    const aCheck = document.getElementById("coordinate").value;
    const bCheck = document.getElementById("value").value
    if (!filenameCheck || !aCheck || !bCheck){
        alert("Fill all fields!");
    } else {
        addItem();
        }
}

function remItem(filename) {
    document.getElementById(filename).remove();
    let newData = data.filter(objs => objs["filename"] != filename);
    data = newData;
    tableLister();
}

function tableLines(){
    let table = document.getElementById("listItens");
    let rows = table.children;

    for (let i = 0; i < rows.length; i++){
        data.push({"coordinate": rows.item(i).children[1].innerHTML,
                    "filename": rows.item(i).children[0].innerHTML,
                    "value": rows.item(i).children[2].innerHTML});
        if (rows.item(i).children[3].innerHTML){
            data[i]["sheetname"] = rows.item(i).children[3].innerHTML;
        }
        if (rows.item(i).children[4].innerHTML){
            data[i]["savepath"] = rows.item(i).children[4].innerHTML;
        }
    }
}

function showLoaderSync(status){
    if (status == 0){
        document.getElementById("loading").setAttribute("hidden", "hidden");}
    else {
        document.getElementById("loading").removeAttribute("hidden");
    }
}

const resetData = () => data = [];

function sendDataLoad() {
    tableLines()
    var jasonOfObjs = JSON.stringify(data);
    showLoaderSync(1);
    console.log(jasonOfObjs);
    $.ajax({
      headers: {
        'dataType': 'jsonp',
        'Access-Control-Allow-Origin': '*',   
      },
      type: "PATCH",
      url: "http://localhost:5000/pyxl/write",
      data: jasonOfObjs,
      contentType: "application/json",
      success: function(data) {
        let titles = ["value", "old_value", "coordinate", "path", "error"]
        let response = new PopulateResponseTable(titles, data, "writeTable", "divWriteResponse");
        response.setDivVisible();
        response.setThead("writeHeadResponse");
        response.setTbody("writeBodyResponse");
        response.populateThead();
        response.populateTbody();
        resetData();
        showLoaderSync(0);
      },error: function(error) {
        console.log(error);
        showLoaderSync(0);
        }
    });
}

window.addItem = addItem;
window.createTr = createTr;
window.clearFields = clearFields;
window.remItem = remItem;
window.tableLister = tableLister;
window.cleanTable = cleanTable;
window.process_form = process_form;
window.addCheck = addCheck;
window.tableLines = tableLines;
window.showLoaderSync = showLoaderSync;
window.sendDataLoad = sendDataLoad;