import { Component, OnInit } from '@angular/core';
import { Router, Data } from '@angular/router';
import { DataService } from '../data.service';

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
  //idadeConsulta="";
  posicaoConsulta="";
  nacionalidadeConsulta="";
  numeroConsulta="";
  equipeConsulta="";
  pernaChuteConsulta="";
  pesquisaGenerica="";

  onSubmit(){
    var queryParams = "";
    if(this.pesquisaGenerica.trim()==""){
      if(this.nomeConsulta.trim()!="")queryParams+="name="+this.nomeConsulta;
      //if(this.idadeConsulta.trim()!="")queryParams+="&age="+this.idadeConsulta;
      if(this.posicaoConsulta.trim()!="")queryParams+="&position="+this.posicaoConsulta;
      if(this.nacionalidadeConsulta.trim()!="")queryParams+="&nacionality="+this.nacionalidadeConsulta;
      if(this.numeroConsulta.trim()!="")queryParams+="&number="+this.numeroConsulta;
      if(this.equipeConsulta.trim()!="")queryParams+="&team="+this.equipeConsulta;
      if(this.pernaChuteConsulta.trim()!="")queryParams+="&leg="+this.pernaChuteConsulta; 
      if(queryParams.startsWith("&"))queryParams = queryParams.substr(1,queryParams.length);
    }
    else{
      queryParams+="term="+this.pesquisaGenerica;
    }
    this.dataService.storeQuery(queryParams);
    this.router.navigate(['/search']);
  }

}
