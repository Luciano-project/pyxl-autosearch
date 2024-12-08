class PopulateResponseTable {
    constructor(titles, files, table, hiddenDivName){
        this.response_files = files;
        this.titles = titles;
        this.table = table;
        this.tbody = ""
        this.thead = ""
        this.hiddenDivName = hiddenDivName
    }

    setTbody(tbodyId){
        this.tbody = document.getElementById(tbodyId);
        this.tbody.innerHTML="";
    }

    setThead(theadId){
        this.thead = document.getElementById(theadId);
    }

    setDivVisible(){
        document.getElementById(this.hiddenDivName).style.display = "block";
    }

    populateTbody(){
        this.response_files.forEach(element => {
            console.log("check", element);
            let tr = this.createTr();
            for (let i of this.titles) {
                let td = document.createElement("td");
                td.textContent = element[i];
                tr.appendChild(td);
            }
            this.tbody.appendChild(tr);
            return 1;
        });
    }

    isTheadEmpty(){
        if (this.thead.children.length == 0){
            return 1;
        } else {
            return 0;
        }
    }

    populateThead(){
        if (!this.isTheadEmpty()){
            return 0;
        }
        let tr = this.createTr();
        for (let i of this.titles) {
            let th = document.createElement("th");
            th.textContent = i.charAt(0).toUpperCase() + i.slice(1);
            tr.appendChild(th);
        }
        this.thead.appendChild(tr);
        return 1;
    }

    createTr(){
        let tr = document.createElement("tr");
        return tr;
    }
}

export default PopulateResponseTable;