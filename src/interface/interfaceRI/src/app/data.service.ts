import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private query = "";
  
  constructor() {
    this.query = window.location.search
  }

  storeQuery(q:string){
    this.query=q;
  }

  getQuery(){
    return this.query;
  }

  clearQuery(){
    this.query="";
  }

}
