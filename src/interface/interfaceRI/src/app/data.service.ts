import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private query = "";
  
  constructor() { }

  storeQuery(q:string){
    this.query=q;
  }

  getQuery(){
    return this.query;
  }

  clearQuery(){
    this.query=undefined;
  }

}
