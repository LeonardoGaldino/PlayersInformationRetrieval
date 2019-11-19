import { Component, OnInit } from '@angular/core';
import { RiServiceService } from '../ri-service.service';
import { DataService } from '../data.service';
import { Router, Data } from '@angular/router';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css']
})
export class SearchResultComponent implements OnInit {

  constructor(private router: Router,private riService:RiServiceService, private dataService: DataService) { }

  ngOnInit() {
    //this.dataService.storeQuery(localStorage.getItem('queryParam'));
    //console.log(JSON.parse(localStorage.getItem('queryParam')))
    var queryParams = JSON.parse(localStorage.getItem('queryParam'));
    //var queryParams = this.dataService.getQuery();
    this.riService.getHTMLForSearch(queryParams).subscribe(resp=>{
      if(resp.obj._body=="")document.getElementById("toFill").innerHTML = "<span>nenhum resultado</span>";
      else document.getElementById("toFill").innerHTML = resp.obj._body;
    },error=>{
      document.getElementById("toFill").innerHTML = "<span>Erro</span>";
    })
    //console.log(this.riService.testHTMLForSearch("hello"));
    //document.getElementById("toFill").innerHTML = this.riService.testHTMLForSearch("hello");
  }

  goBack(){
    this.router.navigate(['/']);
  }

}
