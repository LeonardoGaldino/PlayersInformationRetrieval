import { Component, OnInit } from '@angular/core';
import { Router, Data } from '@angular/router';
import { DataService } from '../data.service';
import { query } from '@angular/core/src/render3/query';

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
    //this.dataService.clearQuery()
    //localStorage.removeItem('queryParam');
    var queryParams = "";
    var qp:any = {}
    if(this.pesquisaGenerica.trim()==""){
      if(this.nomeConsulta!="")qp.name = this.nomeConsulta;
      //if(this.idadeConsulta!="")qp.age = this.idadeConsulta;
      if(this.posicaoConsulta!="")qp.position = this.posicaoConsulta;
      if(this.nacionalidadeConsulta!="")qp.nacionality = this.nacionalidadeConsulta;
      if(this.numeroConsulta!="")qp.number = this.numeroConsulta;
      if(this.equipeConsulta!="")qp.team = this.equipeConsulta;
      if(this.pernaChuteConsulta!="")qp.leg = this.pernaChuteConsulta;
    }
    else{
      if(this.pesquisaGenerica!="")qp.term = this.pesquisaGenerica;
    }

    Object.keys(qp).forEach(key=>{
      if(queryParams!="")queryParams+="&";
      queryParams +=key+"="+qp[key] ;
    })
    //this.dataService.storeQuery("?"+queryParams);
    localStorage.setItem('queryParam', JSON.stringify("?"+queryParams));
    this.router.navigate(['/search'],{
        queryParams:qp
      }
    );
  }

}
