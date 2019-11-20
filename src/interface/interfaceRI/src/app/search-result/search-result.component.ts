import { Component, OnInit } from '@angular/core';
import { RiServiceService } from '../ri-service.service';
import { DataService } from '../data.service';
import { Router } from '@angular/router';
import { timeInterval } from 'rxjs/operators';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css']
})
export class SearchResultComponent implements OnInit {

  noResults = false;
  hasErrors = false;
  isLoading = true;
  tfIdf = true;

  constructor(private router: Router,private riService:RiServiceService, private dataService: DataService) {
    let query = dataService.getQuery();
    if(query.indexOf('tfidf=') !== -1) {
      let tfIdfRaw = dataService.getQuery().split('tfidf=')[1][0];
      this.tfIdf = tfIdfRaw == "0" ? false : true;
    }
  }

  toggleClicked(): void {
    this.tfIdf = !this.tfIdf;
    let query = this.dataService.getQuery();
    let searchParam = 'tfidf=';
    let tfIdfRaw = this.tfIdf ? "1" : "0";
    let idx = query.indexOf(searchParam) + searchParam.length;
    if(idx === -1) {
      this.dataService.storeQuery(query + "&" + searchParam + tfIdfRaw);
    } else {
      let newQuery = query.substr(0, idx) + tfIdfRaw + query.substr(idx+1);
      this.dataService.storeQuery(newQuery);
    }
    this.loadResults();
  }

  ngOnInit(): void {
    this.loadResults();
  }

  getSecondsDifference(requestBeginMilli: number): number {
    let requestEndMilli = (new Date()).getTime();
    return (requestEndMilli-requestBeginMilli)/1000.0;
  }

  updateResponseTime(requestBeginMilli: number): void {
    let time = this.getSecondsDifference(requestBeginMilli);
    document.getElementById("responseTimeHeader").innerHTML = `Response time: ${time.toString()} seconds.`;
  }

  loadResults(): void {
    let query = this.dataService.getQuery();
    document.getElementById("toFill").innerHTML = "";
    document.getElementById("responseTimeHeader").innerHTML = "";
    this.isLoading = true;
    let requestBeginMilli = (new Date()).getTime();
    this.riService.getHTMLForSearch(query).subscribe(resp => {
      this.isLoading = false;
      if(resp.obj._body=="")this.noResults=true;
      else document.getElementById("toFill").innerHTML = resp.obj._body;
      this.updateResponseTime(requestBeginMilli);
    },error=>{
      this.isLoading=false;
      this.hasErrors=true;
      this.updateResponseTime(requestBeginMilli);
    });
  }

  goBack(): void {
    this.router.navigate(['/']);
  }

}
