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

  constructor(private router: Router, private dataService: DataService) { }

  ngOnInit() {
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

    this.dataService.storeQuery(Utilities.paramsObjToStr(qp));
    this.router.navigate(['/search'], {queryParams: qp});
  }

}
