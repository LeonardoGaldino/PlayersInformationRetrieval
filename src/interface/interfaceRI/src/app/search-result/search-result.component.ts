import { Component, OnInit } from '@angular/core';
import { RiServiceService } from '../ri-service.service';
import { DataService } from '../data.service';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css']
})
export class SearchResultComponent implements OnInit {

  constructor(private riService:RiServiceService, private dataService: DataService) { }

  ngOnInit() {
    /*this.riService.getHTMLForSearch("hello").subscribe(resp=>{
      document.getElementById("toFill").innerHTML = resp;
    })*/
    var queryParams = this.dataService.getQuery();
    this.dataService.clearQuery();
    console.log(this.riService.testHTMLForSearch("hello"));
    document.getElementById("toFill").innerHTML = this.riService.testHTMLForSearch("hello");
  }

}
