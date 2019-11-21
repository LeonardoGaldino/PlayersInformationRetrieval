import { Component, OnInit } from '@angular/core';
import { Router, Data } from '@angular/router';
import { DataService } from '../data.service';
import { Utilities } from '../utils';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  focusOnField="";
  namesTopMutualInfo=[];
  positionTopMutualInfo=[];
  nationalityTopMutualInfo=[];
  numberTopMutualInfo=[];
  teamTopMutualInfo=[];
  genericTopMutualInfo=[];
  constructor(private router: Router, private dataService: DataService) { }


  getTopMutualInfo(arr,attr){
    var stopWords = ["de","para","fc","undefined"];
    var attrMapped;
    if(attr=="")attrMapped = arr.filter(o=>stopWords.indexOf(o.value)==-1);
    else attrMapped = arr.filter(o=>o.attr==attr && stopWords.indexOf(o.value)==-1);
    var attrMappedSorted = attrMapped.sort(function(a,b){if(a.freq>b.freq)return -1; else if(b.freq>a.freq)return 1;else return 0})
    return attrMappedSorted.slice(0,3)
  }

  onFocus(field){
    this.focusOnField = field;
  }

  readTextFile(file)
  {
      var that = this;
      var rawFile = new XMLHttpRequest();
      rawFile.open("GET", file, true);
      rawFile.onreadystatechange = function ()
      {
          if(rawFile.readyState === 4)
          {
              if(rawFile.status === 200 || rawFile.status == 0)
              {
                  var allText = rawFile.responseText;
                  var lines = allText.split('\n');
                  var importantFromLines = [];
                  lines.forEach(o=>{
                    importantFromLines.push(o.split(' ')[0]+'//'+o.split(' ')[1]);
                  })
                  var mapped = importantFromLines.map(o=>{return {attr:o.split('//')[0],value:o.split('//')[1],freq:parseInt(o.split('//')[2])}})
                  
                  that.namesTopMutualInfo = that.getTopMutualInfo(mapped,"name"); 
                  that.positionTopMutualInfo = that.getTopMutualInfo(mapped,"position");
                  that.nationalityTopMutualInfo = that.getTopMutualInfo(mapped,"nationality");
                  that.numberTopMutualInfo = that.getTopMutualInfo(mapped,"number");
                  that.teamTopMutualInfo = that.getTopMutualInfo(mapped,"team");
                  that.genericTopMutualInfo = that.getTopMutualInfo(mapped,"");
              }
          }
      }
      rawFile.send(null);
  }
  ngOnInit() {
    this.readTextFile("https://raw.githubusercontent.com/LeonardoGaldino/PlayersInformationRetrieval/master/src/index/freq_index.txt");
  }

  title = 'app';
  opcoesPernaChute=['Right','Left','Both'];
  consulta = "";
  nomeConsulta="";
  posicaoConsulta="";
  nacionalidadeConsulta="";
  numeroConsulta="";
  equipeConsulta="";
  pernaChuteConsulta="";
  pesquisaGenerica="";
  responseSize = 10;
  tfIdf=true;

  toggleClicked() {
    this.tfIdf = !this.tfIdf;
  }

  onSubmit(){
    var queryParams = "";
    var qp:any = {}
    if(this.pesquisaGenerica.trim()==""){
      if(this.nomeConsulta!="")qp.name = this.nomeConsulta;
      if(this.posicaoConsulta!="")qp.position = this.posicaoConsulta;
      if(this.nacionalidadeConsulta!="")qp.nationality = this.nacionalidadeConsulta;
      if(this.numeroConsulta!="")qp.number = this.numeroConsulta;
      if(this.equipeConsulta!="")qp.team = this.equipeConsulta;
      if(this.pernaChuteConsulta!="")qp.foot = this.pernaChuteConsulta;
    }
    else{
      if(this.pesquisaGenerica!="")qp.term = this.pesquisaGenerica;
    }
    qp.tfidf = this.tfIdf ? "1" : "0";
    qp.max_size = this.responseSize
    if(Object.keys(qp).length > 2) {
      this.dataService.storeQuery(Utilities.paramsObjToStr(qp));
      this.router.navigate(['/search'], {queryParams: qp});
    } else {
      alert("Preencha algum campo de consulta.")
    }
  }

}
