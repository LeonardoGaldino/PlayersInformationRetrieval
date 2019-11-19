import { Injectable } from '@angular/core';
import { environment } from '../environments/environment'
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs';
import { map,catchError } from 'rxjs/operators';

const API_URL = environment.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class RiServiceService {

  constructor(private http: Http) { }

  private handleError (error: Response | any) {
    return Observable.throw(error);
  }

  public getHTMLForSearch(query: string): Observable<string> {
    return this.http
      .get(API_URL + '/HTMLSearch/' + query).pipe(map(response=>response.json()))
  }

  public testHTMLForSearch(query: string): string {
    return "<div class='card' style='width: 677px;height: 93px;margin-left: 166px;margin-bottom: 27px'><div class='card-body'><h3 class='card-title' style='margin-bottom: 0px;color: #1a0dab;font-size: 20px;font-weight: 400;line-height: 26px;font-family:arial,sans-serif'>Entendendo RxJS Observable com Angular - Medium</h3><h5 class='card-subtitle mb-2 text-muted' style='margin-bottom: 0px;margin-top: 0px;color:#006621;font-style: normal;font-size: 16px;font-weight: 400;line-height: 24px;padding-top: 1px;font-family:arial,sans-serif'>https://medium.com/tableless/entendendo-rxjs-observable-com-angular-6f607a9a6a00</h5><span class='card-text' style='color: #545454;font-family: arial,sans-serif;font-size: 14px;font-weight: 400;line-height: 21.98px;'>4 de jan. de 2017 - Após passar por um projeto com Angular 2(ou somente Angular, para os mais íntimos) posso dizer que: É um framework com muitas ...</span></div></div>"
  }
}
